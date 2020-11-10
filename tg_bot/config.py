import os
from dotenv import load_dotenv
from gino import Gino

load_dotenv()
envs = os.environ

TG_TOKEN = envs.get("TG_TOKEN")
REDIS_HOST = envs.get('REDIS_HOST')
db = Gino()
