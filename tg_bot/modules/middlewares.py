from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from tg_bot.db.models import BotUser


class GetUserMiddleware(BaseMiddleware):
    def __init__(self):
        super(GetUserMiddleware, self).__init__()

    async def on_pre_process_callback_query(self, callback_query: types.CallbackQuery, data: dict):
        data["bot_user"] = self.get_or_create_user(callback_query.message.chat.id)

    async def on_pre_process_message(self, message: types.Message, data: dict):
        data["bot_user"] = self.get_or_create_user(message.chat.id)

    async def get_or_create_user(self, tg_id):
        try:
            user, _ = await BotUser.get_or_create(tg_id=tg_id)
        except:
            return None
        else:
            return user
