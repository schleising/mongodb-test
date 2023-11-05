import atexit
import logging
from pathlib import Path

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure

from . import logger

class MongoConnector:
    def __init__(self, server_url: str | None = None, enable_debug: bool = False) -> None:
        # Set the logging level to DEBUG if enabled
        if enable_debug:
            logger.setLevel(logging.DEBUG)

        # Check if server url is provided
        if server_url is None:
            # Get server url
            self._server_url = self.get_server_url()
        else:
            # Set server url
            self._server_url = server_url

        # Connect to server
        self._client = MongoClient(self._server_url, serverSelectionTimeoutMS=1000)

        # Check if connected
        try:
            # Ping server
            self._client.admin.command('ping')
        except ConnectionFailure:
            # Log error message
            logger.error(f'Could not connect to server {self._server_url}')

            # Set connected flag
            self.connected = False
        else:
            # Log success message
            logger.debug(f'Connected to server {self._server_url}')

            # Set connected flag
            self.connected = True

            # Close connection on exit
            atexit.register(self.close)

    def get_server_url(self) -> str:
        # Read server from config file
        server_path = Path('./server.txt')

        if server_path.exists():
            # Read server from file
            with open(server_path, 'r') as f:
                server_url = f.read().strip()

            return server_url
        else:
            # Log warning
            logger.warning('Server file not found')

            # Retern the default localhost mongodb server
            return 'mongodb://localhost:27017/'

    def close(self) -> None:
        # Close connection
        self._client.close()

        # Log message
        logger.debug(f'Closed connection to server {self._server_url}')

    def get_database(self, database_name: str) -> Database | None:
        # Check the database exists
        if database_name in self._client.list_database_names():
            # Log success message
            logger.debug(f'Database \'{database_name}\' found')

            # Return database
            return self._client[database_name]
        else:
            # Log the error
            logger.error(f'Database \'{database_name}\' not found')

            # Return None
            return None

    def get_collection(self, database_name: str, collection_name: str) -> Collection | None:
        # Get database
        database = self.get_database(database_name)

        # Return None if database not found
        if database is None:
            return None

        # Check if database exists
        if collection_name in database.list_collection_names():
            # Log success message
            logger.debug(f'Collection \'{collection_name}\' found in database \'{database_name}\'')

            # Return collection
            return database[collection_name]
        else:
            # Log the error
            logger.error(f'Collection \'{collection_name}\' not found in database \'{database_name}\'')

            # Return None
            return None
