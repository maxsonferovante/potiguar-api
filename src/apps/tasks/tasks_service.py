import asyncio
import redis
import json
from celery import Celery, states
from typing import Dict
from nest.core import Injectable
from src.providers.potiguar_lookup.potiguar_lookup_service import PotiguarLookupService
from src.providers.recaptcha.recaptcha_service import RecaptchaService

from src.providers.potiguar_lookup.potiguar_lookup_exception import LicensePlaceOrRenavamException, UserPasswordException, InternalServerErrorException
from src.providers.recaptcha.recaptcha_exception import FaildCreateTaskException, FaildSolutionException

from src.config import config_redis



celery_manager = Celery(
    'tasks',
    broker=config_redis['url'],
    backend=config_redis['url']
)

redis = redis.Redis(host=config_redis['host'], port=config_redis['port'])

celery_manager.conf.update(
    visibility_timeout=3600,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/Sao_Paulo',
    enable_utc=True
)

potiguar_lookup_service = PotiguarLookupService(RecaptchaService())

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

        
@celery_manager.task(name='get_vehicle_data',
                     default_retry_delay= 15,
                     autoretry_for=(Exception, InternalServerErrorException, FaildCreateTaskException, FaildSolutionException),)
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
    
    except LicensePlaceOrRenavamException as e:
        raise e
    except UserPasswordException as e:
        # aqui seria interessante enviar um email para o administrador do sistema
        print ("UserPasswordException: {}".format(e))
        
        # salvar no redis como falha 
        redis.set(identifier, json.dumps({
            "status": "FAILURE",
            "message": str(e),
            "identifier": identifier
        }), ex=3600)
        raise e
    except InternalServerErrorException as e:
        raise e
    except FaildCreateTaskException as e:
        raise e
    except FaildSolutionException as e:
        raise e
    except Exception as e:
        raise e
         
       
