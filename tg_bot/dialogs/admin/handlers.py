import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.deep_linking import get_start_link, decode_payload
from aiogram.dispatcher.filters import CommandStart

from ...db.models import BotUser
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
                await message.answer(texts.main_menu(bot_user.token),
                                     reply_markup=keyboards.main_menu())
                bot_user.token = message.text
                await bot_user.save()
                await state.reset_state(with_data=False)
            else:
                await message.answer(texts.error_token())


@dp.callback_query_handler(Button("add_group"), state="*")
async def add_group(callback: types.CallbackQuery, state: FSMContext):
    message = callback.message
    await message.answer(texts.add_group())
    await States.add_group.set()


@dp.message_handler(IsBotNewChatMember(), state=States.add_group)
# content_types=types.ContentTypes.NEW_CHAT_MEMBERS,
async def new_chat_member(message: types.Message, state: FSMContext):
    await States.notifications.set()
    await message.answer(texts.notifications(), reply_markup=keyboards.notifications())

# @dp.callback_query_handler(Button("add_group"), state="*"):
# await state.reset_state(with_data=False)
