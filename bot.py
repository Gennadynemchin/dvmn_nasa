import logging
import os
import telegram
from time import sleep
from dotenv import load_dotenv


load_dotenv()
telegram_token = os.getenv('TELEGRAM_TOKEN')
bot = telegram.Bot(token=telegram_token)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


def upload_pic(destination_folder, chat_id, delay):
    for filename in os.listdir(destination_folder):
        if filename.endswith(('jpg', 'gif', 'png')):
            with open(f'{destination_folder}/{filename}', 'rb') as pic:
                bot.send_photo(chat_id=chat_id, photo=pic)
            sleep(delay)


def main() -> None:
    while True:
        upload_pic('nasa_apod', '@show_me_nasa_pics', 10)


if __name__ == '__main__':
    main()
