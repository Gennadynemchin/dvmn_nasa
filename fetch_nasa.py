import datetime
import requests
import os
from pathlib import Path


def get_nasa_apod(destination_folder, nasa_token):
    Path(destination_folder).mkdir(parents=True, exist_ok=True)
    params = {'api_key': nasa_token, 'count': 30}
    response = requests.get('https://api.nasa.gov/planetary/apod', params=params)
    response.raise_for_status()
    decoded_response = response.json()

    for to_download in decoded_response:
        try:
            apod_link = to_download.get('hdurl')
            pathname, extension = os.path.splitext(apod_link)
            filename = pathname.split('/')
            response = requests.get(apod_link)
            response.raise_for_status()
            file_path = f'{destination_folder}/nasa_apod_{filename[-1]}{extension}'
        except TypeError:
            pass
        else:
            with open(file_path, 'wb') as file:
                file.write(response.content)
    return response.ok


def get_nasa_epic(destination_folder, nasa_token):
    Path(destination_folder).mkdir(parents=True, exist_ok=True)
    url = 'https://api.nasa.gov/EPIC/api/natural/images'
    params = {'api_key': nasa_token}
    response = requests.get(url, params=params)
    response.raise_for_status()
    decoded_response = response.json()

    for to_download in decoded_response:
        try:
            image = to_download.get('image')
            date_time_str = to_download.get('date')
            date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            year, month, day = date_time_obj.year, '%02d' % date_time_obj.month, '%02d' % date_time_obj.day
            url_pic = f'https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image}.png'
            pathname, extension = os.path.splitext(url_pic)
            filename = pathname.split('/')
            response_pic = requests.get(url_pic, params=params)
            response_pic.raise_for_status()
            file_path = f'{destination_folder}/nasa_epic_{filename[-1]}{extension}'
        except TypeError:
            pass
        else:
            with open(file_path, 'wb') as file:
                file.write(response_pic.content)
    return response.ok
