import asyncio
import pika
import json
import logging

from aio_pika import IncomingMessage

from ..config import DONATION_CHECK_DELAY, RABBIT_CONNECTION_PARAMS
from ..load_all import bot, dp
from ..db.models import BotUser, Group
from ..dialogs.admin import texts


async def process_donation(message: IncomingMessage):
    don = json.loads(message.body.decode("utf-8"))
    try:
        logging.info("NEW DONATION, trying to identify who is it.")
        user = BotUser.get(tg_id=don["additionalParameters"]["usr_tg_id"])
        group = Group.get(tg_id=don["additionalParameters"]["group_id"])
    except KeyError:
        logging.info("Not successful.")
    else:
        if user and group:
            logging.info("Sending messages to admin.")
            await bot.send_message(chat_id=don["additionalParameters"]["usr_tg_id"],
                                   text=texts.new_donation(don))
            if group.is_report_donations:
                logging.info("Sending messages to group.")
                await bot.send_message(chat_id=don["additionalParameters"]["group_id"],
                                       text=texts.new_donation(don))
