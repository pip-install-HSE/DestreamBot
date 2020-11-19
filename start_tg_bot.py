import os

from aiogram import executor
from tortoise import Tortoise

from tg_bot.load_all import bot, loop, DONATION_CHECK_DELAY, connection, channel
from tg_bot.modules.repeat import repeat, check_new_donations


async def on_shutdown(dp):
    await bot.close()
    await dp.storage.close()
    await dp.storage.wait_closed()
    await Tortoise.close_connections()


async def on_startup(dp):
    await bot.send_message("446162145", "Bot is running!")
    await bot.send_message("385778185", "Bot is running!")
    loop.call_later(DONATION_CHECK_DELAY, repeat, check_new_donations, loop)


from tg_bot.dialogs.users.handlers import dp
from tg_bot.dialogs.admin.handlers import dp
executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup, skip_updates=True)
