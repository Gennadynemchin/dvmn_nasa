import logging
import telegram
import os
from bot import upload_pic
from dotenv import load_dotenv
from fetch_nasa import get_nasa_apod, get_nasa_epic
from fetch_spacex import get_spacex_last_launch


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
    get_spacex_last_launch(destination_folder)
    get_nasa_apod(destination_folder, nasa_token)
    get_nasa_epic(destination_folder, nasa_token)

    while True:
        upload_pic(bot, destination_folder, telegram_channel, delay)


if __name__ == '__main__':
    main()
