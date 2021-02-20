from aiohttp import web

from src.init.routes import routes
from src.spiders.easydarf.flow.darf import DarfSpider
from src.spiders.easydarf.flow.income import IncomeSpider


def run():
    app = web.Application()
    app.add_routes(routes=routes)
    app.router.add_view("/leao/darf", DarfSpider)
    app.router.add_view("/leao/income", IncomeSpider)
    web.run_app(app)
