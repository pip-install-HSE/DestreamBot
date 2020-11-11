import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.deep_linking import get_start_link, decode_payload
from aiogram.dispatcher.filters import CommandStart

from ...db.models import BotUser, Group
from ...load_all import dp, bot
from . import texts, keyboards
from ...modules.filters import Button, IsBotNewChatMember

import sys
import asyncio
import aiohttp
import json
import datetime


class States(StatesGroup):
    token = State()
    add_group = State()
    notifications = State()


@dp.message_handler(CommandStart(deep_link=""), state="*")
async def bot_user_start(message: types.Message):
    await States.token.set()
    await message.answer(texts.bot_user_start(), reply_markup=keyboards.bot_user_start())


@dp.message_handler(state=States.token)
async def token(message: types.Message, state: FSMContext, bot_user: BotUser):
    url = "https://exp.destream.net/api/v1/telegram-bot/user"
    headers = {"X-API-KEY": message.text}
    loop = asyncio.get_running_loop()
    async with aiohttp.ClientSession(loop=loop) as client:
        async with client.get(url, headers=headers) as response:
            if response.status == 200:
                bot_user.token = message.text
                data = await response.read()
                json_data = json.loads(data.decode('utf-8'))
                await message.answer(texts.main_menu(json_data),
                                     reply_markup=keyboards.main_menu())
                await bot_user.save()
                await state.reset_state(with_data=False)
            else:
                await message.answer(texts.error_token())


@dp.callback_query_handler(Button("add_group"), state="*")
async def add_group(callback: types.CallbackQuery, state: FSMContext):
    message = callback.message
    await message.answer(texts.add_group())
    await States.add_group.set()
    await callback.answer()


@dp.message_handler(IsBotNewChatMember(), content_types=types.ContentTypes.NEW_CHAT_MEMBERS, state="*")
# content_types=types.ContentTypes.NEW_CHAT_MEMBERS,
async def new_chat_member(message: types.Message, state: FSMContext, bot_user: BotUser):
    # await States.notifications.set()
    admin_id = message.from_user.id
    await state.storage.set_state(user=admin_id, state=States.notifications.state)
    await bot.send_message(chat_id=admin_id, text=texts.notifications()
                           , reply_markup=keyboards.notifications())
    await Group.get_or_create(tg_id=message.chat.id, admin=bot_user)
    # await message.answer(texts.notifications(), reply_markup=keyboards.notifications())
    # await Group


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


@dp.callback_query_handler(Button("my_group"))
async def my_group(callback: types.CallbackQuery):
    message = callback.message
    await message.answer(texts.my_group())


@dp.message_handler(state="*")
async def any_message(message: types.Message):
    await message.answer(texts.any_message())
# @dp.callback_query_handler(Button("add_group"), state="*"):
# await state.reset_state(with_data=False)
