from pathlib import Path
import subprocess
from dataclasses import dataclass

from rich import print

from MongoConnector import MongoConnector
from MongoConnector.databases import MEDIA_DATABASE
from MongoConnector.collections import MEDIA_COLLECTION

@dataclass
class SuccessInfo:
    '''
    Class to hold information about successful conversions
    '''
    filepath: Path
    new_size: int

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

        # Create a list of successful and unsuccessful conversions
        successful: list[SuccessInfo] = []
        unsuccessful: list[Path] = []

        # Use a subprocess to convert the files to h265 using ffmpeg
        for filepath in filepaths:
            try:
                subprocess.run(['ffmpeg', '-i', filepath.absolute(), '-c:v', 'libx265', '-crf', '28', '-c:a', 'copy', f'/Users/steve/Downloads/{filepath.stem}.mkv'], check=True)
            except subprocess.CalledProcessError as e:
                print(f'[red]Error converting {filepath}[/red]')
                print(e)
                unsuccessful.append(filepath)
            else:
                print(f'[green]Converted {filepath}[/green]')
                success_info = SuccessInfo(filepath, filepath.stat().st_size)
                successful.append(success_info)

        # Print the list of successful conversions
        print(f'Successful conversions:')
        for filename in successful:
            print(f'  {filename}')

        # Print the list of unsuccessful conversions
        print(f'Unsuccessful conversions:')
        for filename in unsuccessful:
            print(f'  {filename}')

        # Save the list of successful conversions to a file
        with open('successful.txt', 'w', encoding='utf8') as f:
            for success_info in successful:
                f.write(f'{success_info.filepath}, {success_info.new_size}\n')

        # Save the list of unsuccessful conversions to a file
        with open('unsuccessful.txt', 'w', encoding='utf8') as f:
            for filename in unsuccessful:
                f.write(f'{filename}\n')

if __name__ == '__main__':
    main()
