# AWS Cloudwatch Lightweight Handler

This small log handler is designed to send events to AWS Cloudwatch. It is useful when operating infrastructure outside of the AWS, when AWS does not log automatically (EC2) or when you want to separate logs. If you are logging on Serverless Infrastructure (e.g. Lambdas or ECS) you might find it easier to just let AWS Handle the logs automatically.

We originally developed this to be used on dedicated servers (on and off EC2) and chose to create something new because we wanted to:

* Be able to provide your own AWS programmatic access credentials
* Have a lightweight solution (only the handler is included and you need only one file)

If you already have a codebase that is using python's logger, you only need minor modifications to send your logs to AWS. In fact, you only need to change code at the logger creation. If you haven't done any logging before, I recommend you look at a basic tutorial on python's logging module. There are plenty of resources out there.

# Installing it

We are on PyPi, so you can install via pip

```bash
pip install cloudwatch
```

Or if you prefer to customise and (hopefully) feedback on improvements and bugs

```bash
git clone https://github.com/labrixdigital/cloudwatch
```

# Usage

This module is designed to fit right into your existing logging code, so you only need to replace (or add) a handler and the same logger will send events to cloudwatch.

```python
import logging
#Create the logger
logger = logging.getLogger('my_logger')
#Create the formatter
formatter = logging.Formatter('%(asctime)s : %(levelname)s - %(message)s')

#Import cloudwath and create the new handler
from cloudwatch import cloudwatch
handler = cloudwatch.CloudwatchHandler(log_group = 'my_log_group')

#Pass the formater to the handler
handler.setFormatter(formatter)
#Set the level
logger.setLevel(logging.WARNING)
#Add the handler to the logger
logger.addHandler(handler)

#USE IT!
logger.warning("Watch out! Something happened!")
```

# Credentials

## Specifying credentials and region

If you dont add credentials when creating the handler, it uses the default AWS credentials that you set-up on the CLI, or that you passed on the invokation (if using on EC2, Lambda, ECS), this is in line with the boto3 configuration [Expained here](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html). However, you can also specify the credentials like this:

```python
handler = cloudwatch.CloudwatchHandler(
 log_group = 'my_log_group',
 access_id = 'AWS_ACCESS_KEY_ID', 
 access_key = 'AWS_SECRET_ACCESS_KEY'
)
```

Likewise, you can specify a region where the logger will be with the parameter: `region = 'us-east-1'`

## Specifying log stream

If you dont add a log stream, the logger will create one for you with the timestamp and a random number. This is useful when you have multiple processes logging to the same log group without colliding. If you want, you can specify the log stream like this:

```python
handler = cloudwatch.CloudwatchHandler(
 log_group = 'my_log_group',
 log_stream = 'my_log_stream'
)
```

# Overflow

AWS CloudWatch Logs takes a maximum event size of 256 KB ([reference](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutLogEvents.html)). This means that large messages can result in an error if not handled correctly. We have included 3 options in the parameters:
* __error__: This is the default, and will simply raise a value exception
* __truncate__: This will truncate the original message to the maximum possible size and log it
* __split__: This will divide the original message into multiple parts of the maximum size and send them separately

One caveat is that because the truncate and split options are based on bytes and not characters (because its size limited), its possible that non-ASCII characters will end up being split or truncated.

```python
#Specify truncate
handler = cloudwatch.CloudwatchHandler(
 log_group = 'my_log_group',
 overflow = 'truncate'
)

#Specify split
```python
handler = cloudwatch.CloudwatchHandler(
 log_group = 'my_log_group',
 overflow = 'split'
)
```

# Parameters

|Positional order|Keyword argument|Required|Default|Description|
|---|---|---|---|---|
|0|`access_id`|No|Taken from the AWS Configuration File or Role|The AWS Access Key ID that you want to use to interact with your AWS Account. Usually a 20 character alphanumeric.|
|1|`access_key`|No|Taken from the AWS Configuration File or Role|The corresponding AWS Secret to the above parameter|
|2|`region`|No|Taken from the AWS Configuration File or Role|The AWS Region name (e.g. `us-east-1`)|
|3|`log_group`|Yes||The name of the log group. If it already exists, it writes to it, otherwise it creates it.|
|4|`log_stream`|No|Datetime in the format `%Y%m%d%H%M%S%f` and 3 random digits|The name of the log stream. If it already exists, it writes to it, otherwise it creates it.|
|5|`overflow`|No|Defines the behaviour when a message is too large to send in one API call. Either `'error'`, `'truncate'` or `'split'`. Default is `'error'`|

# Legacy initialisation

We much prefer keyword arguments, and encourage you to use them. However, if you really want to avoid some typing, the order of the positional arguments work as follows:

```python
handler = cloudwatch.CloudwatchHandler(
 'AWS_ACCESS_KEY_ID',
 'AWS_SECRET_ACCESS_KEY',
 'REGION',
 'LOG_GROUP',
 'LOG_STREAM',
 'OVERFLOW'
)
```


