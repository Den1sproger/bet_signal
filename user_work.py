from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import ChatNotFound
from ...bot_config import dp, bot, ADMIN
from .states import ProfileStatesGroup
from ...keyboards import get_mail_lists_kb, users_actions_ikb
from database import Database



mail_lists = []
current_user_id: int



@dp.callback_query_handler(lambda callback: callback.data == 'select_user')
async def select_user_by_id(callback: types.CallbackQuery) -> None:
    await callback.answer('Введите id')
    await ProfileStatesGroup.get_user_id.set()
    await bot.send_message(
        chat_id=ADMIN, 
        text='Введите id(число слева в списке юзеров) человека'
    )


@dp.message_handler(lambda message: not message.text.isdigit(),
                    state=ProfileStatesGroup.get_user_id)
async def check_id(message: types.Message) -> None:
    await message.reply('❌❌Это не id, нужна цифра')


@dp.message_handler(state=ProfileStatesGroup.get_user_id)
async def get_db_id(message: types.Message, state: FSMContext) -> None:
    user_id = int(message.text)

    db = Database()
    users_id = db.get_all_table_elements(
        query='SELECT id FROM subscribers;', element='id'
    )

    if user_id not in users_id:
        await message.reply('❌Пользователь с таким id отсутствует, попробуйте ввести еще раз')
    else:
        global current_user_id
        current_user_id = user_id

        INSTRUCTION = """
        1️⃣<b>Добавить подписки пользователю</b> - добавляет списков рассылки юзеру
        2️⃣<b>Удалить подписки у пользователя</b> - удаляет указанные списки рассылки юзера
        3️⃣<b>Удалить пользователя</b> - удаляет юзера
        """
        await state.finish()
        await message.answer(
            text=INSTRUCTION, reply_markup=users_actions_ikb, parse_mode='HTML'
        )


@dp.callback_query_handler(lambda callback: callback.data == 'add_mail_lists' \
                           or callback.data == 'remove_user_subscribes' \
                           or callback.data == 'add_into_mail_lists')
async def add_mail_list(callback: types.CallbackQuery) -> None:
    db = Database()
    
    is_mail_lists = db.get_one_data_cell(
        query='SELECT * FROM mail_lists;', column='id'
    )
    if not is_mail_lists:
        await bot.send_message(
            chat_id=ADMIN,
            text='❌❌Вы не создали еще ни одного списка рассылки, создайте списки и добавляйте юзеров'
        )
    else:
        global current_user_id

        if callback.data == 'add_mail_lists' or callback.data == 'add_into_mail_lists':
            await ProfileStatesGroup.get_adding_subscribes.set()
            if callback.data == 'add_into_mail_lists':
                current_user_id = int(callback.message.text.split()[0])
        else:
            await ProfileStatesGroup.get_removing_subscribes.set()

        await bot.send_message(
            chat_id=ADMIN,
            text='Выбирайте списки, если хотите закончить, жмите кнопку <b>cтоп</b>\n' \
                'Если вы ошиблись с выбором списков, то нажмите кнопку <b>заново</b>',
            reply_markup=get_mail_lists_kb(
                mail_lists=db.get_all_table_elements(
                    query='SELECT list_name FROM mail_lists;',
                    element='list_name'
                ),
                stop='стоп'
            ),
            parse_mode='HTML'
        )
        
    await bot.delete_message(
        chat_id=ADMIN,
        message_id=callback.message.message_id
    )
    

@dp.message_handler(Text(equals='заново'),
                    state=[ProfileStatesGroup.get_adding_subscribes,
                           ProfileStatesGroup.get_removing_subscribes])
async def again(message: types.Message) -> None:
    global mail_lists
    mail_lists.clear()
    await message.answer('Выбирайте списки сначала')


@dp.message_handler(Text(equals='стоп'),
                    state=ProfileStatesGroup.get_adding_subscribes)
async def stop_get_lists(message: types.Message, state: FSMContext) -> None:
    global mail_lists, current_user_id

    db = Database()

    lists_id = []
    for item in mail_lists:
        list_id = db.get_one_data_cell(
            query=f"SELECT id FROM mail_lists WHERE list_name = '{item}';",
            column='id'
        )
        lists_id.append(list_id)

    if db.is_maillist_in_user(current_user_id, lists_id):
        await message.answer(
            "❌❌Все или один из указанных вами списков уже есть в подписках этого пользователя" \
            " Попробуйте еще раз указать списки рассылки"
        )
    else:
        for item in mail_lists:
            list_id = db.get_one_data_cell(
                query=f"SELECT id FROM mail_lists WHERE list_name = '{item}';",
                column='id'
            )
            db.action(
                f"INSERT INTO bundle VALUES ({current_user_id}, {list_id});"
            )
            
        await state.finish()
        await message.answer(
            "✅Пользователь успешно подписан на рассылку",
            reply_markup=types.ReplyKeyboardRemove()
        )
        current_user_id = 0
        
    mail_lists.clear()


@dp.message_handler(Text(equals='стоп'),
                    state=ProfileStatesGroup.get_removing_subscribes)
async def stop_get_lists(message: types.Message, state: FSMContext) -> None:
    global mail_lists, current_user_id

    db = Database()

    lists_id = []
    for item in mail_lists:
        list_id = db.get_one_data_cell(
            query=f"SELECT id FROM mail_lists WHERE list_name = '{item}';",
            column='id'
        )
        lists_id.append(list_id)

    if not db.is_maillist_in_user(current_user_id, lists_id):
        await message.answer(
            "❌❌Все или один из указанных вами списков отсутствуют в подписках этого пользователя" \
            " Попробуйте еще раз указать списки рассылки"
        )
    else:
        for item in mail_lists:
            list_id = db.get_one_data_cell(
                query=f"SELECT id FROM mail_lists WHERE list_name = '{item}';",
                column='id'
            )
            db.action(
                f"DELETE FROM bundle WHERE user_id = {current_user_id} AND list_id = {list_id};"
            )
            
        await state.finish()
        await message.answer(
            "✅Списки удалены из подписок пользователя",
            reply_markup=types.ReplyKeyboardRemove()
        )
        current_user_id = 0
        
    mail_lists.clear()


@dp.message_handler(state=[ProfileStatesGroup.get_adding_subscribes,
                           ProfileStatesGroup.get_removing_subscribes])
async def get_mail_list(message: types.Message) -> None:
    global mail_lists
    mail_lists.append(message.text)

    await message.answer(
        "Список добавлен\nЖмите на название списка рассылки или кнопку <b>стоп</b>",
        parse_mode='HTML'
    )
    

@dp.callback_query_handler(lambda callback: callback.data == 'remove_user')
async def remove_user(callback: types.CallbackQuery) -> None:
    global current_user_id

    db = Database()
    db.action(
        f"DELETE FROM subscribers WHERE id = {current_user_id};"
    )
    db.action(
        f"DELETE FROM bundle WHERE user_id = {current_user_id};"
    )
    await callback.answer('Пользователь успешно удален')
    await bot.delete_message(
        chat_id=ADMIN,
        message_id=callback.message.message_id
    )
    current_user_id = 0


@dp.callback_query_handler(lambda callback: callback.data == 'send_message_to_users')
async def send_message_to_users(callback: types.CallbackQuery) -> None:
    await callback.answer('Введите текст сообщения')
    await ProfileStatesGroup.get_msg_for_users.set()
    await bot.send_message(
        chat_id=ADMIN, text='Введите текст сообщения'
    )


@dp.message_handler(state=ProfileStatesGroup.get_msg_for_users)
async def get_msg_text(message: types.Message, state: FSMContext) -> None:
    await state.finish()

    db = Database()
    users_chat_id = db.get_all_table_elements(
        query="SELECT chat_id FROM subscribers;", element='chat_id'
    )
    for user in users_chat_id:
        try:
            await bot.send_message(chat_id=int(user), text=message.text)
        except ChatNotFound:
            username = db.get_one_data_cell(
                f"SELECT nickname FROM subscribers WHERE chat_id = '{user}';"
            )
            await message.answer(
                f'@{username} не создал чат с ботом'
            )
    await message.answer('✅Сообщения отправлены')


@dp.callback_query_handler(lambda callback: callback.data == 'unknown_user')
async def unknown_user(callback: types.CallbackQuery) -> None:
    global current_user_id
    current_user_id = 0

    await callback.answer("Пользователь игнорирован")
    await bot.delete_message(
        chat_id=ADMIN,
        message_id=callback.message.message_id
    )
