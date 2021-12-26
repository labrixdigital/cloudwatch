# AWS Cloudwatch Lightweight Handler

This small log handler is designed to send events to AWS Cloudwatch. It is useful when operating infrastructure outside of the AWS Serverless Infrastructure (e.g. Lambdas or ECS). You can still integrate it in your Serverless Infrastructure, but you might find it easier to just let AWS Handle the logs in this cases.

We originally developed this to be used on dedicated servers (on and off EC2) and chose to create something new because we wanted:

* Provide your own AWS programmatic access credentials
* Lightweight (only the handler is included and you need only one file)

If you already have a codebase that is using python's logger, you only need minor modifications to send your logs to AWS. In fact, you only need to change code at the logger creation. If you havent done any logging before, I recommend you look at a basic tutorial on python's logging module. There are plenty of resources out there.

# Installing it

We are on PyPi, so you can install via pip

```bash
pip install cloudwatch
```

Or if you prefer to customise and (hopefully) feedback on improvements and bugs

```bash
git clone https://github.com/ernestomonroy/cloudwatch
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

## Specifying credentials and region

If you dont add credentials when creating the handler, it uses the default AWS credentials that you set-up on the CLI, or that you passed on the invokation (if using on EC2, Lambda, ECS). However, you can also specify the credentials like this:

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

## Legacy

We much prefer keyword arguments, and encourage you to use them. However, if you really want to avoid some typing, the order of the positional arguments work as follows:

```python
handler = cloudwatch.CloudwatchHandler(
 'AWS_ACCESS_KEY_ID',
 'AWS_SECRET_ACCESS_KEY',
 'REGION',
 'LOG_GROUP',
 'LOG_STREAM'
)
```
