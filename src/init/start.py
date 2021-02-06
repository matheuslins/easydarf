from aiohttp import web

from src.init.routes import routes
from src.spiders.easydarf import EasyDarfSpider


def run():
    app = web.Application()
    app.add_routes(routes=routes)
    app.router.add_view("/darf", EasyDarfSpider)
    web.run_app(
        app
    )
