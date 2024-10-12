from nest.core import PyNestFactory, Module
from .config import config
from .app_controller import AppController
from .app_service import AppService
from src.apps.order.order_module import OrderModule
from src.apps.tasks.tasks_module import TasksModule

from src.middlewares.rate_limit_middleware import RateLimitMiddleware

@Module(
    imports=[OrderModule, TasksModule],
    controllers=[AppController],
    providers=[AppService],
)
class AppModule:
    pass


app = PyNestFactory.create(
    AppModule,
    description="Potiguar API is a service designed to facilitate the consultation of vehicle infractions, subsidies, and fines in Rio Grande do Norte. It provides a robust and efficient way to access and manage this information through a well-structured API.",
    title="Potiguar API",
    version="1.0.0",
    docs_url="/api/docs",
)
http_server = app.get_server()
#  - RateLimitMiddleware: Limit the number of requests per client IP.
http_server.add_middleware(RateLimitMiddleware, max_requests=60, window_seconds=60)

@http_server.on_event("startup")
async def startup():
    await config.create_all()
