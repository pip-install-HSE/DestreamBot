from ...db.models import BotUser
from ...load_all import dp, bot
from aiogram import types


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    token = BotUser.get(tg_id=message.chat.id)
    await message.answer(f"Ну привет!\n\nВот той токен: {token}")
