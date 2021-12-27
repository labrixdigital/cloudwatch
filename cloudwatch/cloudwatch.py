import logging

class CloudwatchHandler(logging.Handler):
  """
  This is a lightweight Handler for Python's standard logging to send logs 
  to AWS Cloudwatch. It extends the logging Handler and replaces the emit
  Usage:
  from cloudwatch import cloudwatch
  ... create python logger ...
  handler = cloudwatch.CloudwatchHandler('yourLogGroup','yourLogStream')
  logger.addHandler(handler)
  """
 
  import boto3
  import time

  def __init__(self, 
    access_id = None, 
    access_key = None, 
    region = None, 
    log_group = None, 
    log_stream = None
  ):
    #First validate and populate defaults
    if not log_group:
      raise ValueError('At least log_group keyword argument is required')
    if not log_stream:
      from datetime import datetime
      from random import randrange
      log_stream = '{}{}'.format(
        datetime.strftime(datetime.now(),"%Y%m%d%H%M%S%f"),
        randrange(100)
      )
    #Set them in self
    self.log_group = log_group
    self.log_stream = log_stream
    self.next_sequence_token = None

    #If there is no keys specified use a default session
    if not access_id and not region:
      self.logs = self.boto3.client('logs')
    elif not access_id:
      self.logs = self.boto3.client('logs', region_name=region)
    else:
      #Create required AWS Objects and Variables
      self.session = self.boto3.Session(
        aws_access_key_id=access_id,
        aws_secret_access_key=access_key,
        region_name=region
      )
      self.logs = self.session.client('logs')

    try:
      #Get the streams and find the desired token
      response = self.logs.describe_log_streams(logGroupName=self.log_group)
      for l in response['logStreams']:
        if l['logStreamName'] == self.log_stream:
          self.next_sequence_token =l['uploadSequenceToken'] if 'uploadSequenceToken' in l else None
      #If no token then create the stream
      if self.next_sequence_token == None:
        self.logs.create_log_stream(logGroupName=self.log_group, logStreamName=self.log_stream)
    
    #On Resource Error (from checking the describe_log_streams, create the group since it doesnt exist)
    except self.logs.exceptions.ResourceNotFoundException as e:
      self.logs.create_log_group(logGroupName=self.log_group)
      self.logs.create_log_stream(logGroupName=self.log_group, logStreamName=self.log_stream)

    except self.logs.exceptions.ResourceAlreadyExistsException:
      #Ignore ResourceAlreadyExistsException that arises if we have no token but means the stream does exist
      pass

    #Continue to initialize the rest of the handler (from its parent logging.Handler)
    logging.Handler.__init__(self)

  def send_log(self, timestamp, log_entry):
    #Send the message to AWS (function depends if there is a token or not)
    if self.next_sequence_token:
      response = self.logs.put_log_events(logGroupName=self.log_group,
        logStreamName=self.log_stream,
        sequenceToken = self.next_sequence_token,
        logEvents=[{'timestamp': timestamp,'message': log_entry}])
    else:
      response = self.logs.put_log_events(logGroupName=self.log_group,
        logStreamName=self.log_stream,
        logEvents=[{'timestamp': timestamp,'message': log_entry}])

    #Store the next token
    self.next_sequence_token = response['nextSequenceToken']

  def emit(self, record):
    """This is the overriden function from the handler to send logs to AWS
    """
    #Get current time in MS (required by AWS)
    timestamp = round(self.time.time() * 1000)
    
    #Format the message (using Formatter of the logging)
    log_entry = self.format(record)
  
    try:
      self.send_log(timestamp, log_entry)

    except self.logs.exceptions.DataAlreadyAcceptedException as e:
      #Ignore DataAlreadyAcceptedException and get next token
      exception_text = str(e)
      self.next_sequence_token = exception_text[exception_text.find("sequenceToken: ")+15:]

    except self.logs.exceptions.InvalidSequenceTokenException as e:
      #If we get an invalid sequence, change the token and retry
      exception_text = str(e)
      self.next_sequence_token = exception_text[exception_text.find("sequenceToken is: ")+18:]
      self.send_log(timestamp, log_entry)

    except self.logs.exceptions.ClientError as e:
      #Wait and try resending
      self.time.sleep(3)
      self.send_log(timestamp, log_entry) 