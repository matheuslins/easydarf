from aiohttp import ClientSession

from src.core.logging import log


class RequestHandler:
    headers = {}
    cookies = {}
    context = {}
    __response = None

    def __init__(self, headers=None, cookies=None):
        self.headers = headers
        self.cookies = cookies

    @property
    def get_response(self):
        return self.__response

    async def session(self, **kwargs):
        async with ClientSession() as session:
            method = 'GET' if not kwargs.get('method') else kwargs['method']
            kwargs['method'] = method
            async with session.request(**kwargs) as resp:
                self.__response = resp
                log.debug(msg=resp)
                return await resp.text()

    @staticmethod
    async def make_raw_request(session, **kwargs):
        async with session.request(**kwargs) as resp:
            return resp
