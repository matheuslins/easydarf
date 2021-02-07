from src.spiders.interfaces.spider_login import SpiderLoginInterface
from src.utils.extract import extract_ecac_code, extract_imposto_renda_url


class EasyDarfBusiness(SpiderLoginInterface):

    context = {}

    async def go_to_dashboard(self):
        response = self.session(
            url='https://cav.receita.fazenda.gov.br/ecac',
            cookies=self.context['pos_login_cookies']
        )
        self.context['ecac_code'] = extract_ecac_code(response)
        await self.go_to_components()

    async def go_to_components(self):
        response = self.session(
            url=(
                f'https://cav.receita.fazenda.gov.br/ecac/'
                f'componentes.aspx/{self.context["ecac_code"]}/destaques.html'
            ),
            cookies=self.context['pos_login_cookies']
        )
        self.context['imposto_renda_url'] = extract_imposto_renda_url(response)

    async def go_to_extrato_dirpf(self):
        response = self.session(
            url=self.context['imposto_renda_url'],
            headers={
                'Host': 'www3.cav.receita.fazenda.gov.br',
                'Referer': 'https://cav.receita.fazenda.gov.br/ecac/'
            },
            cookies={
                'infoMultiAcesso': 'true',
                'COOKIECAV': self.context['pos_login_cookies']['COOKIECAV']
            }
        )
        print(response)
