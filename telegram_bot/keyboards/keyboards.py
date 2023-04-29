from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


admin_main_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                '➕➕Добавить список рассылки➕➕', callback_data='add_mail_list'
            )
        ],
        [
            InlineKeyboardButton(
                '👀Посмотреть списки рассылки', callback_data='view_mail_lists'
            )
        ],
        [
            InlineKeyboardButton(
                '👀Посмотреть юзеров и их подписки', callback_data='view_users'
            )
        ],
        [
            InlineKeyboardButton(
                '❌❌Удалить список рассылки❌❌', callback_data='remove_mail_list'
            )
        ],
        [
            InlineKeyboardButton(
                '➡️➡️Послать ручной сигнал юзерам➡️➡️', callback_data='send_handmade_signal'
            )
        ]
    ]
)

add_to_mail_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                'Добавить в списки рассылки', callback_data='add_into_mail_lists'
            )
        ],
        [
            InlineKeyboardButton(
                'Неизвестный юзер', callback_data="unknown_user"
            )
        ]
    ]
)

users_work_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                'Выбрать пользователя', callback_data='select_user'
            )
        ],
        [
            InlineKeyboardButton(
                '➕➕Добавить пользователя➕➕', callback_data='add_user_in_db'
            )
        ],
        [   
            InlineKeyboardButton(
                '📩📩Отправить сообщение пользователям📩📩', callback_data='send_message_to_users'
            )
        ]
    ]
)

users_actions_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                '➕➕Добавить подписки пользователю➕➕', callback_data='add_mail_lists'
            )
        ],
        [
            InlineKeyboardButton(
                '❌❌Удалить подписки у пользователя❌❌', callback_data='remove_user_subscribes'
            )
        ],
        [
            InlineKeyboardButton(
                '❌❌Удалить пользователя❌❌', callback_data='remove_user'
            )
        ],
    ]
)

def get_mail_lists_kb(mail_lists: list[str],
                      stop: str = 'cancel') -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton(list_)] for list_ in mail_lists]
    keyboard.append([KeyboardButton(stop)])
    keyboard.append([KeyboardButton('заново')])
    
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=keyboard
    )
    return kb