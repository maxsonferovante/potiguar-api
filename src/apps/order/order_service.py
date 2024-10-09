from .order_model import Order, OrderCreateDTO, transform_OrderCreateDTO_to_order
from .order_entity import Order as OrderEntity
from nest.core.decorators.database import db_request_handler
from nest.core import Injectable


@Injectable
class OrderService:

    @db_request_handler
    async def add_order(self, order: OrderCreateDTO) -> Order:
        
        orderModel = transform_OrderCreateDTO_to_order(order)
        new_order = OrderEntity(**orderModel.dict())
        await new_order.save()
        return orderModel

    @db_request_handler
    async def get_order(self):
        return await OrderEntity.find_all().to_list()
