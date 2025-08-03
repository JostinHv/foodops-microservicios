from pydantic import BaseModel, Field, validator
from typing import Optional


class DNIRequest(BaseModel):
    """
    Modelo para la solicitud de consulta de DNI
    """
    dni: str = Field(..., description="Número de DNI a consultar", min_length=8, max_length=8)
    
    @validator('dni')
    def validate_dni(cls, v):
        """Valida que el DNI sea numérico y tenga 8 dígitos"""
        if not v.isdigit():
            raise ValueError('El DNI debe contener solo números')
        if len(v) != 8:
            raise ValueError('El DNI debe tener exactamente 8 dígitos')
        return v


class PersonaResponse(BaseModel):
    """
    Modelo para la respuesta de datos de persona (simplificado)
    Solo incluye los campos esenciales
    """
    dni: str = Field(..., description="Número de DNI")
    nombres: str = Field(..., description="Nombres de la persona")
    apellido_paterno: str = Field(..., description="Apellido paterno")
    apellido_materno: str = Field(..., description="Apellido materno")
    nombres_completos: str = Field(..., description="Nombre completo formateado")


class DecolectaResponse(BaseModel):
    """
    Modelo para la respuesta directa de la API de Decolecta
    """
    first_name: str
    first_last_name: str
    second_last_name: str
    full_name: str
    document_number: str


class ErrorResponse(BaseModel):
    """
    Modelo para respuestas de error
    """
    error: str
    message: str
    status_code: int
    detalles: Optional[dict] = None


class APILimitResponse(BaseModel):
    """
    Modelo para respuesta cuando se excede el límite de API
    """
    error: str = "LIMITE_API_EXCEDIDO"
    message: str = "Se ha excedido el límite de peticiones mensuales (2/1000)"
    status_code: int = 429
    peticiones_restantes: int = 0
    peticiones_usadas: int = 2
    limite_mensual: int = 1000 