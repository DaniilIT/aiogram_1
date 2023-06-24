from datetime import datetime

from aiogram.types import CallbackQuery, Chat, Message, Update, User

TEST_USER = User(id=123, is_bot=False, first_name='Test', last_name='Bot',
                 username='testbot', language_code='ru-RU')

TEST_CHAT = Chat(id=12, type='private', username=TEST_USER.username,
                 first_name=TEST_USER.first_name, last_name=TEST_USER.last_name)


def get_message(text: str):
    return Message(message_id=42, date=datetime.now(), chat=TEST_CHAT, from_user=TEST_USER,
                   sender_chat=TEST_CHAT, text=text)


def get_update(message: Message = None, call: CallbackQuery = None):
    return Update(update_id=23, message=message, callback_query=call)
