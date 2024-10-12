from fastapi import HTTPException, status as HTTPStatus
from .identifier_not_valid import IdentifierNotValid
from .order_not_found_exception import OrderNotFoundException
from .conflict_order_exception import ConflictProcessOrderException

def handlers_order_expections(exception: Exception):
    if isinstance(exception, OrderNotFoundException):
        raise HTTPException(
            status_code= HTTPStatus.HTTP_404_NOT_FOUND, 
            detail= {
                "message": str(exception),
                "identifier": exception.identifier,
                "type": "OrderNotFoundException"
            })
        
    if isinstance(exception, IdentifierNotValid):
        raise HTTPException(
            status_code=HTTPStatus.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail= {
                "message": str(exception),
                "identifier": exception.identifier,
                "type": "IdentifierNotValid"
            })
    
    if isinstance(exception, ConflictProcessOrderException):
        raise HTTPException(
            status_code=HTTPStatus.HTTP_409_CONFLICT, 
            detail= {
                "message": str(exception),
                "license_plate": exception.license_plate,
                "renavam": exception.renavam,
                "identifier": exception.identifier,
                "task_id": exception.task_id,
                "type": "ConflictProcessOrderException"
            })
    raise HTTPException(status_code=500, 
                        detail= {
                            "message": str(exception),
                            "type": "InternalServerError"
                    })