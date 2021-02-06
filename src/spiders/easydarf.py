from src.settings import SPIDERS_SETTINGS
from src.core.spiders.easydarf import EasyDarfBusiness
from src.core.logging import log
from src.spiders.interfaces.spider import BaseSpider


class EasyDarfSpider(BaseSpider, EasyDarfBusiness):

    spider_name = 'easydarf'
    start_url = SPIDERS_SETTINGS["easydarf"]["START_URL"]

    def __init__(self, *args, **kwargs):
        super(EasyDarfSpider, self).__init__(*args, **kwargs)
        self.set_login_params()

    def get_start_url(self):
        return self.start_url

    async def get(self):
        return await self.run()

    def set_login_params(self):
        self.login_params = {
            "username": SPIDERS_SETTINGS["easydarf"]["USERNAME"],
            "password": SPIDERS_SETTINGS["easydarf"]["PASSWORD"],
            "captcha": True
        }

    async def start_consult(self, response):
        log.info(msg=f"{self.spider_name} - Start consult spider")
        log.info(msg=f"{self.spider_name} - Spider with login")
        await self.start_login(self.response)
        await self.make_login()

    async def start_extract(self):
        await self.consult_stores()
        await self.extract_data()
        self.save_item(file_name="instacart_items.json")
        log.info(msg=f"{self.spider_name} - Saved all items!")

    def save_item(self, file_name):
        pass
