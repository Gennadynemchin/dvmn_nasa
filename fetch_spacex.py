import requests
import datetime
from pathlib import Path


def get_spacex_last_launch(destination_folder):
    Path(destination_folder).mkdir(parents=True, exist_ok=True)
    response = requests.get('https://api.spacexdata.com/v3/launches/past')
    response.raise_for_status()
    decoded_response = response.json()

    for launch in reversed(decoded_response):
        if launch['links']['flickr_images']:
            for to_download in launch['links']['flickr_images']:
                filename = f'{destination_folder}/spacex_launch_{datetime.datetime.now().time()}.jpeg'
                response = requests.get(to_download)
                response.raise_for_status()
                with open(filename, 'wb') as file:
                    file.write(response.content)
            break
