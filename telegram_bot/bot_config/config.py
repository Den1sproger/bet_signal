import os

from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


TOKEN = os.getenv('BETS_TOKEN')
ADMIN = int(os.getenv('ADMIN'))

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())