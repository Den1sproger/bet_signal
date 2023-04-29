from aiogram import executor
from telegram_bot import dp
from telegram_bot.handlers.start.start import *
from telegram_bot.handlers.admin.main_menu import *
from telegram_bot.handlers.admin.states import *
from telegram_bot.handlers.admin.user_work import *
from telegram_bot.handlers.user.add import *



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)