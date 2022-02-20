import requests
import json
import os
from urllib.parse import urlparse
from requests.models import HTTPError
from pathlib import Path

def get_pic(url_pic, destination_folder):
    Path(destination_folder).mkdir(parents=True, exist_ok=True)
    filename = f'{destination_folder}/hubble.jpeg'
    response = requests.get(url_pic)
    response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)
    return response.ok


def get_last_spacex(destination_folder):
    Path(destination_folder).mkdir(parents=True, exist_ok=True)
    spacex_launch_counter = -1
    filename = f'{destination_folder}/spacex_launch_{spacex_launch_counter}.jpeg'
    response = requests.get('https://api.spacexdata.com/v3/launches/past')
    response.raise_for_status()
    decoded_response = response.json()
    last_launch_pics = decoded_response[spacex_launch_counter]['links']['flickr_images']

    if len(last_launch_pics) > 0:
        for x in last_launch_pics:
            with open(filename, 'wb') as file:
                file.write(x)
    else:
        spacex_launch_counter -= 1
    return response.ok

def main():
    #get_pic('https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg', 'images')
    get_last_spacex('spacex')

if __name__ == '__main__':
    main()
