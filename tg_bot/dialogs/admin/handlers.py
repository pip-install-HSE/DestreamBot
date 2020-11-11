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
    default = None


@dp.message_handler(CommandStart(deep_link=""), state="*")
async def bot_user_start(message: types.Message):
    await States.token.set()
    await message.answer(texts.bot_user_start, reply_markup=keyboards.bot_user_start)


@dp.message_handler(state=States.token)
async def token(message: types.Message, state: FSMContext):
    await state.storage.reset_state(user=message.chat.id)
    # TODO: проверка на валидность токена желательно aiohttp
