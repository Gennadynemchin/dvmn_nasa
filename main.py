import datetime
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
    response = requests.get('https://api.spacexdata.com/v3/launches/past')
    response.raise_for_status()
    decoded_response = response.json()
    last_launch_pics = decoded_response[spacex_launch_counter]['links']['flickr_images']

    while len(last_launch_pics) < 1:
        spacex_launch_counter -= 1
        last_launch_pics = decoded_response[spacex_launch_counter]['links']['flickr_images']
        print(last_launch_pics)

    Path(destination_folder).mkdir(parents=True, exist_ok=True)

    for x in last_launch_pics:
        print(x)
        filename = f'{destination_folder}/spacex_launch_{datetime.datetime.now().time()}.jpeg'
        response = requests.get(x)
        response.raise_for_status()

        with open(filename, 'wb') as file:
            file.write(response.content)

    return response.ok


def main():
    #get_pic('https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg', 'images')
    get_last_spacex('spacex')

if __name__ == '__main__':
    main()
