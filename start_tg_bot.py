import json
from aiogram import executor
from tortoise import Tortoise

from tg_bot.load_all import bot, RABBIT_QUEUE, channel, loop
from tg_bot.modules.repeat import process_donation


async def on_shutdown(dp):
    await bot.close()
    await dp.storage.close()
    await dp.storage.wait_closed()
    await Tortoise.close_connections()


async def on_startup(dp):
    await bot.send_message("446162145", "Bot is running!")
    await bot.send_message("385778185", "Bot is running!")
    channel.queue_declare(queue=RABBIT_QUEUE, passive=True)

    def callback(ch, method, properties, body):
        loop.run_until_complete(process_donation(json.loads(body.decode("utf-8"))))
    channel.basic_consume(queue=RABBIT_QUEUE, on_message_callback=callback)
    channel.start_consuming()
    # loop.call_later(DONATION_CHECK_DELAY, repeat, check_new_donations, loop)


from tg_bot.dialogs.users.handlers import dp
from tg_bot.dialogs.admin.handlers import dp
executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup, skip_updates=True)
