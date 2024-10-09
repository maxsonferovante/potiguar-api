from typing import Optional, Dict
from datetime import datetime
from beanie import Document
from .order_model import OrderStatus        
        
class Order(Document):
    identifier: str
    status: str = OrderStatus.PENDING
    license_plate: str
    renavam: str
    created_at: datetime
    result: Dict = {}
    
    class Config:
        schema_extra = {
            "order": {
                "identifier": "string",
                "status": "string",
                "license_plate": "string",
                "renavam": "string",
                "created_at": "string",
                "result": "any"
            }
        }
