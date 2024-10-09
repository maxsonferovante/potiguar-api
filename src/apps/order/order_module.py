from nest.core import Module
from .order_controller import OrderController
from .order_service import OrderService


@Module(
    controllers=[OrderController],
    providers=[OrderService],
    imports=[]
)   
class OrderModule:
    pass

    