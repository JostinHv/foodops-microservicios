from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from app.models.request_models import PersonaResponse, ErrorResponse, APILimitResponse
from app.services.reniec_service import RENIECService
from app.services.cache_service import cache_service
from app.middleware.rate_limiter import rate_limiter
from app.utils.validators import validate_dni_format
import logging
import time

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/reniec", tags=["RENIEC"])


def get_reniec_service() -> RENIECService:
    """
    Dependency injection para el servicio de RENIEC
    """
    return RENIECService()


@router.get(
    "/persona/{dni}",
    response_model=PersonaResponse,
    responses={
        200: {"description": "Datos de la persona encontrados"},
        400: {"model": ErrorResponse, "description": "DNI inválido"},
        404: {"model": ErrorResponse, "description": "Persona no encontrada"},
        429: {"model": APILimitResponse, "description": "Límite de API excedido"},
        500: {"model": ErrorResponse, "description": "Error interno del servidor"}
    },
    summary="Consultar datos de persona por DNI",
    description="Obtiene los datos personales de una persona usando su número de DNI. Validación estricta para optimizar el consumo de API (2/1000 peticiones mensuales). Incluye cache de 30 minutos."
)
async def get_person_by_dni(
    dni: str,
    reniec_service: RENIECService = Depends(get_reniec_service)
) -> PersonaResponse:
    """
    Consulta los datos de una persona por su DNI
    Optimizado con cache y validación estricta
    
    Args:
        dni: Número de DNI de 8 dígitos
        reniec_service: Servicio de RENIEC inyectado
        
    Returns:
        Datos de la persona
        
    Raises:
        HTTPException: Si el DNI es inválido o no se encuentra la persona
    """
    try:
        # Validación estricta del DNI antes de consumir la API
        if not validate_dni_format(dni):
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "DNI_INVALIDO",
                    "message": "El DNI debe contener exactamente 8 dígitos numéricos y no puede empezar con 0",
                    "status_code": 400,
                    "detalles": {
                        "dni_proporcionado": dni,
                        "longitud": len(dni) if dni else 0,
                        "es_numerico": dni.isdigit() if dni else False
                    }
                }
            )
        
        # Consultar datos de la persona
        persona = reniec_service.get_person_by_dni(dni)
        
        if not persona:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "PERSONA_NO_ENCONTRADA",
                    "message": f"No se encontraron datos para el DNI: {dni}",
                    "status_code": 404,
                    "detalles": {"dni": dni}
                }
            )
        
        logger.info(f"Datos consultados exitosamente para DNI: {dni}")
        return persona
        
    except HTTPException:
        # Re-lanzar las excepciones HTTP
        raise
    except Exception as e:
        logger.error(f"Error inesperado al consultar DNI {dni}: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "ERROR_INTERNO",
                "message": "Error interno del servidor",
                "status_code": 500
            }
        )


@router.get(
    "/health",
    summary="Verificar estado del servicio",
    description="Endpoint para verificar que el servicio esté funcionando correctamente"
)
async def health_check() -> dict:
    """
    Endpoint de verificación de salud del servicio
    
    Returns:
        Estado del servicio
    """
    return {
        "status": "healthy",
        "service": "reniec-microservice",
        "version": "1.0.0",
        "api_provider": "Decolecta",
        "optimizacion": "Validación estricta para ahorrar peticiones",
        "cache": "Habilitado (30 minutos TTL)",
        "rate_limiting": "Habilitado"
    }


@router.get(
    "/api-usage",
    summary="Monitorear uso de la API",
    description="Obtiene información sobre el consumo de peticiones de la API de Decolecta"
)
async def get_api_usage(
    reniec_service: RENIECService = Depends(get_reniec_service)
) -> dict:
    """
    Endpoint para monitorear el uso de la API de Decolecta
    
    Returns:
        Información sobre el uso de la API
    """
    usage_info = reniec_service.get_api_usage_info()
    
    return {
        "api_provider": "Decolecta",
        "limite_mensual": usage_info["limite_mensual"],
        "peticiones_usadas": usage_info["peticiones_usadas"],
        "peticiones_restantes": usage_info["peticiones_restantes"],
        "porcentaje_usado": f"{usage_info['porcentaje_usado']:.1f}%",
        "timeout_segundos": usage_info["timeout_segundos"],
        "cache_stats": usage_info["cache_stats"],
        "recomendacion": "Validar DNI antes de consultar para optimizar uso"
    }


@router.get(
    "/cache/stats",
    summary="Estadísticas del cache",
    description="Obtiene estadísticas detalladas del cache en memoria"
)
async def get_cache_stats() -> dict:
    """
    Endpoint para obtener estadísticas del cache
    
    Returns:
        Estadísticas del cache
    """
    cache_stats = cache_service.get_stats()
    
    return {
        "cache_type": "Memory Cache",
        "ttl_minutos": 30,
        "total_entries": cache_stats["total_entries"],
        "hit_rate_percent": cache_stats["hit_rate_percent"],
        "hits": cache_stats["hits"],
        "misses": cache_stats["misses"],
        "sets": cache_stats["sets"],
        "evictions": cache_stats["evictions"],
        "total_requests": cache_stats["total_requests"]
    }


@router.delete(
    "/cache/clear",
    summary="Limpiar cache",
    description="Elimina todas las entradas del cache en memoria"
)
async def clear_cache() -> dict:
    """
    Endpoint para limpiar el cache
    
    Returns:
        Confirmación de limpieza
    """
    cache_service.clear()
    
    return {
        "message": "Cache limpiado exitosamente",
        "status": "success",
        "timestamp": time.time()
    }


@router.get(
    "/rate-limit/stats",
    summary="Estadísticas de rate limiting",
    description="Obtiene estadísticas del rate limiting por IP"
)
async def get_rate_limit_stats() -> dict:
    """
    Endpoint para obtener estadísticas del rate limiting
    
    Returns:
        Estadísticas del rate limiting
    """
    rate_limit_stats = rate_limiter.get_stats()
    
    return {
        "rate_limiting": "Habilitado",
        "total_minute_requests": rate_limit_stats["total_minute_requests"],
        "total_hour_requests": rate_limit_stats["total_hour_requests"],
        "unique_ips": rate_limit_stats["unique_ips"],
        "limits": rate_limit_stats["limits"]
    } 