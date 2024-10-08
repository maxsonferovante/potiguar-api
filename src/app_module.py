from nest.core import PyNestFactory, Module
from .config import config
from .app_controller import AppController
from .app_service import AppService


@Module(imports=[], controllers=[AppController], providers=[AppService])
class AppModule:
    pass


app = PyNestFactory.create(
    AppModule,
    description="This is my Async PyNest app.",
    title="PyNest Application",
    version="1.0.0",
    debug=True,
)

http_server = app.get_server()

@http_server.on_event("startup")
async def startup():
    await config.create_all()
    
