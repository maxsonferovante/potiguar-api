from typing import Optional, Dict
from pydantic import BaseModel, Field
from enum import Enum

from datetime import datetime

import uuid

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Order(BaseModel):
    identifier: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: OrderStatus = Field(default=OrderStatus.PENDING, init=False)
    license_plate: str
    renavam: str
    created_at: datetime = Field(default_factory=datetime.now, init=False) 
    result: Optional[Dict] = {}

class OrderCreateDTO(BaseModel):
    license_plate: str
    renavam: str


def transform_OrderCreateDTO_to_order(order: OrderCreateDTO) -> OrderCreateDTO:
    return Order(
        license_plate=order.license_plate,
        renavam=order.renavam
    )
