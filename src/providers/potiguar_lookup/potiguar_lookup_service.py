from nest.core import Injectable
from src.config import config_auth, config_recaptcha
from src.providers.recaptcha.recaptcha_service import RecaptchaService
from .token_manager import TokenManager
from .potiguar_lookup_exception import LicensePlaceOrRenavamException, UserPasswordException, InternalServerErrorException

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
            elif response.status_code == 500:
                print ("Failed to login: {} - {}".format(response.status_code, response.json()))
                raise InternalServerErrorException("Internal Server Error: {}".format(response.json()))
            
            bearer_token = response.json().get("data")
            
            TokenManager.save_token(bearer_token)
            
            return bearer_token
    
    
    async def obtain_vehicle_data(self, license_plate: str, renavam: str):
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
                    "placa": license_plate,
                    "renavam": renavam,
                }
                headers = self.build_headers({"tokencaptcha": recaptcha, "authentication": bearer_token})
                
                async with httpx.AsyncClient() as client:
                    response = await client.post(f"{self.api}/consultaveiculo/obtemdadosveiculo", json=payload, headers=headers, timeout=30)
                    
                    if response.status_code == 400:
                        self.handler_expection(response.json())
                        new_token = True
                    elif response.status_code == 500:
                        raise InternalServerErrorException("Internal Server Error: {}".format(response.json()))
                    elif response.status_code == 200:
                        return response.json()["data"]
                    
                    raise Exception("Failed to obtain vehicle data")
                
            except Exception as e:
                print('Error in obtain_vehicle_data: {}'.format(e))
                raise e
    
    async def obtain_vehicle_debts(self, vehicle_data: Dict):
        
        recaptcha = await self.recaptcha_service.get_recaptcha()
        
        if not recaptcha:
            raise Exception("Failed to get recaptcha")
        
        bearer_token = await self.login()
        
        headers = self.build_headers({"tokencaptcha": recaptcha, "authentication": bearer_token})
        
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.api}/consultaveiculo/obtemdebitosveiculo", json=vehicle_data, headers=headers, timeout=30)
            
            if response.status_code == 400:
                self.handler_expection(response.json())
                new_token = True
            elif response.status_code == 500:
                raise InternalServerErrorException("Internal Server Error: {}".format(response.json()))
            elif response.status_code == 200:
                return response.json()["data"]
            
            raise Exception("Failed to obtain vehicle debts")
    
    
    async def obtain_vehicle_infractions(self, vehicle_data: Dict):
        new_token = False        
        for attempt in range(3):
            try:        
                bearer_token = await self.login(new_token=new_token)
                
                recaptcha = await self.recaptcha_service.get_recaptcha()
                
                if not recaptcha:
                    raise Exception("Failed to get recaptcha")
            
                headers = self.build_headers({"tokencaptcha": recaptcha, "authentication": bearer_token})
    
                async with httpx.AsyncClient() as client:
                    response = await client.post(f"{self.api}/consultaveiculo/obteminfracoesveiculo", json=vehicle_data, headers=headers, timeout=30)
                    
                    if response.status_code == 400:
                        self.handler_expection(response.json())
                        new_token = True
                    elif response.status_code == 500:
                        raise InternalServerErrorException("Internal Server Error: {}".format(response.json()))
                    elif response.status_code == 200:
                        return response.json()["data"]
                    
                    raise Exception("Failed to obtain vehicle data")
                
            except Exception as e:
                print('Error in obtain_vehicle_data: {}'.format(e))
                raise e                            

    async def obtain_vehicle_fines(self, vehicle_data: Dict):
        new_token = False
        for attempt in range(3):
            try:
                bearer_token = await self.login(new_token=new_token)
                
                recaptcha = await self.recaptcha_service.get_recaptcha()
                
                if not recaptcha:
                    raise Exception("Failed to get recaptcha")
                
                headers = self.build_headers({"tokencaptcha": recaptcha, "authentication": bearer_token})
                
                async with httpx.AsyncClient() as client:
                    response = await client.post(f"{self.api}/consultaveiculo/obtemmultasveiculo", json=vehicle_data, headers=headers, timeout=30)
                    
                    if response.status_code == 400:
                        self.handler_expection(response.json())
                        new_token = True
                    elif response.status_code == 500:
                        raise InternalServerErrorException("Internal Server Error: {}".format(response.json()))
                    elif response.status_code == 200:
                        return response.json()["data"]
                    
                    raise Exception("Failed to obtain vehicle data")
            except Exception as e:
                print('Error in obtain_vehicle_data: {}'.format(e))
                raise e
            
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
    

    def handler_expection(self,data: Dict):
        message = data.get("data")
        
        if message == "Login ou senha inválidos":
            raise UserPasswordException(message)
        elif message == "Placa e/ou Renavam incorretos, por favor verifique os dados!":
            raise LicensePlaceOrRenavamException(message)