from aiogram.filters.callback_data import CallbackData


class TestCallBackData(CallbackData, prefix='test'):
    text: str
    user_id: int
