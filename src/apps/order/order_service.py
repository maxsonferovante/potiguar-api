from .order_model import Order, OrderDTO, transform_orderDTO_to_order
from .order_entity import Order as OrderEntity
from nest.core.decorators.database import db_request_handler
from nest.core import Injectable


@Injectable
class OrderService:

    @db_request_handler
    async def add_order(self, order: OrderDTO) -> Order:
        
        orderModel = transform_orderDTO_to_order(order)
        new_order = OrderEntity(**orderModel.dict())
        await new_order.save()
        return orderModel

    @db_request_handler
    async def get_order(self):
        return await OrderEntity.find_all().to_list()
