from fastapi import HTTPException
from typing import Optional


class RENIECException(HTTPException):
    """
    Excepción base para errores relacionados con RENIEC
    """
    
    def __init__(
        self,
        status_code: int,
        error_code: str,
        message: str,
        details: Optional[dict] = None
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "error": error_code,
                "message": message,
                "status_code": status_code,
                "details": details
            }
        )


class DNIInvalidException(RENIECException):
    """
    Excepción para DNI inválido
    """
    
    def __init__(self, dni: str):
        super().__init__(
            status_code=400,
            error_code="DNI_INVALIDO",
            message=f"El DNI '{dni}' no tiene un formato válido",
            details={"dni": dni}
        )


class PersonaNotFoundException(RENIECException):
    """
    Excepción para persona no encontrada
    """
    
    def __init__(self, dni: str):
        super().__init__(
            status_code=404,
            error_code="PERSONA_NO_ENCONTRADA",
            message=f"No se encontraron datos para el DNI: {dni}",
            details={"dni": dni}
        )


class APIServiceException(RENIECException):
    """
    Excepción para errores de la API externa
    """
    
    def __init__(self, service: str, message: str):
        super().__init__(
            status_code=503,
            error_code="SERVICIO_EXTERNO_ERROR",
            message=f"Error en el servicio {service}: {message}",
            details={"service": service}
        )


class RateLimitException(RENIECException):
    """
    Excepción para límite de peticiones excedido
    """
    
    def __init__(self):
        super().__init__(
            status_code=429,
            error_code="RATE_LIMIT_EXCEEDED",
            message="Se ha excedido el límite de peticiones",
            details={"retry_after": 60}
        ) 