import pytz
from datetime import datetime, timedelta
from base64 import b64encode

from src.core.request import RequestHandler
from src.utils.extract import extract_current_year, extract_user_data
from src.core.logging import log


class EasyDarfCarneLeao(RequestHandler):

    async def go_to_carne_leao(self):
        _ = await self.session(
            url='https://www3.cav.receita.fazenda.gov.br/carneleao/',
            headers={
                'Host': 'www3.cav.receita.fazenda.gov.br',
                'Referer': (
                    'https://www3.cav.receita.fazenda.gov.br/extratodirpf/'
                )
            },
            cookies={
                'COOKIECAV': self.context['pos_login_cookies']['COOKIECAV']
            }
        )
        await self.got_to_demonstrativo()

    async def got_to_demonstrativo(self):
        response = await self.session(
            url=(
                'https://www3.cav.receita.fazenda.gov.br/'
                'carneleao/api/demonstrativo/auth'
            ),
            method="POST",
            headers={
                'Host': 'www3.cav.receita.fazenda.gov.br',
                'Referer': (
                    'https://www3.cav.receita.fazenda.gov.br/carneleao/login'
                ),
                'Origin': 'https://www3.cav.receita.fazenda.gov.br',
                'Content-Type': 'application/json',
                'Accept': 'application/json, text/plain, */*'
            },
            cookies={
                'COOKIECAV': self.context['pos_login_cookies']['COOKIECAV']
            },
            data="{\"cpf\":\"00000000000\"}"
        )

        self.context['authorization'] = self.get_response.headers.get(
            'authorization'
        )
        self.context['user_data'] = extract_user_data(response)

        await self.go_to_carne_leao_login()

    async def go_to_carne_leao_login(self):
        response = await self.session(
            url=(
                'https://www3.cav.receita.fazenda.gov.br/carneleao/'
                'api/demonstrativo/anoCalendario'
            ),
            headers={
                'Authorization': self.context['authorization']
            },
            cookies={
                'COOKIECAV': self.context['pos_login_cookies']['COOKIECAV']
            }
        )
        self.context['current_year'] = extract_current_year(response)

        await self.go_to_user_id(1)

    async def go_to_user_id(self, range_times):
        for _ in range(range_times):
            _ = await self.session(
                url=(
                    f'https://www3.cav.receita.fazenda.gov.br/carneleao/api/'
                    f'demonstrativo/configuracaoIdentificacao/'
                    f'{self.context["current_year"]}'
                ),
                headers={
                    'Authorization': self.context['authorization']
                },
                cookies={
                    'COOKIECAV': self.context['pos_login_cookies']['COOKIECAV']
                }
            )
            self.context['user_data'].update(**await self.get_response.json())

    async def create_new_yield(self):
        yield_created = {}
        now = (
                datetime.now() + timedelta(hours=3)
        ).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        amount = 100

        data = (
            '{{"dataLancamento":"{now}","codigoOcupacao":"",'
            '"codigoNatureza":"01.004.001","origemRecebimento":'
            '"EXTERIOR","historico":"","tipoRendimento":"OUTROS_RENDIMENTOS",'
            '"valorDeducao":0,"valorCheio":0,"valor":{amount},'
            '"descricaoOcupacao":"","descricaoOcupacaoResumida":"",'
            '"descricaoNatureza":"Outros"}}'
        ).format(now=now, amount=amount)

        _ = await self.session(
            url=(
                f'https://www3.cav.receita.fazenda.gov.br/carneleao/'
                f'api/demonstrativo/rendimento/'
                f'{self.context["user_data"]["id"]}'
            ),
            method='POST',
            headers={
                'Host': 'www3.cav.receita.fazenda.gov.br',
                'Authorization': self.context['authorization'],
                'Origin': 'https://www3.cav.receita.fazenda.gov.br',
                'Content-Type': 'application/json',
                'Referer': (
                    'https://www3.cav.receita.fazenda.gov.br/'
                    'carneleao/rendimentos/rendimento'
                )
            },
            cookies={
                'COOKIECAV': self.context['pos_login_cookies']['COOKIECAV']
            },
            data=data
        )

        if self.get_response.status == 200:
            log.info(msg='New yield created!')
            yield_created.update({
                'created_at': now,
                'amount': amount
            })

        return await self.generate_new_darf(yield_created)

    async def generate_new_darf(self, yield_created):
        month = '0'
        current_month = datetime.now(
            tz=pytz.timezone('America/Sao_Paulo')
        ).month
        mes_index = month if month else (current_month - 1)

        _ = await self.session(
            url=(
                f'https://www3.cav.receita.fazenda.gov.br/carneleao/'
                f'api/demonstrativo/darf/{self.context["current_year"]}'
            ),
            method="POST",
            headers={
                'Host': 'www3.cav.receita.fazenda.gov.br',
                'Authorization': self.context['authorization'],
                'Origin': 'https://www3.cav.receita.fazenda.gov.br',
                'Content-Type': 'application/json',
                'Referer': (
                    'https://www3.cav.receita.fazenda.gov.br/'
                    'carneleao/rendimentos/rendimento'
                )
            },
            cookies={
                'COOKIECAV': self.context['pos_login_cookies']['COOKIECAV']
            },
            data=f"{{\"mesIndex\":{mes_index}}}"
        )
        response = await self.get_response.json()
        pdf = response['pdf']
        yield_created.update({'pdf': pdf})
        return yield_created
