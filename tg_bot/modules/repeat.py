import asyncio
from ..config import DONATION_CHECK_DELAY
import pika
from pika.exceptions import ChannelClosedByBroker
from ..load_all import bot


async def check_new_donations():
    try:
        pass
    except ChannelClosedByBroker:
        pass


def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(DONATION_CHECK_DELAY, repeat, coro, loop)
