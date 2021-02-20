from src.settings import SPIDERS_SETTINGS
from src.spiders.easydarf.business import EasyDarfBusiness
from src.interfaces.spider import BaseSpider
from src.core.logging import log


class DarfSpider(BaseSpider, EasyDarfBusiness):

    spider_name = 'easydarf - darf'
    start_url = SPIDERS_SETTINGS["easydarf"]["START_URL"]

    def __init__(self, *args, **kwargs):
        super(DarfSpider, self).__init__(*args, **kwargs)
        self.set_login_params()

    async def post(self):
        return await self.run()

    def get_start_url(self):
        return self.start_url

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
        await self.go_to_dashboard()
        await self.go_to_carne_leao()
        self.data = await self.generate_new_darf()

    def save_item(self, file_name):
        pass
