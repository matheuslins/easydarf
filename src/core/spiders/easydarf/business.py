from src.spiders.interfaces.spider_login import SpiderLoginInterface
from src.utils.extract import extract_ecac_code, extract_imposto_renda_url
from src.core.spiders.easydarf.carne_leao import EasyDarfCarneLeao
from src.settings import SPIDERS_SETTINGS


class EasyDarfBusiness(SpiderLoginInterface, EasyDarfCarneLeao):

    async def go_to_dashboard(self):
        response = await self.session(
            url=SPIDERS_SETTINGS['easydarf']['ECAC_URL'],
            cookies=self.context['pos_login_cookies']
        )
        self.context['ecac_code'] = extract_ecac_code(response)
        await self.go_to_components()

    async def go_to_components(self):
        response = await self.session(
            url=(
                f'{SPIDERS_SETTINGS["easydarf"]["ECAC_URL"]}'
                f'componentes.aspx/{self.context["ecac_code"]}/destaques.html'
            ),
            cookies=self.context['pos_login_cookies']
        )
        self.context['imposto_renda_url'] = extract_imposto_renda_url(response)
        await self.go_to_extrato_dirpf()

    async def go_to_extrato_dirpf(self):
        _ = await self.session(
            url=self.context['imposto_renda_url'],
            headers={
                'Host': 'www3.cav.receita.fazenda.gov.br',
                'Referer': SPIDERS_SETTINGS["easydarf"]["ECAC_URL"]
            },
            cookies={
                'infoMultiAcesso': 'true',
                'COOKIECAV': self.context['pos_login_cookies']['COOKIECAV']
            }
        )
        await self.go_to_api_init()

    async def go_to_api_init(self):
        _ = await self.session(
            url=SPIDERS_SETTINGS['easydarf']['API_INIT_URL'],
            headers={
                'Host': 'www3.cav.receita.fazenda.gov.br',
                'Referer': (
                    'https://www3.cav.receita.fazenda.gov.br/extratodirpf/'
                )
            },
            cookies={
                'infoMultiAcesso': 'true',
                'COOKIECAV': self.context['pos_login_cookies']['COOKIECAV']
            }

        )
        self.context['user_tokens'] = await self.get_response.json()
