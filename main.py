import requests
from pathlib import Path
import os
from urllib.parse import urlparse
from requests.models import HTTPError


def get_pic(url_pic, destination_folder):
    Path(destination_folder).mkdir(parents=True, exist_ok=True)
    filename = f'{destination_folder}/hubble.jpeg'
    response = requests.get(url_pic)
    response.raise_for_status()

    with open(filename, 'wb') as file:
        file.write(response.content)
    return response.ok


def main():
        get_pic('https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg', 'images')


if __name__ == '__main__':
    main()

