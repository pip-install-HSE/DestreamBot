import logging
from tortoise import Tortoise
from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from .modules.languages_middelware import setup_middleware
from .modules.middlewares import GetUserMiddleware
from .config import *
from .modules.repeat import repeat, check_new_donations


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
loop.call_later(DONATION_CHECK_DELAY, repeat, check_new_donations, loop, bot)
# await Tortoise.generate_schemas()
