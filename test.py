from src.providers.potiguar_lookup.potiguar_lookup_service import PotiguarLookupService
from src.providers.recaptcha.recaptcha_service import RecaptchaService


import asyncio                
recaptcha = RecaptchaService()
potiguar_lookup = PotiguarLookupService(recaptcha_service=recaptcha)


dados ={
    "placa": "RGG0E83",
    "renavam": "1260720184",
}
print (dados)
response = asyncio.run(potiguar_lookup.obtain_vehicle_data(dados["placa"], dados["renavam"]))
print(response)

response = asyncio.run(potiguar_lookup.obtain_vehicle_debts(response))
print(response)