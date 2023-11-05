from pathlib import Path
import subprocess

from rich import print

from MongoConnector import MongoConnector
from MongoConnector.databases import MEDIA_DATABASE
from MongoConnector.collections import MEDIA_COLLECTION

def main() -> None:
    # Connect to server
    connector = MongoConnector()

    # Check if connected
    if connector.connected:
        collection = connector.get_collection(MEDIA_DATABASE, MEDIA_COLLECTION)

        # Check if collection exists
        if collection is None:
            print('[red]Collection not found[/red]')
            return

        # Get all documents in the media collection where conversion_error is true
        documents = collection.find({'conversion_error': True})

        # Create a list of document file paths prepending each filename with /Volumes
        filepaths = [Path(f'/Volumes{document["filename"]}') for document in documents]

        # Print the list of filenames
        print(f'Conversion errors:')
        for filename in filepaths:
            print(f'  {filename}')

        # Use a subprocess to convert the files to h265 using ffmpeg
        for filepath in filepaths:
            subprocess.run(['ffmpeg', '-i', filepath.absolute(), '-c:v', 'libx265', '-crf', '28', '-c:a', 'copy', f'/Users/steve/Downloads/{filepath.stem}.mkv'])

if __name__ == '__main__':
    main()
