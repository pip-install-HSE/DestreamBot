import asyncio
import json
from tg_bot.dialogs.admin.texts import main_menu

import aiohttp
loop = asyncio.get_event_loop()

async def test():
    url = "https://exp.destream.net/api/v1/telegram-bot/user"
    headers = {"X-API-KEY": "user1-secret-access-token"}

    async with aiohttp.ClientSession(loop=loop) as client:
        async with client.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.read()
                json_data = json.loads(data.decode('utf-8'))
                print(type(json_data))
                x = main_menu(json_data)
                print()
loop.run_until_complete(test())
# await test()