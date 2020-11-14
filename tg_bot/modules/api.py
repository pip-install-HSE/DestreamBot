import json
import aiohttp
from ..load_all import loop


class BadResponseStatus(Exception):
    def __init__(self, status):
        self.status = status


class Methods:
    def __init__(self, key):
        self.key = key
        self.headers = {"X-API-KEY": key}
        self.common_url = "https://exp.destream.net/api/v1/telegram-bot/"


class MethodsGET(Methods):
    def __init__(self, key):
        super().__init__(key)

    async def get(self, url: str, headers: dict = None, **kwargs) -> dict:
        self.headers.update(headers if headers else {})
        async with aiohttp.ClientSession(loop=loop) as client:
            async with client.get(url, headers=self.headers, **kwargs) as response:
                if response.status == 200:
                    return json.loads((await response.read()).decode("utf-8"))
                else:
                    raise BadResponseStatus(response.status)

    async def user(self):
        url = self.common_url + "user"
        return await self.get(url)


class MethodsPOST(Methods):
    def __init__(self, key):
        super().__init__(key)

    async def post(self, url: str, headers: dict = None, **kwargs) -> dict:
        self.headers.update(headers if headers else {})
        async with aiohttp.ClientSession(loop=loop) as client:
            async with client.post(url, headers=self.headers, **kwargs) as response:
                if response.status == 200:
                    return json.loads((await response.read()).decode("utf-8"))
                else:
                    raise BadResponseStatus(response.status)

    async def donation(self, currency: str, amount: [int, float], message: str = "",
                       additional_parameters: dict = None):
        additional_parameters = dict() if additional_parameters is None else additional_parameters
        url = self.common_url + "donation"
        headers = {"Content-type": "application/json", "Accept": "application/json"}
        body = {
            "currency": currency,
            "amount": amount,
            "message": message,
            "additionalParameters": additional_parameters
        }
        await self.post(url=url, headers=headers, json=body)


class API:
    def __init__(self, key: str):
        self.get = MethodsGET(key)
        self.post = MethodsPOST(key)
