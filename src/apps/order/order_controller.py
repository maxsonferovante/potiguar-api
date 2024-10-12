from nest.core import Controller, Get, Post
from .order_service import OrderService
from .order_model import OrderCreateDTO, Order, OrderFindDTO
from .exceptions.handlers_order_expections import handlers_order_expections


@Controller("order")
class OrderController:

    def __init__(self, order_service: OrderService):
        self.service = service

    @Get("/{identifier}")
    async def get_order_by_identifier(self, identifier: str) -> Order:
        try:
            return await self.order_service.get_order_by_identifier(identifier)
        except Exception as exception:
            print ("Exception -- get_order_by_identifier", exception)
            handlers_order_expections(exception) 

    @Post("/")
    async def add_order(self, order: OrderCreateDTO) -> Order:
        try:
            return await self.order_service.add_order(order)
        except Exception as exception:
            print ("Exception - add_order", exception)
            handlers_order_expections(exception)
 