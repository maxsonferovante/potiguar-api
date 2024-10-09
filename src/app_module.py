from nest.core import PyNestFactory, Module
from .config import config
from .app_controller import AppController
from .app_service import AppService
from src.apps.order.order_module import OrderModule
from src.apps.detran_rn_crawler.detran_rn_crawler_module import DetranRnCrawlerModule


@Module(
    imports=[OrderModule, DetranRnCrawlerModule],
    controllers=[AppController],
    providers=[AppService],
)
class AppModule:
    pass


app = PyNestFactory.create(
    AppModule,
    description="This is my Async PyNest app.",
    title="PyNest Application",
    version="1.0.0",
    debug=True,
    docs_url="/api/docs"
)
http_server = app.get_server()


@http_server.on_event("startup")
async def startup():
    await config.create_all()
