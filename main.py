import datetime
import requests
import json
import os
from dotenv import load_dotenv
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


def fetch_spacex_last_launch(destination_folder):
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


def nasa_apod(destination_folder, nasa_token):
    Path(destination_folder).mkdir(parents=True, exist_ok=True)
    params = {'api_key' : nasa_token}
    response = requests.get('https://api.nasa.gov/planetary/apod', params=params)
    response.raise_for_status()
    decoded_response = response.json()

    return decoded_response


def main():
    load_dotenv()
    nasa_token = os.getenv('NASATOKEN')
    #get_pic('https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg', 'images')
    #fetch_spacex_last_launch('spacex')
    print(nasa_apod('nasa_apod', nasa_token))

if __name__ == '__main__':
    main()
