from fastapi import HTTPException, status as HTTPStatus
from .identifier_not_valid import IdentifierNotValid
from .order_not_found_exception import OrderNotFoundException


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
    
    raise HTTPException(status_code=500, 
                        detail= {
                            "message": str(exception),
                            "type": "InternalServerError"
                    })