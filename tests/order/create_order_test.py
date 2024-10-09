import pytest
from pydantic import ValidationError
from src.apps.order.order_model import OrderCreateDTO, Order, transform_OrderCreateDTO_to_order


class TestOrderCreateDTO:
    
    def create_OrderCreateDTO(self):
        OrderCreateDTO = OrderCreateDTO(license_plate="ABC1234", renavam="123456789")
        assert OrderCreateDTO.license_plate == "ABC1234"
        assert OrderCreateDTO.renavam == "123456789"

    # não enviar os campos obrigatórios
    def test_create_OrderCreateDTO_with_none(self):
        with pytest.raises(ValidationError):
            OrderCreateDTO()
    
    def test_create_OrderCreateDTO_with_invalid(self):
        with pytest.raises(ValidationError):
            OrderCreateDTO(invalid_field="invalid_value")
            
               
    def test_transform_OrderCreateDTO_to_order(self):
        OrderCreateDTO = OrderCreateDTO(license_plate="ABC1234", renavam="123456789")
        order = transform_OrderCreateDTO_to_order(OrderCreateDTO)
        assert order.license_plate == "ABC1234"
        assert order.renavam == "123456789"
        assert order.status == "PENDING"
        assert order.result == {}
        assert order.identifier
        assert order is not None

    def test_transform_OrderCreateDTO_to_order_with_none(self):
        OrderCreateDTO = OrderCreateDTO(license_plate="ABC1234",renavam="123456789")
        order = transform_OrderCreateDTO_to_order(OrderCreateDTO)
        assert order.license_plate == "ABC1234"
        assert order.renavam == "123456789"
        assert order.status == "PENDING"
        assert order.result == {}
        assert order.identifier
        assert order is not None
    

class TestOrderModel:
    def test_create_order(self):
        order = Order(license_plate="ABC1234", renavam="123456789")
        assert order.license_plate == "ABC1234"
        assert order.renavam == "123456789"
        assert order.status == "PENDING"
        assert order.result == {}
        assert order.identifier
        assert order.created_at
        assert order is not None
        
    def test_create_order_with_none(self):
        with pytest.raises(ValidationError):
            Order()
    def test_create_order_with_invalid(self):
        with pytest.raises(ValidationError):
            Order(invalid_field="invalid_value")
    