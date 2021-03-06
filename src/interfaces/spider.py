import json
from abc import ABCMeta, abstractmethod
from aiohttp import web

from src.core.request import RequestHandler
from src.core.logging import log


class BaseSpider(web.View, metaclass=ABCMeta):

    response = None
    spider_name = None
    start_url = None
    data = {}
    req_data = {}

    @abstractmethod
    def get_start_url(self):
        raise NotImplementedError

    @abstractmethod
    async def start_consult(self, response):
        raise NotImplementedError

    @abstractmethod
    async def start_extract(self):
        raise NotImplementedError

    @abstractmethod
    def save_item(self, *args, **kwargs):
        raise NotImplementedError

    async def request_initial_page(self):
        log.info(msg=f"{self.spider_name} - Initial page request")
        request_handler = RequestHandler()
        self.response = await request_handler.session(
            url=self.get_start_url()
        )
        log.info(msg=f"{self.spider_name} - Got initial page text")

    async def run(self):
        await self.request_initial_page()
        await self.start_consult(self.response)
        await self.start_extract()
        status = self.data.pop('status')
        return web.json_response(
            data={
                'spider': f"{self.spider_name}",
                **self.data
            },
            status=status
        )

    async def error(self, status):
        return web.json_response(
            data={
                'spider': f"{self.spider_name}",
                **self.data
            },
            status=status
        )
