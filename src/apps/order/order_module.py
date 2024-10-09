from nest.core import Module
from .order_controller import OrderController
from .order_service import OrderService

from src.providers.potiguar_lookup.potiguar_lookup_module import PotiguarLookupModule

@Module(
    controllers=[OrderController],
    providers=[OrderService],
    imports=[PotiguarLookupModule]
)   
class OrderModule:
    pass

    