import json
from re import search

from scrapy import Selector


def extract_set_cookies(response, keys: list) -> dict:
    headers = str(response.headers)
    return {
        key: search(fr'(?<={key}=)(.*?);', headers).group(1)
        for key in keys
    }


def extract_ecac_code(response) -> str:
    return search(r"(?<=ECAC\.Default\.iniciar\(\')(.*?)\'", response).group(1)


def extract_imposto_renda_url(response) -> str:
    selector = Selector(text=response)
    return selector.xpath(
        '//ul[@class="lista-destaque"]//li//a/@href'
    ).extract_first()


def extract_current_year(response) -> str:
    return search(r'(\d+)', response).group(1)


def extract_user_data(response) -> dict:
    return json.loads(response)
