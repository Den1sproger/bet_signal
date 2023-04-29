from aiogram import types
from ...bot_config import dp, bot, ADMIN
from ...keyboards import add_to_mail_ikb
from database import Database



@dp.message_handler(lambda message: message.text == '+', user_id=not ADMIN)
async def add_user(message: types.Message) -> None:
    chat_id = message.from_user.id
    if chat_id != ADMIN:
        username = message.from_user.username
        if not username:
            username = message.from_user.full_name

        db = Database()

        additional_text = ''

        if not db.is_user_in_db(chat_id):
            db.action(
                f"INSERT INTO subscribers (nickname, chat_id) VALUES ('{username}', '{chat_id}');"
            )
        else:
            additional_text += ' (уже есть в базе)'

        user_id = db.get_one_data_cell(
            query=f"SELECT id FROM subscribers WHERE chat_id = '{chat_id}';",
            column="id"
        )

        await bot.send_message(
            chat_id=ADMIN,
            text=f'{user_id} @{username} подана заявка на подписку{additional_text}',
            reply_markup=add_to_mail_ikb
        )