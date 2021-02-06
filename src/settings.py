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
        'PASSWORD': config("PASSWORD")
    }
}
