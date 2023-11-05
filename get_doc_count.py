from rich import print

from MongoConnector import MongoConnector
from MongoConnector.databases import MEDIA_DATABASE
from MongoConnector.collections import MEDIA_COLLECTION

def main() -> None:
    # Connect to server
    connector = MongoConnector()

    # Check if connected
    if connector.connected:
        # Get the collection
        collection = connector.get_collection(MEDIA_DATABASE, MEDIA_COLLECTION)

        # Check if collection exists
        if collection is not None:
            # Print the number of documents in the collection
            print(f'[green]{collection.count_documents({})} documents in the collection \'{collection.name}\'[/green]')
        else:
            print('[red]Collection not found[/red]')

if __name__ == '__main__':
    main()
