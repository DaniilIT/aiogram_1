from unittest.mock import AsyncMock

import pytest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from handlers import call_start_handler, command_start_handler
from structures import keyboards
from tests.utils import TEST_CHAT, TEST_USER


@pytest.mark.asyncio
async def test_start_handler():
    message = AsyncMock()
    await command_start_handler(message)

    message.answer.assert_called_with(
        'Меню',
        reply_markup=keyboards.MENU_BOARD
    )


@pytest.mark.asyncio
async def test_start_callback_handler(memory_storage, bot):
    call = AsyncMock()
    state = FSMContext(
        # bot=bot,
        storage=memory_storage,
        key=StorageKey(bot_id=bot.id, user_id=TEST_USER.id, chat_id=TEST_CHAT.id)
    )

    await call_start_handler(call=call, state=state)

    assert await state.get_state() is None
    call.message.delete.assert_any_call()
    call.message.answer.assert_called_with(
        'Меню',
        reply_markup=keyboards.MENU_BOARD
    )
