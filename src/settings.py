from decouple import config


CAPTCHA = {
    "2CAPTCHA_API_KEY": config("2CAPTCHA_API_KEY")
}

SPIDERS_SETTINGS = {
    'easydarf': {
        'START_URL': (
            'https://cav.receita.fazenda.gov.br/autenticacao/login/index/11'
        ),
        'USERNAME': config("USERNAME"),
        'PASSWORD': config("PASSWORD"),
        'ECAC_URL': 'https://cav.receita.fazenda.gov.br/ecac/',
        'API_INIT_URL': (
            'https://www3.cav.receita.fazenda.gov.br/'
            'extratodirpf/api/appinit/ecac'
        ),
        'graphql': {

        }
    }
}

GRAPHQL = {
    'parametro': {
        'query': (
                "query ($exercicio: Int!, $tipoParametro: String!) "
                "{\n  parametro(exercicio: $exercicio, tipoParametro: "
                "$tipoParametro) {\n    conteudo\n    __typename\n  }\n}\n"
            ),
        'arg': {
            "tipoParametro": "ajuda"
        }
    },
    'dominio': {
        'query': (
            "query ($exercicio: Int!, $tipoDominio: String!) "
            "{\n  dominio(exercicio: $exercicio, tipoDominio: "
            "$tipoDominio) {\n    conteudo\n    __typename\n  }\n}\n"
        ),
        'arg': {
            "tipoDominio": "rendimentos"
        }
    }
}
