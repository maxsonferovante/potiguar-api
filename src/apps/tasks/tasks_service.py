import asyncio
from celery import Celery, chain
from typing import Dict
from nest.core import Injectable
from src.providers.potiguar_lookup.potiguar_lookup_service import PotiguarLookupService
from src.providers.recaptcha.recaptcha_service import RecaptchaService
from src.apps.order.order_entity import Order as OrderEntity, OrderStatus
from src.config import config_redis

celery_manager = Celery(
    'tasks',
    broker=config_redis['url'],
    backend=config_redis['url']
)

potiguar_lookup_service = PotiguarLookupService(RecaptchaService())

@Injectable
class TasksService:


    def run_get_vehicle_data(self, license_plate: str, renavam: str, identifier: str):       
        try:
            print("Starting task for license_plate: {} and renavam: {} -- {}".format(license_plate, renavam, identifier))

            get_vehicle_data.delay(license_plate, renavam, identifier)
            
            return {
                "message": "Task completed for license_plate: {} and renavam: {}".format(license_plate, renavam)
            }
        except Exception as e:
            print("Error: {}".format(e))
    
        
@celery_manager.task(name='get_vehicle_data',retry_backoff=True,autoretry_for=(Exception,))
def get_vehicle_data(license_plate: str, renavam: str, identifier: str):
    vehicle_data = asyncio.run(potiguar_lookup_service.obtain_vehicle_data(
        license_plate=license_plate,
        renavam=renavam
    ))
    vehicle_debts = asyncio.run(potiguar_lookup_service.obtain_vehicle_debts(vehicle_data=vehicle_data))
    
    save_vehicle_data.delay(vehicle_data, vehicle_debts, identifier)
 
@celery_manager.task(name='save_vehicle_data',bind=True, retry_backoff=True,autoretry_for=())   
def save_vehicle_data(vehicle_data: Dict, vehicle_debts: Dict, identifier: str):
    order_find = asyncio.run(OrderEntity.find_one(OrderEntity.identifier == identifier))
    
    order_find.result = {
        "vehicle_data": 'vehicle_data',
        "vehicle_debts": 'vehicle_debts',
        }
    order_find.status = OrderStatus.COMPLETED
    asyncio.run(order_find.save())
        
        
       
