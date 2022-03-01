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
    params = {'api_key' : nasa_token, 'count': 100}
    response = requests.get('https://api.nasa.gov/planetary/apod', params=params)
    response.raise_for_status()
    decoded_response = response.json()

    for x in decoded_response:
        try:
            apod_link = x['url']
            print('ok', apod_link)
        except KeyError:
            pass
        else:
            pathname, extension = os.path.splitext(apod_link)
            filename = pathname.split('/')
            response = requests.get(apod_link)
            response.raise_for_status()
            file_path = f'{destination_folder}/nasa_apod_{filename[-1]}{extension}'

            with open(file_path, 'wb') as file:
                file.write(response.content)
    return response.ok


def nasa_epic(destination_folder, nasa_token):

    return


def get_extension(link):
    result = urlparse(link).path
    ext = os.path.splitext(result)[1]
    return ext


def main():
    load_dotenv()
    nasa_token = os.getenv('NASATOKEN')

    #get_pic('https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg', 'images')
    #fetch_spacex_last_launch('spacex')
    nasa_apod('nasa_apod', nasa_token)
    #print(get_extension('"https://example.com/txt/hello%20world.txt?v=9#python"'))

if __name__ == '__main__':
    main()
