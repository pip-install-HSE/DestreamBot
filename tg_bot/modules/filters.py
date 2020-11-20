import typing
from aiogram.dispatcher.filters import BoundFilter, CommandStart
from aiogram.types import Message, CallbackQuery

from ..db.models import Group
from ..load_all import bot


class Button(BoundFilter):
    def __init__(self, key, contains=False, work_in_group=False):
        self.key = key
        self.contains = contains
        self.work_in_group = work_in_group

    async def check(self, message: Message) -> bool:
        # if not self.work_in_group:
        #     res = await isItNotGroup(message)
        #     if not res:
        #         return False

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
        group_ids = [str(d['tg_id']) for d in await Group.all().values("tg_id")]

        if check:
            payload = str(decode_payload(message.get_args()))
            print(payload, group_ids, type(payload), flush=True)
            return False if not (payload in group_ids) else {'group_id': payload}
        return check


class IsItNotGroup(BoundFilter):

    async def check(self, message_or_call: [Message, CallbackQuery]) -> bool:
        res = await isItNotGroup(message_or_call)
        return res


async def isItNotGroup(message_or_call: [Message, CallbackQuery]) -> bool:
    if isinstance(message_or_call, Message):
        return message_or_call.chat.id == message_or_call.from_user.id
    elif isinstance(message_or_call, CallbackQuery):
        return message_or_call.message.chat.id == message_or_call.message.from_user.id
