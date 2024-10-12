from nest.core import Module
from .order_controller import OrderController
from .order_service import OrderService

from src.providers.potiguar_lookup.potiguar_lookup_module import PotiguarLookupModule
from src.apps.tasks.tasks_module import TasksModule

@Module(
    controllers=[OrderController],
    providers=[OrderService],
    imports=[PotiguarLookupModule, TasksModule]
)   
class OrderModule:
    pass

    