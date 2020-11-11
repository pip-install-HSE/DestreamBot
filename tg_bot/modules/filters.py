from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, CallbackQuery
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
    def __init__(self):
        pass

    async def check(self, message: Message) -> bool:
        flag = False
        print(bot.id)
        if members := message.__getattribute__("new_chat_members"):
            for member in members:
                flag = True if member.id == bot.id else flag
            print(members)
        return flag
