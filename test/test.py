# 0 - GET LOGGER READY
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

# 1 - TESTS
# 1.1 Small
logger.warning('Hello World')

# 1.2 Large, but not overflowing
with open('test/message_256.txt', 'r') as f:
 message = f.read()
logger.warning(message)

# 1.3 Overflowing should generate error
with open('test/message_257.txt', 'r') as f:
 message = f.read()
try:
 logger.warning(message)
except ValueError as e:
 if not str(e).startswith('Overflow:'):
  raise e

# 1.4 Overflow with truncation
logger.handlers.clear()
handler = cloudwatch.CloudwatchHandler(
 log_group = 'my_log_group', overflow='truncate')
handler.setFormatter(formatter)
logger.setLevel(logging.WARNING)
logger.addHandler(handler)
#Try again
logger.warning(message)

# 1.5 Overflow with split
logger.handlers.clear()
handler = cloudwatch.CloudwatchHandler(
 log_group = 'my_log_group', overflow='split')
handler.setFormatter(formatter)
logger.setLevel(logging.WARNING)
logger.addHandler(handler)
#Try again
logger.warning(message)