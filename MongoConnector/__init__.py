import logging

# Set up a logger specific to this module
logger = logging.getLogger(__name__)

# Set the logging level to INFO
logger.setLevel(logging.INFO)

# Set the logger message format
formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)-8s : %(message)s')

# Add the formatter to the console handler
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

# Add the console handler to the logger
logger.addHandler(stream_handler)

# Import the Connector class
from .connector import MongoConnector

# Set the __all__ variable
__all__ = [
    'MongoConnector',
]
