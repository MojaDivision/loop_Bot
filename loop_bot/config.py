import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN', '8828932102:AAGHqCIuLAHhMPi0BfggYwLRuo-PfIhQCRk')
CHANNEL_ID = os.getenv('CHANNEL_ID', '@ofiicial_loop')
BOT_USERNAME = os.getenv("BOT_USERNAME", "@Official_Loop_Bot")
CHANNEL_URL = os.getenv('CHANNEL_URL', 'https://t.me/ofiicial_loop')

DOWNLOAD_DIR = 'downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
