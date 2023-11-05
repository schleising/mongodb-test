from MongoConnector import MongoConnector
from MongoConnector.databases import MEDIA_DATABASE, WEB_DATABASE

def main() -> None:
    # Connect to server
    connector = MongoConnector()

    # Check if connected
    if connector.connected:
        # Get the list of collections in the media database
        collections = connector.get_collection_list(MEDIA_DATABASE)

        # Print the list of collections in the media database
        print(f'Collections in {MEDIA_DATABASE}:')
        for collection in collections:
            print(f'  {collection}')

        print()

        # Get the list of collections in the web database
        collections = connector.get_collection_list(WEB_DATABASE)

        # Print the list of collections in the web database
        print(f'Collections in {WEB_DATABASE}:')
        for collection in collections:
            print(f'  {collection}')

if __name__ == '__main__':
    main()
