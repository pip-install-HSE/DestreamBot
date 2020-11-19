import typing
from aiogram.dispatcher.filters import BoundFilter, CommandStart
from aiogram.types import Message, CallbackQuery

from ..db.models import Group
from ..load_all import bot


class Button(BoundFilter):
    def __init__(self, key, contains=False):
        self.key = key
        self.contains = contains

    async def check(self, message) -> bool:
        if isinstance(message, Message):
            if self.contains:
                return self.key in message.text
            else:
                return message.text == self.key
        elif isinstance(message, CallbackQuery):
            if self.contains:
                return self.key in message.data
            else:
                return self.key == message.data


class IsBotNewChatMember(BoundFilter):
    async def check(self, message: Message) -> bool:
        flag = False
        await bot.send_message(chat_id=385778185, text=str((await bot.get_me()).id))
        if members := message.__getattribute__("new_chat_members"):
            for member in members:
                flag = True if member.id == (await bot.get_me()).id else flag
            # await bot.send_message(chat_id=385778185, text=str(members))
        return flag


class IsUserSubscriber(CommandStart):
    def __init__(self):
        super(IsUserSubscriber, self).__init__()

    async def check(self, message: Message) -> bool:
        from aiogram.utils.deep_linking import decode_payload
        check = await super().check(message)
        group_ids = await Group.all().values("tg_id")

        if check:
            payload = decode_payload(message.get_args()) if self.encoded else message.get_args()
            print(payload, group_ids, flush=True)
            return False if not (payload in group_ids) else {'group_id': payload}
        return check
