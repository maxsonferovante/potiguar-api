from src.providers.potiguar_lookup.potiguar_lookup_service import PotiguarLookupService
from src.apps.tasks.tasks_service import TasksService
from .order_model import Order, OrderCreateDTO, transform_OrderCreateDTO_to_order, OrderFindDTO, OrderStatus
from .order_entity import Order as OrderEntity, transform_Document_to_Order
from .exceptions.order_not_found_exception import OrderNotFoundException

from nest.core.decorators.database import db_request_handler
from nest.core import Injectable

from fastapi import HTTPException

@Injectable
class OrderService:
    def __init__(self, potiguar_lookup_service: PotiguarLookupService, tasks_service: TasksService):
        self.potiguar_lookup_service = potiguar_lookup_service
        self.tasks_service = tasks_service


    @db_request_handler
    async def add_order(self, order: OrderCreateDTO) -> Order:
        
        orderModel = transform_OrderCreateDTO_to_order(order)
        
        # vehicle_data = await self.potiguar_lookup_service.get_vehicle_data(order.dict())
        # vehicle_debts = await self.potiguar_lookup_service.obtain_vehicle_debts(vehicle_data)
        # orderModel.result = {
        #     "vehicle_data": vehicle_data,
        #     "vehicle_debts": vehicle_debts
        # }
        # orderModel.status = OrderStatus.COMPLETED
        
        new_order = OrderEntity(**orderModel.dict())
        
        await new_order.save()
        
        message = self.tasks_service.run_get_vehicle_data(
            license_plate=orderModel.license_plate,
            renavam=orderModel.renavam,
            identifier=orderModel.identifier   
        )
        
        orderModel.result = message
        
        return orderModel

    @db_request_handler
    async def get_order_by_identifier(self, identifier: str) -> Order:
        
        order_find = OrderFindDTO(identifier=identifier)      
        
        result = await OrderEntity.find_one(OrderEntity.identifier == order_find.identifier)
        
        if not result:
            raise OrderNotFoundException(order_find.identifier)
        
        return transform_Document_to_Order(result)
