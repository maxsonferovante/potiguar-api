from nest.core import Controller, Get, Post

from .order_service import OrderService
from .order_model import OrderCreateDTO, Order


@Controller("order")
class OrderController:

    def __init__(self, order_service: OrderService):
        self.service = service

    @Get("/")
    async def get_order(self):
        return await self.order_service.get_order()

    @Post("/")
    async def add_order(self, order: OrderCreateDTO) -> Order:
        return await self.order_service.add_order(order)
 