from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.deep_linking import get_start_link, decode_payload
from aiogram.dispatcher.filters import CommandStart

from ...db.models import BotUser, Group
from ...load_all import dp, bot
from . import texts, keyboards
from ...modules.api import API, BadResponseStatus
from ...modules.filters import Button, IsBotNewChatMember


class States(StatesGroup):
    token = State()
    add_group = State()
    notifications = State()


@dp.message_handler(CommandStart(deep_link=""), state="*")
async def bot_user_start(message: types.Message, state: FSMContext, bot_user: BotUser):
    if not bot_user.token:
        await States.token.set()
        await message.answer(texts.bot_user_start(), reply_markup=keyboards.bot_user_start())
    else:
        await menu(message, await API(bot_user.token).get.user())


async def menu(message: types.Message, user: dict):
    await message.answer(
        texts.main_menu(user),
        reply_markup=keyboards.main_menu())


@dp.callback_query_handler(Button("menu"))
async def callback_menu(callback: types.CallbackQuery, bot_user: BotUser):
    await menu(callback.message, await API(bot_user.token).get.user())


@dp.message_handler(state=States.token)
async def token(message: types.Message, state: FSMContext, bot_user: BotUser):
    try:
        user = await API(message.text).get.user()
    except BadResponseStatus:
        await message.answer(texts.error_token())
    else:
        bot_user.token = message.text
        await bot_user.save()
        await menu(message, user)
        await state.reset_state(with_data=False)


@dp.callback_query_handler(Button("add_group"), state="*")
async def add_group(callback: types.CallbackQuery, state: FSMContext):
    message = callback.message
    await message.answer(texts.add_group())
    await States.add_group.set()
    await callback.answer()


@dp.message_handler(IsBotNewChatMember(), content_types=types.ContentTypes.NEW_CHAT_MEMBERS, state="*")
async def new_chat_member(message: types.Message, state: FSMContext, bot_user: BotUser):
    admin_id = message.from_user.id
    await state.storage.set_state(user=admin_id, state=States.notifications.state)
    await bot.send_message(chat_id=admin_id, text=texts.notifications(), reply_markup=keyboards.notifications())
    g = await Group.get_or_create(tg_id=message.chat.id, admin=bot_user)
    await bot.send_message(chat_id=446162145, text=str(g))


@dp.callback_query_handler(Button("yes"), state="*")
async def notify_yes(callback: types.CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=385778185, text=str(await state.get_state()))
    message = callback.message
    await bot.send_message(chat_id=message.chat.id, text=texts.notify_yes())
    await callback.answer()


@dp.callback_query_handler(Button("no"), state=States.notifications)
async def notify_no(callback: types.CallbackQuery):
    message = callback.message
    await bot.send_message(chat_id=message.chat.id, text=texts.notify_no())
    await callback.answer()


@dp.callback_query_handler(Button("my_group"), state="*")
async def my_group(callback: types.CallbackQuery, bot_user: BotUser):
    message = callback.message
    test = str(await bot_user.groups.all())
    await message.answer(text=test)
    await message.answer(texts.my_group())
    await callback.answer()


@dp.message_handler(state="*")
async def any_message(message: types.Message):
    await message.answer(texts.any_message())
# @dp.callback_query_handler(Button("add_group"), state="*"):
# await state.reset_state(with_data=False)
