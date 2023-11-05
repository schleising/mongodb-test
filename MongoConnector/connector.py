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
        '''
        MongoConnector
        --------------

        Connect to a mongodb server, will read the server url from a file if not provided.

        The connection will be closed on exit either normally or by an exception.
        
        Parameters
        ----------
        
        server_url : str | None
            The url of the mongodb server to connect to. If None, the server url will be read from a file.
            
        enable_debug : bool
            Enable debug logging
        
        Returns
        -------
        
        None
        
        Raises
        ------
        
        None
        
        Examples
        --------
        
        >>> from MongoConnector import MongoConnector
        >>> connector = MongoConnector()
        >>> connector.connected
        True
        >>> connector.get_database_list()
        ['admin', 'config', 'local']
        >>> connector.get_collection_list('admin')
        ['system.version']
        '''
        # Set the logging level to DEBUG if enabled
        if enable_debug:
            logger.setLevel(logging.DEBUG)

        # Check if server url is provided
        if server_url is None:
            # Get server url
            self._server_url = self._get_server_url()
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
            '''
            A flag indicating whether the connector is connected to the mongodb server
            
            Type: bool
            
            True if connected, False otherwise
            '''
        else:
            # Log success message
            logger.debug(f'Connected to server {self._server_url}')

            # Set connected flag
            self.connected = True

            # Close connection on exit
            atexit.register(self.close)

    def _get_server_url(self) -> str:
        '''
        Read the server url from a file
        
        Parameters
        ----------
        
        None
        
        Returns
        -------
        
        server_url : str
            The url of the mongodb server
            
        Raises
        ------
        
        None
        '''
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
        '''
        Close the connection to the mongodb server

        Parameters
        ----------

        None

        Returns
        -------

        None

        Raises
        ------

        None
        '''
        # Close connection
        self._client.close()

        # Set connected flag
        self.connected = False

        # Log message
        logger.debug(f'Closed connection to server {self._server_url}')

    def get_database(self, database_name: str) -> Database | None:
        '''
        Get a database from the mongodb server
        
        Parameters
        ----------
        
        database_name : str
            The name of the database to get
            
        Returns
        -------
        
        database : Database | None
            The database if found, None otherwise
        
        Raises
        ------
        
        None
        
        Examples
        --------
        
        >>> from MongoConnector import MongoConnector
        >>> connector = MongoConnector()
        >>> connector.get_database('admin')
        Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), 'admin')
        >>> connector.get_database('not_a_database')
        None
        '''
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
        '''
        Get a collection from the mongodb server

        Parameters
        ----------

        database_name : str
            The name of the database to get

        collection_name : str
            The name of the collection to get

        Returns
        -------

        collection : Collection | None
            The collection if found, None otherwise

        Raises
        ------

        None

        Examples
        --------

        >>> from MongoConnector import MongoConnector
        >>> connector = MongoConnector()
        >>> connector.get_collection('admin', 'system.version')
        Collection(Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), 'admin'), 'system.version', ...)
        >>> connector.get_collection('admin', 'not_a_collection')
        None
        '''
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

    def get_database_list(self) -> list[str]:
        '''
        Get a list of databases from the mongodb server
        
        Parameters
        ----------
        
        None
        
        Returns
        -------
        
        database_list : list[str]
            The list of databases
        
        Raises
        ------
        
        None
        
        Examples
        --------
        
        >>> from MongoConnector import MongoConnector
        >>> connector = MongoConnector()
        >>> connector.get_database_list()
        ['admin', 'config', 'local']
        '''
        # Return list of databases
        return sorted(self._client.list_database_names())

    def get_collection_list(self, database_name: str) -> list[str]:
        '''
        Get a list of collections from the mongodb server

        Parameters
        ----------

        database_name : str
            The name of the database to get
        
        Returns
        -------

        collection_list : list[str]
            The list of collections

        Raises
        ------

        None

        Examples
        --------

        >>> from MongoConnector import MongoConnector
        >>> connector = MongoConnector()
        >>> connector.get_collection_list('admin')
        ['system.version']
        >>> connector.get_collection_list('not_a_database')
        []
        '''
        # Get database
        database = self.get_database(database_name)

        # Return None if database not found
        if database is None:
            return []

        # Return list of collections
        return sorted(database.list_collection_names())
