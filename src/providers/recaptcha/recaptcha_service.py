from src.config import config_recaptcha
from nest.core import Injectable

from .recaptcha_exception import FaildCreateTaskException, FaildSolutionException

import httpx
import time
import asyncio
@Injectable
class RecaptchaService:
    def __init__(self):
        self.client_key = config_recaptcha["key"]
        self.task = {
            "type": 'ReCaptchaV3TaskProxyLess',
            "websiteKey": config_recaptcha["site_key"],
            "websiteURL": config_recaptcha["site_url"],
            "pageAction": "login",
        }
        self.url_captcha = config_recaptcha["url_captcha"] 
    
    async def get_recaptcha(self) -> str:
        async with httpx.AsyncClient() as client:
            try:
                payload = {
                    "clientKey": self.client_key,
                    "task": self.task
                }
                print ("Payload", payload)
                response = await client.post(f"{self.url_captcha}/createTask", json=payload, timeout=30)
                task_id = response.json().get("taskId")
                if not task_id:
                    raise FaildCreateTaskException("Failed to create task: {}".format(response.json()))
                while True:
                    await asyncio.sleep(1)
                    response = await client.post(f"{self.url_captcha}/getTaskResult", json={"clientKey": self.client_key, "taskId": task_id}, timeout=30)
                    status = response.json().get("status")
                    if status == "ready":
                        return response.json().get("solution", {}).get('gRecaptchaResponse')
                    if status == "failed" or response.json().get("errorId"):
                        raise FaildSolutionException("Failed to solve captcha: {}".format(response.json()))
            except Exception as e:
                if isinstance(e, Exception):
                    raise e
                raise e
            
            
        