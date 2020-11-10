import os

from aiogram import executor
from .tgbot.load_all import bot
from .db.models import BotUser


async def on_shutdown(dp):
    await bot.close()
    await dp.storage.close()
    await dp.storage.wait_closed()


async def on_startup(dp):
    admins = BotUser.objects.filter(is_admin=True)
    for admin in admins:
        try:
            await bot.send_message(admin.tg_id, "Bot is running!")
        except:
            pass


class Command(BaseCommand):
    def handle(self, *args, **options):
        from .tgbot.dialogs.general.handlers import dp
        from .tgbot.dialogs.general.synchronization.handlers import dp
        from .tgbot.dialogs.contractor.handlers import dp
        from .tgbot.dialogs.customer.handlers import dp
        executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup, skip_updates=True)
