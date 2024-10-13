from nest.core import Injectable
from src.config import config_auth, config_recaptcha
from src.providers.recaptcha.recaptcha_service import RecaptchaService
from .token_manager import TokenManager
from .potiguar_lookup_exception import LicensePlaceOrRenavamException, UserPasswordException, InternalServerErrorException, UserBlockedException

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
              
    async def login(self):
        
        is_token_valid = TokenManager.is_token_valid()
        
        if is_token_valid:
            return TokenManager.get_token()
        
        recaptcha = await self.recaptcha_service.get_recaptcha()
        
        data = {
            "username": self.username,
            "password": self.password,
        }
        
        headers = self.build_headers({"tokencaptcha": recaptcha})
        
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.api}/auth/login", json=data, headers=headers, timeout=30)
            
            if response.status_code != 200:
                self.handler_expection(response.json())            
            
            bearer_token = response.json().get("data")
            
            TokenManager.save_token(bearer_token)
            
            return bearer_token
    
    
    async def obtain_vehicle_data(self, license_plate: str, renavam: str):
               
        bearer_token = await self.login()
                
        recaptcha = await self.recaptcha_service.get_recaptcha()                
        
        headers = self.build_headers({"tokencaptcha": recaptcha, "authentication": bearer_token})
                
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.api}/consultaveiculo/obtemdadosveiculo", json={"placa": license_plate,"renavam": renavam,}, headers=headers, timeout=30)
                
            if response.status_code != 200:
                self.handler_expection(response.json())
        
            return response.json()["data"]
                
    async def obtain_vehicle_debts(self, vehicle_data: Dict):
        
        recaptcha = await self.recaptcha_service.get_recaptcha()
        
        bearer_token = await self.login()
        
        headers = self.build_headers({"tokencaptcha": recaptcha, "authentication": bearer_token})
        
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.api}/consultaveiculo/obtemdebitosveiculo", json=vehicle_data, headers=headers, timeout=30)        
            if response.status_code != 200:
                self.handler_expection(response.json())
            return response.json()["data"]
       
    async def obtain_vehicle_infractions(self, vehicle_data: Dict):
            bearer_token = await self.login()
                
            recaptcha = await self.recaptcha_service.get_recaptcha()
                                           
            headers = self.build_headers({"tokencaptcha": recaptcha, "authentication": bearer_token})
    
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.api}/consultaveiculo/obteminfracoesveiculo", json=vehicle_data, headers=headers, timeout=30)
                    
                if response.status_code != 200:
                    self.handler_expection(response.json())
                    
                return response.json()["data"]                
            
    async def obtain_vehicle_fines(self, vehicle_data: Dict):
            bearer_token = await self.login()
                
            recaptcha = await self.recaptcha_service.get_recaptcha()
                                           
            headers = self.build_headers({"tokencaptcha": recaptcha, "authentication": bearer_token})
    
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.api}/consultaveiculo/obtemmultasveiculo", json=vehicle_data, headers=headers, timeout=30)
                        
                if response.status_code != 200:
                    self.handler_expection(response.json())
                    
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
   
    def handler_expection(self,data: Dict):
            # Dicionário que mapeia mensagens de erro para exceções
        error_map = {
            "Login ou senha inválidos": UserPasswordException,
            "Seu cadastro encontra-se bloqueado": UserBlockedException,
            "CPF/CNPJ inválido.": UserBlockedException,
            "Placa e/ou Renavam incorretos, por favor verifique os dados!": LicensePlaceOrRenavamException,
            "Informe a placa do veículo": LicensePlaceOrRenavamException,
            "Informe o renavam do veículo": LicensePlaceOrRenavamException
        }
         # Extrai a lista de mensagens do dicionário
        message_list = data.get("data")
        
        # Se não houver mensagens, retorna um erro genérico
        
        if not message_list:
            raise InternalServerErrorException("Internal Server Error: No messages found in response")
        
        for message in message_list:
            matching_key =  next((key for key in error_map if key in message), None)    
            print('handler exception logs', message, data, message_list, matching_key)
            # Verifica se a mensagem está no dicionário de erros
            if matching_key:
                # Lança a exceção mapeada
                raise error_map[matching_key](message)
            
        # Caso a mensagem não corresponda a nenhuma condição anterior, levanta uma exceção de erro interno         
        raise InternalServerErrorException("Internal Server Error: {}".format(message))
              