import telegram
import os
from dotenv import load_dotenv


load_dotenv()
telegram_token = os.getenv('TELEGRAM_TOKEN')

bot = telegram.Bot(token = telegram_token)

print(bot.get_me())
chat_id = '@show_me_nasa_pics'
bot.send_message(chat_id=chat_id, text='Initial commit')
