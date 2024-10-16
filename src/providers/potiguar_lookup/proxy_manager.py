from typing import List, Dict
from src.config import config_proxy

import httpx
import random

class ProxyManager:
    pass
    
    @staticmethod
    async def get_proxy():
        attemps = 0
        while attemps < 10:
            attemps += 1
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(config_proxy["proxy_list"], timeout=30,
                                headers={"Content-Type": "application/json"})      
            
                if response.status_code == 200:
                    return ProxyManager.random_proxy(response.json())   
                attemps += 1
            except Exception as exception:
                print("get_proxy exception: {}".format(exception))
                continue
        return None
    
    @staticmethod
    def random_proxy(response: Dict):
        chosen_proxy = random.choice(response['proxies'])
        print("Chosen proxy: {} - Localidade: {} {}".format(chosen_proxy['proxy'], chosen_proxy['ip_data']['city'],chosen_proxy['ip_data']['country']))
        return chosen_proxy["proxy"]
     
            
  
    
