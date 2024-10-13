from src.providers.potiguar_lookup.potiguar_lookup_service import PotiguarLookupService
from src.apps.tasks.tasks_service import TasksService
from .order_model import Order, OrderCreateDTO, transform_OrderCreateDTO_to_order, OrderFindDTO, OrderStatus
from .order_entity import Order as OrderEntity, transform_Document_to_Order
from .exceptions.order_not_found_exception import OrderNotFoundException
from .exceptions.conflict_order_exception import ConflictProcessOrderException

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
        
        # verifica se já existe uma ordem license_plate erenavam em processamento
        # devo olhar no banco de dados se já existe uma ordem com esses dados
        # se existir, devo retornar uma mensagem de erro
        existing_order = await OrderEntity.find_one(
            OrderEntity.license_plate == orderModel.license_plate,
            OrderEntity.renavam == orderModel.renavam,
        )
        print ("existing_order", existing_order)
        if existing_order:
            if existing_order.status == OrderStatus.PROCESSING or existing_order.status == OrderStatus.PENDING:
                raise ConflictProcessOrderException(
                    license_plate=orderModel.license_plate,
                    renavam=orderModel.renavam,
                    identifier=existing_order.identifier,
                    task_id=existing_order.result.get('task_id')
                )
                       
        new_order = OrderEntity(**orderModel.dict())
        
        
        task = self.tasks_service.run_get_vehicle_data(
            license_plate=orderModel.license_plate,
            renavam=orderModel.renavam,
            identifier=orderModel.identifier   
        )
        
        orderModel.result = task        
        new_order.result = task
        
        await new_order.save()
        
        return orderModel

    @db_request_handler
    async def get_order_by_identifier(self, identifier: str) -> Order:
        
        order_find = OrderFindDTO(identifier=identifier)      
        
        order = await OrderEntity.find_one(OrderEntity.identifier == order_find.identifier)
        if not order:
            raise OrderNotFoundException(order_find.identifier)
        
        if order.status == OrderStatus.COMPLETED or order.status == OrderStatus.FAILED:
            return transform_Document_to_Order(order)
        
        task_result = self.tasks_service.get_result_task(order.identifier)

        if task_result is not None:
            if task_result.get('status') == "FAILURE":
                
                order.status = OrderStatus.FAILED
                
                order.result = {
                    "message": task_result.get('message'),  
                    "taks_id": order.result.get('task_id'),    
                }
            else:
                order.result = {
                    "vehicle_data": task_result.get('vehicle_data'),
                    "vehicle_debts": task_result.get('vehicle_debts'),
                    "vehicle_infractions": task_result.get('vehicle_infractions'),
                    "vehicle_fines": task_result.get('vehicle_fines'),
                    "taks_id": order.result.get('task_id'),
                }
                order.status = OrderStatus.COMPLETED
        else:
            order.status = OrderStatus.PROCESSING
            
        await order.save()
        return transform_Document_to_Order(order)
