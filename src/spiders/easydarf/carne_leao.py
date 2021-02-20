from http import HTTPStatus

from src.core.request import RequestHandler
from src.utils.extract import extract_current_year, extract_user_data
from src.core.logging import log
from src.utils.datetime import now_datetime


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

    async def create_new_income(self, data) -> dict:
        now, now_str = now_datetime()
        amount = data['amount']
        data = (
            '{{"dataLancamento":"{now}","codigoOcupacao":"",'
            '"codigoNatureza":"01.004.001","origemRecebimento":'
            '"EXTERIOR","historico":"","tipoRendimento":"OUTROS_RENDIMENTOS",'
            '"valorDeducao":0,"valorCheio":0,"valor":{amount},'
            '"descricaoOcupacao":"","descricaoOcupacaoResumida":"",'
            '"descricaoNatureza":"Outros"}}'
        ).format(now=now_str, amount=amount)

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
            log.info(msg='New income created!')
            return {
                'created_at': now_str,
                'status': HTTPStatus.CREATED,
                'message': 'Income created successfully',
                'data': {
                    'amount': amount
                }
            }

        return {
            'created_at': None,
            'status': HTTPStatus.BAD_REQUEST,
            'message': 'Cannot create income',
            'data': {}
        }

    async def generate_new_darf(self):
        now, now_str = now_datetime()
        month = '0'
        current_month = now.month
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
        response = self.get_response
        if response.status == 400:
            return {
                'created_at': None,
                'status': HTTPStatus.BAD_REQUEST,
                'message': 'Darf indisponível',
                'data': {}
            }

        json_response = await response.json()
        return {
            'created_at': now_str,
            'status': HTTPStatus.CREATED,
            'message': 'Darf baixada com sucesso',
            'data': {
                'pdf': json_response['pdf']
            }
        }
