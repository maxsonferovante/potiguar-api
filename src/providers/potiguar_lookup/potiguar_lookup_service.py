from nest.core import Injectable
from src.config import config_auth, config_recaptcha
from src.providers.recaptcha.recaptcha_service import RecaptchaService
from .token_manager import TokenManager

from typing import Dict
from datetime import datetime, timedelta
import json
import os
import jwt
import httpx

@Injectable
class PotiguarLookupService:    
    def __init__(self, recaptcha_service:RecaptchaService):
        self.recaptcha_service = recaptcha_service                      
        
        self.username = config_auth["username"]
        self.password = config_auth["password"]
        self.api = config_auth["api"]
        self.referer = config_recaptcha["site_url"]
              
    async def login(self, new_token: bool = False):
        
        is_token_valid = TokenManager.is_token_valid()
        
        if is_token_valid and not new_token:
            return TokenManager.get_token()
        
        recaptcha = await self.recaptcha_service.get_recaptcha()
        
        data = {
            "username": self.username,
            "password": self.password,
        }
        
        headers = self.build_headers({"tokencaptcha": recaptcha})
        
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.api}/auth/login", json=data, headers=headers, timeout=30)
            
            if response.status_code == 400:
                # {'success': False, 'data': ['Login ou senha inválidos']}
                print ("Failed to login: {} - {}".format(response.status_code, response.json()))
            elif response.status_code != 200:
                print ("Failed to login: {} - {}".format(response.status_code, response.json()))
                raise Exception("Failed to login")
            
            bearer_token = response.json().get("data")
            
            TokenManager.save_token(bearer_token)
            
            return bearer_token
    
    
    async def get_vehicle_data(self, order: Dict):
        new_token = False
        
        for attempt in range(3):
            try:        
                bearer_token = await self.login(new_token=new_token)
                
                recaptcha = await self.recaptcha_service.get_recaptcha()
                
                if not recaptcha:
                    raise Exception("Failed to get recaptcha")
                # payload = {
                #    "placa": "rgg0e83",
                #    "renavam": " 1260720184"
                # }
                payload = {
                    "placa": order["license_plate"],
                    "renavam": order["renavam"]
                }
                headers = self.build_headers({"tokencaptcha": recaptcha, "authentication": bearer_token})
                
                async with httpx.AsyncClient() as client:
                    response = await client.post(f"{self.api}/consultaveiculo/obtemdadosveiculo", json=payload, headers=headers, timeout=30)
                    
                    if response.status_code == 400:
                        print("Failed to get vehicle data: status: {} - {}".format(response.status_code, response.json()))
                        new_token = True
                    elif response.status_code != 200:
                        raise Exception("Failed to get vehicle data: status: {} - {}".format(response.status_code, response.json()))
                    
                    return response.json()["data"]
            except Exception as e:
                raise e
    async def obtain_vehicle_debts(self, vehicle_data: Dict):
        
        recaptcha = await self.recaptcha_service.get_recaptcha()
        
        if not recaptcha:
            raise Exception("Failed to get recaptcha")
        
        bearer_token = await self.login()
        
        headers = self.build_headers({"tokencaptcha": recaptcha, "authentication": bearer_token})
        
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.api}/consultaveiculo/obtemdebitosveiculo", json=vehicle_data, headers=headers, timeout=30)
            
            if response.status_code != 200:
                raise Exception("Failed to get vehicle debts")
            
            return response.json()["data"]
        
    def build_headers(self, data: Dict = None):
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "content-type": "application/json",
            "priority": "u=1, i",
            "sec-ch-ua": "\"Microsoft Edge\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Linux\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "Referer": self.referer,
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }
        
        if not data:
            return headers
        
        if data.get('tokencaptcha'):
            headers['tokencaptcha'] = data['tokencaptcha']
        if data.get('authentication'):
            headers['Authorization'] = "Bearer " + data['authentication']

        # ordena as chaves do dicionário em ordem alfabética
        headers = dict(sorted(headers.items()))
        return headers
    
