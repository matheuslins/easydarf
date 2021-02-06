
from aiohttp import ClientSession


class RequestHandler:
    headers = {}
    cookies = {}

    def __init__(self, headers=None, cookies=None):
        self.headers = headers
        self.cookies = cookies

    @staticmethod
    async def make_session_request(**kwargs):
        async with ClientSession() as session:
            async with session.request(**kwargs) as resp:
                return await resp.text()

    @staticmethod
    async def make_raw_request(session, **kwargs):
        async with session.request(**kwargs) as resp:
            return resp
