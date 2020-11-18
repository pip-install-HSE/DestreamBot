import asyncio
from ..config import DONATION_CHECK_DELAY
from ..load_all import bot


async def check_new_donations():
    await bot.send_message("446162145", "Bot is running!")


def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(DONATION_CHECK_DELAY, repeat, coro, loop)
