import pytest
from aiogram import Bot, Dispatcher
from aiogram.methods import SendMessage
from structures import keyboards
from tests.utils import get_message, get_update


@pytest.mark.asyncio
async def test_start_command(dispatcher: Dispatcher, bot: Bot):
    result = await dispatcher.feed_update(bot=bot, update=get_update(message=get_message(text='/start')))
    assert isinstance(result, SendMessage)
    assert result.text == 'Меню'
    assert result.reply_markup == keyboards.MENU_BOARD
