from twocaptcha import TwoCaptcha
from scrapy import Selector

from src.core.request import RequestHandler
from src.core.captcha import CaptchaHandler
from src.core.logging import log
from src.settings import SPIDERS_SETTINGS, CAPTCHA
from src.utils.format import format_cpf
from src.utils.extract import extract_set_cookies


class SpiderLoginInterface(RequestHandler):

    login_params = {}
    login_data = {}

    async def init_login(self, login_url):
        _ = await self.session(url=login_url, allow_redirects=False)
        response = self.get_response
        self.login_data['login_cookies'] = extract_set_cookies(
            self.get_response, ['Session_Gov_Br_Prod', 'INGRESSCOOKIE']
        )
        self.login_data['location'] = response.headers.get('location')

    def format_username_data(self):
        cpf = format_cpf(SPIDERS_SETTINGS["easydarf"]["USERNAME"])
        return {
            "_csrf": self.login_data['_csrf'],
            "accountId": cpf,
            "action": "enterAccountId"
        }

    def format_password_data(self):
        cpf = format_cpf(SPIDERS_SETTINGS["easydarf"]["USERNAME"])
        return {
            '_csrf': self.login_data['_csrf'],
            'accountId': cpf,
            'password': SPIDERS_SETTINGS['easydarf']['PASSWORD'],
            'g-recaptcha-response': self.login_params["captcha"],
            'action': 'enterPassword'
        }

    @staticmethod
    def extract_site_key(response):
        selector = Selector(text=response)
        return selector.xpath(
            '//div[@id="login-password"]//'
            'button[@id="submit-button"]/@data-sitekey'
        ).extract_first()

    async def login_username(self):
        response = await self.session(
            url=self.login_data['init_url'],
            method="POST",
            headers={
                'content-type': 'application/x-www-form-urlencoded',
            },
            cookies=self.login_data['login_cookies'],
            data=self.format_username_data()
        )
        self.login_data['site_key_captcha'] = self.extract_site_key(response)
        self.login_data['captcha_url'] = str(self.login_data['init_url'])

    async def login_password(self, init_url):
        _ = await self.session(
            url=init_url,
            method="POST",
            headers={
                'content-type': 'application/x-www-form-urlencoded',
            },
            cookies=self.login_data['login_cookies'],
            data=self.format_password_data(),
            allow_redirects=False
        )
        self.login_data['location'] = self.get_response.headers.get('location')

    async def follow_redirect(self):
        response = await self.session(
            url=self.login_data['location'],
            cookies=self.login_data['login_cookies']
        )
        selector = Selector(text=response)
        self.login_data['_csrf'] = selector.xpath(
            '//form[@id="loginData"]//input[@name="_csrf"]/@value'
        ).extract_first()
        return self.get_response

    async def authorize(self):
        _ = await self.session(
            url=self.login_data['location'],
            cookies=self.login_data['login_cookies'],
            allow_redirects=False
        )
        self.login_data['location'] = self.get_response.headers.get('location')

    async def auth_login(self):
        _ = await self.session(
            url=self.login_data['location'],
            allow_redirects=False
        )
        self.context['pos_login_cookies'] = extract_set_cookies(
            self.get_response, ['ASP.NET_SessionId', 'COOKIECAV']
        )

    async def start_login(self, response):
        selector = Selector(text=response)
        login_url = selector.xpath(
            '//form[@id="frmLoginCert"]//a/@href'
        ).extract_first()

        await self.init_login(login_url)
        init_response = await self.follow_redirect()
        self.login_data['init_url'] = init_response.url
        await self.login_username()

    async def make_login(self):
        log.info(msg="Spider captcha detected")
        two_captcha = TwoCaptcha(**{
            'apiKey': CAPTCHA['2CAPTCHA_API_KEY'],
            'defaultTimeout': 60,
            'recaptchaTimeout': 200,
            'pollingInterval': 7
        })
        captcha_handler = CaptchaHandler(captcha_resolver=two_captcha)
        log.info(
            msg=f"Solving captcha - {self.login_data['site_key_captcha']}"
        )

        captcha_result = await captcha_handler.broker_captcha(
            site_key=self.login_data["site_key_captcha"],
            site_url=self.login_data['captcha_url']
        )
        log.info(msg=f"Captcha solved: {captcha_result}")
        self.login_params["captcha"] = captcha_result

        await self.login_password(self.login_data['init_url'])
        await self.authorize()
        await self.auth_login()
