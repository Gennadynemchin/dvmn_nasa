import os
from time import sleep


def upload_pic(bot, destination_folder, chat_id, delay):
    for filename in os.listdir(destination_folder):
        if filename.endswith(('jpg', 'gif', 'png')):
            with open(f'{destination_folder}/{filename}', 'rb') as pic:
                bot.send_photo(chat_id=chat_id, photo=pic)
            sleep(delay)
