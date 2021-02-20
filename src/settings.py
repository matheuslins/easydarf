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
        )
    }
}
