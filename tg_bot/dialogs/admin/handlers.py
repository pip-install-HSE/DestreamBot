from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.deep_linking import get_start_link, decode_payload
from aiogram.dispatcher.filters import CommandStart

from ...db.models import BotUser
from ...load_all import dp, bot
from . import texts, keyboards


class States(StatesGroup):
    token = State()


@dp.message_handler(CommandStart(deep_link=""), state="*")
async def bot_user_start(message: types.Message):
    await States.token.set()
    await message.answer(texts.bot_user_start(), reply_markup=keyboards.bot_user_start())


@dp.message_handler(state=States.token)
async def token(message: types.Message, state: FSMContext, bot_user: BotUser):
    await state.reset_state(with_data=False)
    # TODO: проверка на валидность токена желательно aiohttp
    bot_user.token = message.text
    await bot_user.save()
    await message.answer(texts.main_menu(), reply_markup=keyboards.main_menu())
