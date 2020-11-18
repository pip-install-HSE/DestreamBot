import asyncio
from ..config import DONATION_CHECK_DELAY
import pika
from pika.exceptions import ChannelClosedByBroker


async def check_new_donations():
    print("CHECKED", flush=True)
    try:
        pass
    except ChannelClosedByBroker:
        pass


def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(DONATION_CHECK_DELAY, repeat, coro, loop)
