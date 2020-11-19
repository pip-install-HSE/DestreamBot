import asyncio
import pika
import json
import logging
from ..config import DONATION_CHECK_DELAY, RABBIT_CONNECTION_PARAMS
from ..load_all import bot, dp
from ..db.models import BotUser, Group
from ..dialogs.admin import texts


async def check_new_donations():
    connection, channel = None, None
    for i in range(5):
        try:
            connection = pika.BlockingConnection(RABBIT_CONNECTION_PARAMS)
            channel = connection.channel()
        except:
            pass
        else:
            break
    if connection and channel:
        queue_from = 'telegram-donations'

        cnt = None
        while cnt is None:
            try:
                cnt = channel.queue_declare(queue=queue_from, passive=True).method.message_count
            except:
                pass
            else:
                if cnt:
                    last_msgs_c = (await dp.storage.get_data(chat="static_var")).get("telegram-donations@last_messages_count")
                    last_msgs_c = last_msgs_c if last_msgs_c else 0
                    for i in range(cnt - last_msgs_c):
                        don = json.loads(channel.basic_get(queue_from)[2].decode("utf-8"))
                        try:
                            logging.info("NEW DONATION, trying to identify who is it.")
                            user = BotUser.get(tg_id=don["additionalParameters"]["usr_tg_id"])
                            group = Group.get(tg_id=don["additionalParameters"]["group_id"])
                        except KeyError:
                            logging.info("Not successful.")
                            continue
                        else:
                            logging.info("Sending messages to admin and to group.")
                            if user and group:
                                await bot.send_message(chat_id=don["additionalParameters"]["usr_tg_id"],
                                                       text=texts.new_donation(don))
                                if group.is_report_donations:
                                    await bot.send_message(chat_id=don["additionalParameters"]["group_id"],
                                                           text=texts.new_donation(don))
                    await dp.storage.update_data(chat="static_var", data={"telegram-donations@last_messages_count": cnt})
        channel.close()
        connection.close()

# x = {
#  'currency': 'RUB', 'amount': 1100.0,
#  'message': 'ololo', 'receiver': 'user1',
#  'receiverId': '2222ccbe-aba4-4734-8cd6-fb8544afc3c0',
#  'sender': 'John Doe', 'additionalParameters': {'usr_id': '123456-loo', 'group_id': '44784'}
# }


def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(DONATION_CHECK_DELAY, repeat, coro, loop)
