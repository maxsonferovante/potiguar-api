from .order_model import Order, OrderCreateDTO, transform_OrderCreateDTO_to_order, OrderFindDTO
from .order_entity import Order as OrderEntity, transform_Document_to_Order
from .exceptions.order_not_found_exception import OrderNotFoundException

from nest.core.decorators.database import db_request_handler
from nest.core import Injectable

from fastapi import HTTPException

@Injectable
class OrderService:

    @db_request_handler
    async def add_order(self, order: OrderCreateDTO) -> Order:
        
        orderModel = transform_OrderCreateDTO_to_order(order)
        new_order = OrderEntity(**orderModel.dict())
        await new_order.save()
        return orderModel

    @db_request_handler
    async def get_order_by_identifier(self, identifier: str) -> Order:
        
        order_find = OrderFindDTO(identifier=identifier)      
        
        result = await OrderEntity.find_one(OrderEntity.identifier == order_find.identifier)
        
        if not result:
            raise OrderNotFoundException(order_find.identifier)
        
        return transform_Document_to_Order(result)
