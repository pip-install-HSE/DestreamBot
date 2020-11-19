import os
import asyncio
from pathlib import Path

import pika
from dotenv import load_dotenv

load_dotenv()
envs = os.environ

loop = asyncio.get_event_loop()

TG_TOKEN = envs.get("TG_TOKEN")
REDIS_HOST = envs.get("REDIS_HOST")

I18N_DOMAIN = "testbot"
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / "locales"

DATABASE = envs.get("DATABASE")
PG_DB = envs.get("POSTGRES_DB")
PG_USER = envs.get("POSTGRES_USER")
PG_PASS = envs.get("POSTGRES_PASSWORD")
PG_HOST = envs.get("POSTGRES_HOST")
PG_PORT = envs.get("POSTGRES_PORT")

TORTOISE_ORM = {
    "connections": {"default": f'{DATABASE}://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}'},
    "apps": {
        "models": {
            "models": ["tg_bot.db.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}

RABBIT_USER = envs.get("RABBIT_USER")
RABBIT_PASSWORD = envs.get("RABBIT_PASSWORD")
RABBIT_HOST = envs.get("RABBIT_HOST")
RABBIT_PORT = envs.get("RABBIT_PORT")
RABBIT_VIRTUAL_HOST = envs.get("RABBIT_VIRTUAL_HOST")

DONATION_CHECK_DELAY = 10

print(RABBIT_HOST, RABBIT_PORT, RABBIT_USER, RABBIT_PASSWORD, RABBIT_VIRTUAL_HOST, flush=True)
RABBIT_CONNECTION_CREDENTIALS = pika.PlainCredentials(RABBIT_USER, RABBIT_PASSWORD)
RABBIT_CONNECTION_PARAMS = pika.ConnectionParameters(host=RABBIT_HOST,
                                                     port=int(RABBIT_PORT),
                                                     virtual_host=RABBIT_VIRTUAL_HOST,
                                                     credentials=RABBIT_CONNECTION_CREDENTIALS,
                                                     socket_timeout=5)
