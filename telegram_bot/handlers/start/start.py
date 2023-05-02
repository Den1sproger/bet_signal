from aiogram import types
from ...bot_config import dp, ADMIN



WELCOME_TEXT = """
Привет👋👋👋
Я буду присылать тебе сигналы на ставку
в спортивных матчах
"""

HELP_TEXT_ADMIN = """
❗️❗️❗️<b>Вы являетесь администратором системы</b>❗️❗️❗️
👨🏻‍⚕️👨🏻‍⚕️👨🏻‍⚕️
Главное меню - комнада /main_menu
1️⃣<em>Кнопка</em> <b>Добавить список рассылки</b> - добавляет список расссылки
2️⃣<em>Кнопка</em> <b>Посмотреть списки рассылки</b> - выводит названия списков рассылок
3️⃣<em>Кнопка</em> <b>Посмотреть юзеров и их подписки</b> - выводит список юзеров и их подписки
4️⃣<em>Кнопка</em> <b>Удалить список рассылки</b> - удаляет вводимый список рассылки
⚠️⚠️Если вы начали какую либо оперцию, требующую ввода данных
и потом передумали, нажмите кнопку cancel (или введите слово вручную)
"""


@dp.message_handler(commands=['start'])
async def start(message: types.Message) -> None:
    await message.answer(WELCOME_TEXT)


@dp.message_handler(commands=['help'], user_id=ADMIN)
async def send_instruction(message: types.Message) -> None:
    await message.answer(HELP_TEXT_ADMIN, parse_mode='HTML')