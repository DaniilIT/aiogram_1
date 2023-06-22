from aiogram import types
from aiogram.fsm.context import FSMContext
from db import PRType
from db.post import create_post
from handlers.start import command_start_handler
from sqlalchemy.ext.asyncio import async_sessionmaker
from structures import keyboards
from structures.fsm_groups import PostStates


async def menu_posts_create(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(PostStates.waiting_for_text)
    await call.message.answer(
        'Пришли мне текст нового поста',
        reply_markup=keyboards.CANCEL_BOARD
    )


async def menu_posts_create_text(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.clear()
        return await command_start_handler(message)
    await state.update_data(post_text=message.text)
    await state.set_state(PostStates.waiting_for_url)
    await message.answer('Хорошо! Теперь отправь мне ссылку, которая будет под постом',
                         reply_markup=keyboards.CANCEL_BOARD)


async def menu_posts_create_url(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await state.clear()
        return await command_start_handler(message)
    if message.entities and (urls := [x for x in message.entities if x.type == 'url']):
        if len(urls) > 1:
            return await message.answer('отправь только одну ссылку')
        await state.update_data(post_url=urls[0].extract_from(message.text))
        await state.set_state(PostStates.waiting_for_pr_type)
        await message.answer('Теперь выбери вариант раскрутки поста',
                             reply_markup=keyboards.PRTYPE_BOARD)
    else:
        await message.answer('Ссылка не распознана( попробуй ещё раз',
                             reply_markup=keyboards.CANCEL_BOARD)


async def menu_posts_create_prtype(message: types.Message, state: FSMContext):
    match message.text:
        case 'Отмена':
            await state.clear()
            return await command_start_handler(message)
        case 'Оплата за одну публикацию':
            await state.update_data(pr_type=PRType.PUBLICATIONS.value)
            await state.set_state(PostStates.waiting_for_price_publication)
            return await message.answer('Отправь цену одной публикации (в EUR)')
        case 'Оплата за переход по ссылке':
            await state.update_data(pr_type=PRType.CLICKS.value)
            await state.set_state(PostStates.waiting_for_price_url)
            return await message.answer('Отправь цену одного перехода по ссылке (в EUR)')


async def menu_posts_create_prtype_url(message: types.Message, state: FSMContext, session_maker: async_sessionmaker):
    try:
        price = float(message.text)
        # assert price > 0
        # assert price <= 10
    except (TypeError, AssertionError):
        return await message.answer('Отправь цену в EUR. Цена должна быть больше, чем 0, но не больше 10 EUR.')
    data = await state.get_data()

    await create_post(
        session_maker=session_maker,
        text=data['post_text'],
        author_id=message.from_user.id,
        pr_type=PRType(data['pr_type']),
        url_price=price
    )

    # await create_url(session_maker, url_text=data['post_url'], post=post)

    await state.clear()
    await message.answer('Пост был успешно создан, теперь его можно рекламировать!')
    return await command_start_handler(message)


async def menu_posts_create_prtype_pub(message: types.Message, state: FSMContext):
    try:
        price = float(message.text)
    except ValueError:
        return await message.answer('Отправь цену в EUR')
    await state.update_data(price=price)
    await state.set_state(PostStates.waiting_for_post_subs_min)
    await message.answer('Укажи минимальное количество подписчиков, которое требуется для публикации поста')


async def menu_posts_create_subs_min(message: types.Message, state: FSMContext, session_maker: async_sessionmaker):
    try:
        subs_min = int(message.text)
    except TypeError:
        return await message.answer('Отправь число подписчиков')
    data = await state.get_data()
    post = await create_post(
        session_maker=session_maker,
        text=data['post_text'],
        pr_type=PRType(data['pr_type']),
        pub_price=data['price'],
        subs_min=subs_min,
        author_id=message.from_user.id,
        # url=data['post_url']
    )
    await state.clear()
    if post:
        await message.answer('Пост был успешно создан, теперь его можно рекламировать!')
    else:
        # TODO: add logs
        await message.answer('В ходе создания поста произошла ошибка. О ней сообщено администрации.')
    return await command_start_handler(message)
