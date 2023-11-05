from MongoConnector import MongoConnector

def main() -> None:
    # Connect to server
    connector = MongoConnector()

    # Check if connected
    if connector.connected:
        # Get the list of databases
        databases = connector.get_database_list()

        # Print the list of databases
        print('Databases:')
        for database in databases:
            print(f'  {database}')

if __name__ == '__main__':
    main()
