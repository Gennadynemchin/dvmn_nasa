import os
import random


def upload_pic(bot, destination_folder, chat_id):
    random_pic = random.choice(os.listdir(destination_folder))
    if random_pic.endswith(('jpg', 'gif', 'png')):
        with open(f'{destination_folder}/{random_pic}', 'rb') as pic:
            bot.send_photo(chat_id=chat_id, photo=pic)
