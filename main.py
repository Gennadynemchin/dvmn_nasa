import datetime
import requests
import logging
import telegram
import os
from bot import upload_pic
from dotenv import load_dotenv
from urllib.parse import urlparse
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

    Path(destination_folder).mkdir(parents=True, exist_ok=True)

    for x in last_launch_pics:
        filename = f'{destination_folder}/spacex_launch_{datetime.datetime.now().time()}.jpeg'
        response = requests.get(x)
        response.raise_for_status()

        with open(filename, 'wb') as file:
            file.write(response.content)
    return response.ok


def nasa_apod(destination_folder, nasa_token):
    Path(destination_folder).mkdir(parents=True, exist_ok=True)
    params = {'api_key': nasa_token, 'count': 30}
    response = requests.get('https://api.nasa.gov/planetary/apod', params=params)
    response.raise_for_status()
    decoded_response = response.json()

    for x in decoded_response:
        try:
            apod_link = x['hdurl']
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
    Path(destination_folder).mkdir(parents=True, exist_ok=True)
    url = 'https://api.nasa.gov/EPIC/api/natural/images'
    params = {'api_key': nasa_token}
    response = requests.get(url, params=params)
    response.raise_for_status()
    decoded_response = response.json()

    for x in decoded_response:
        image = x['image']
        date_time_str = x['date']
        date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
        year, month, day = date_time_obj.year, '%02d' % date_time_obj.month, '%02d' % date_time_obj.day
        url_pic = f'https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image}.png'
        pathname, extension = os.path.splitext(url_pic)
        filename = pathname.split('/')
        response_pic = requests.get(url_pic, params=params)
        response_pic.raise_for_status()
        file_path = f'{destination_folder}/nasa_{filename[-1]}{extension}'

        with open(file_path, 'wb') as file:
            file.write(response_pic.content)
    return response.ok


def get_extension(link):
    result = urlparse(link).path
    ext = os.path.splitext(result)[1]
    return ext


def main():
    load_dotenv()
    nasa_token = os.getenv('NASATOKEN')
    destination_folder = os.getenv('DESTINATION_FOLDER')
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    telegram_channel = os.getenv('TELEGRAM_CHANNEL')
    delay = int(os.getenv('SENDING_DELAY'))

    bot = telegram.Bot(token=telegram_token)
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    get_pic('https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg', destination_folder)
    fetch_spacex_last_launch(destination_folder)
    nasa_apod(destination_folder, nasa_token)
    nasa_epic(destination_folder, nasa_token)

    while True:
        upload_pic(bot, destination_folder, telegram_channel, delay)


if __name__ == '__main__':
    main()
