from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.dispatcher.filters import Text
from ...bot_config import dp, ADMIN



class _ProfileStatesGroup(StatesGroup):
    get_username = State()
    get_chat_id = State()
    get_mail_list_name = State()
    get_delete_mail_list = State()
    get_msg_for_users = State()
    get_mail_lists = State()
    get_user_id = State()
    get_adding_subscribes = State()
    get_removing_subscribes = State()
    get_signal_text = State()



@dp.message_handler(Text(equals='cancel'), state='*', user_id=ADMIN)
async def cmd_cancel(message: types.Message,
                     state: FSMContext) -> None:
    if state is None: pass
    else:
        await state.finish()
        await message.reply(
            'Вы прервали операцию', reply_markup=types.ReplyKeyboardRemove()
        )