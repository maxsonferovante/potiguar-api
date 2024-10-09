import pytest
from pydantic import ValidationError
from src.apps.order.order_model import OrderDTO, Order, transform_orderDTO_to_order


class TestOrderDTO:
    
    def create_orderDTO(self):
        orderDTO = OrderDTO(license_plate="ABC1234", renavam="123456789")
        assert orderDTO.license_plate == "ABC1234"
        assert orderDTO.renavam == "123456789"

    # não enviar os campos obrigatórios
    def test_create_orderDTO_with_none(self):
        with pytest.raises(ValidationError):
            OrderDTO()
    
    def test_create_orderDTO_with_invalid(self):
        with pytest.raises(ValidationError):
            OrderDTO(invalid_field="invalid_value")
            
               
    def test_transform_orderDTO_to_order(self):
        orderDTO = OrderDTO(license_plate="ABC1234", renavam="123456789")
        order = transform_orderDTO_to_order(orderDTO)
        assert order.license_plate == "ABC1234"
        assert order.renavam == "123456789"
        assert order.status == "PENDING"
        assert order.result == {}
        assert order.identifier
        assert order is not None

    def test_transform_orderDTO_to_order_with_none(self):
        orderDTO = OrderDTO(license_plate="ABC1234",renavam="123456789")
        order = transform_orderDTO_to_order(orderDTO)
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
    