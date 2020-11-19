import logging

from aio_pika import connect
from tortoise import Tortoise
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from .modules.languages_middelware import setup_middleware
from .modules.middlewares import GetUserMiddleware
from .config import *


storage = RedisStorage2(host=REDIS_HOST)
bot = Bot(token=TG_TOKEN, parse_mode="HTML", loop=loop)
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.DEBUG)

dp.middleware.setup(LoggingMiddleware())
dp.middleware.setup(GetUserMiddleware())
i18n = setup_middleware(dp)
i18n.reload()

_ = i18n.gettext

loop.run_until_complete(Tortoise.init(config=TORTOISE_ORM))

# await Tortoise.generate_schemas()
rabbit_connection = await connect(
    host=RABBIT_HOST,
    port=int(RABBIT_PORT),
    virtualhost=RABBIT_VIRTUAL_HOST,
    login=RABBIT_USER,
    password=RABBIT_PASSWORD,
    loop=loop
)
rabbit_channel = await rabbit_connection.channel()
rabbit_donation_queue = await rabbit_channel.declare_queue(RABBIT_QUEUE, passive=True)
