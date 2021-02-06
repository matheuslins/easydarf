
from aiohttp import web

from src.core.home.views import home


routes = [
    web.get('/', home)
]
