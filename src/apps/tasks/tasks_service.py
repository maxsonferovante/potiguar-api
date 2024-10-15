import asyncio
import redis
import json
from celery import Celery, states
from typing import Dict
from nest.core import Injectable
from src.providers.potiguar_lookup.potiguar_lookup_service import PotiguarLookupService
from src.providers.recaptcha.recaptcha_service import RecaptchaService

from src.providers.potiguar_lookup.potiguar_lookup_exception import LicensePlaceOrRenavamException, UserPasswordException, InternalServerErrorException, UserBlockedException
from src.providers.recaptcha.recaptcha_exception import FaildCreateTaskException, FaildSolutionException

from src.config import config_redis

print("config_redis: {}".format(config_redis))
redis = redis.Redis.from_url(url=config_redis['url'], ssl=True, ssl_cert_reqs='CERT_REQUIRED')

celery_manager = Celery(
    'tasks',
    broker=config_redis['url'],
    backend=config_redis['url'],
)


celery_manager.conf.update(
    broker_use_ssl={
        'ssl_cert_reqs': 'CERT_REQUIRED'
        },
    backend_use_ssl={
        'ssl_cert_reqs': 'CERT_REQUIRED'},
    visibility_timeout=3600,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/Sao_Paulo',
    enable_utc=True
)

potiguar_lookup_service = PotiguarLookupService(RecaptchaService())

AUTORETRY_FOR = (InternalServerErrorException, FaildCreateTaskException, FaildSolutionException, LicensePlaceOrRenavamException)

@Injectable
class TasksService:

        
    def run_get_vehicle_data(self, license_plate: str, renavam: str, identifier: str):       
        try:
            print("Starting task for license_plate: {} and renavam: {} -- {}".format(license_plate, renavam, identifier))

            task = get_vehicle_data.delay(license_plate, renavam, identifier)
            return {
                "message": "Task completed for license_plate: {} and renavam: {}".format(license_plate, renavam),
                "task_id": task.id  # Retorna o ID da tarefa
            }
        except Exception as e:
            print("Error: {}".format(e))
    
    def get_result_task(self, identifier: str):
        try:
            print("Getting result for identifier: {}".format(identifier))
            
            task_result = redis.get(identifier)
            print ("Task result from redis: {}".format(task_result))
            if task_result:
                redis.delete(identifier)
                return json.loads(task_result)
            return None
        except Exception as e:
            print("Error: {}".format(e))
            return None

        
@celery_manager.task(name='get_vehicle_data',default_retry_delay= 10, autoretry_for=AUTORETRY_FOR, retry_kwargs={'max_retries': 3, })
def get_vehicle_data(license_plate: str, renavam: str, identifier: str):
    try:
        vehicle_data = asyncio.run(potiguar_lookup_service.obtain_vehicle_data(
        license_plate=license_plate,
        renavam=renavam
        ))
        vehicle_debts = asyncio.run(potiguar_lookup_service.obtain_vehicle_debts(vehicle_data=vehicle_data))
        
        vehicle_infractions =  asyncio.run(potiguar_lookup_service.obtain_vehicle_infractions(vehicle_data=vehicle_data))
        
        vehicle_fines = asyncio.run(potiguar_lookup_service.obtain_vehicle_fines(vehicle_data=vehicle_data))
        
        
        result = {
            "vehicle_data": vehicle_data,
            "vehicle_debts": vehicle_debts,
            "vehicle_infractions": vehicle_infractions,
            "vehicle_fines": vehicle_fines,
            "identifier": identifier
        }
        
        redis.set(identifier, json.dumps(result), ex=3600)
        
        return result
    
    except Exception as exception:
        print ('get_vehicle_data exception: {}'.format(exception))
        if isinstance(exception, AUTORETRY_FOR) and get_vehicle_data.request.retries <3:
            raise exception                        
                                
        elif isinstance(exception, UserBlockedException):
            
            save_information_about_task.delay(identifier, {
            "status": "FAILURE",
            "tpye": type(exception).__name__,
            "message": "Service unavailable. Please try again in a few moments. If the problem persists, please contact the administrator, providing the following identifier {} and type {}".format(identifier, type(exception).__name__),
            "identifier": identifier
            })            
            
            send_email_alert.delay(
                "User blocked: {}. Expection: {} Type: {}".format(identifier, str(exception),type(exception).__name__)
            )
            
            raise exception
        else:
            save_information_about_task.delay(identifier, {
            "status": "FAILURE",
            "tpye": type(exception).__name__,
            "message": "An error occurred while processing your request. Please try again in a few moments. If the problem persists, please contact the administrators, providing the following identifier {} and type {}".format(identifier, type(exception).__name__),
            "identifier": identifier
            })
            
            raise exception
        
        
@celery_manager.task(name='save_information_about_task')        
def save_information_about_task(identifier:str, information: Dict):
    print("Saving information: {}".format(information))
    
    redis.set(identifier, json.dumps(information), ex=3600)
    
    return {
        "message": "Information saved",
        "information": information
    }
       

@celery_manager.task(name='send_email_alert')
def send_email_alert(alert: str):
    print("Sending email alert: {}".format(alert))
    return {
        "message": "Email sent"
    }