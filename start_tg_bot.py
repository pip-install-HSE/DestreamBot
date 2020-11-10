import os

from aiogram import executor
from tortoise import Tortoise

from tg_bot.load_all import bot
from tg_bot.db.models import BotUser


async def on_shutdown(dp):
    await bot.close()
    await dp.storage.close()
    await dp.storage.wait_closed()
    await Tortoise.close_connections()


async def on_startup(dp):
    admin = BotUser.create(tg_id=446162145, token="ahshhsfa")
    await bot.send_message(admin.tg_id, admin.token)



from tg_bot.dialogs.users.handlers import dp
from tg_bot.dialogs.admin.handlers import dp
executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=None, skip_updates=True)
