import pytest
from pydantic import ValidationError
from datetime import datetime
from uuid import uuid4, UUID
from src.apps.order.order_model import Order, OrderCreateDTO, OrderFindDTO, transform_OrderCreateDTO_to_order, IdentifierNotValid, OrderStatus

def test_order_creation():
    order = Order(license_plate="ABC1234", renavam="123456789")
    assert order.identifier is not None
    assert order.status == OrderStatus.PENDING
    assert order.license_plate == "ABC1234"
    assert order.renavam == "123456789"
    assert isinstance(order.created_at, datetime)
    assert order.result == {}

def test_order_create_dto():
    order_create_dto = OrderCreateDTO(license_plate="ABC1234", renavam="123456789")
    assert order_create_dto.license_plate == "ABC1234"
    assert order_create_dto.renavam == "123456789"

def test_order_find_dto_valid_identifier():
    valid_uuid = str(uuid4())
    order_find_dto = OrderFindDTO(identifier=valid_uuid)
    assert order_find_dto.identifier == valid_uuid

def test_order_find_dto_invalid_identifier():
    with pytest.raises(IdentifierNotValid) as exc_info:
        OrderFindDTO(identifier="invalid-uuid")
    assert str(exc_info.value) == "Identifier 'invalid-uuid' is not valid."

def test_transform_order_create_dto_to_order():
    order_create_dto = OrderCreateDTO(license_plate="ABC1234", renavam="123456789")
    order = transform_OrderCreateDTO_to_order(order_create_dto)
    assert order.license_plate == "ABC1234"
    assert order.renavam == "123456789"
    assert order.status == OrderStatus.PENDING
    assert isinstance(order.identifier, str)
    assert isinstance(UUID(order.identifier), UUID)  # Check if it's a valid UUID
    assert isinstance(order.created_at, datetime)
    assert order.result == {}