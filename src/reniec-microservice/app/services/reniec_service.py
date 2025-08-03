import logging
import requests
import time
from typing import Optional, Dict, Any
from app.models.request_models import PersonaResponse, DecolectaResponse
from app.services.cache_service import cache_service
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class RENIECService:
    """
    Servicio para conectarse a la API de RENIEC a través de Decolecta
    Optimizado para minimizar el consumo de peticiones (2/1000 mensuales)
    Incluye cache en memoria y medidas de seguridad
    """
    
    def __init__(self, api_token: Optional[str] = None) -> None:
        """
        Inicializa el servicio de RENIEC
        
        Args:
            api_token: Token de autenticación para la API de Decolecta
        """
        self.api_token = api_token or os.getenv("DECOLECTA_API_TOKEN")
        self.base_url = "https://api.decolecta.com"
        self.request_count = 0
        self.monthly_limit = 1000
        self.request_timeout = 15  # Timeout de seguridad de 15 segundos
        
        if not self.api_token:
            logger.warning("No se proporcionó token de API. Algunas funcionalidades pueden no estar disponibles.")
    
    def _get(self, endpoint: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Realiza una solicitud GET autenticada al endpoint indicado
        Con timeout de seguridad y manejo de errores mejorado
        
        Args:
            endpoint: Endpoint de la API
            params: Parámetros de la consulta
            
        Returns:
            Respuesta de la API o None si hay error
        """
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "Referer": "reniec-microservice"
        }
        
        try:
            # Timeout de seguridad para evitar esperas indefinidas
            response = requests.get(
                url, 
                headers=headers, 
                params=params, 
                timeout=self.request_timeout
            )
            
            if response.status_code == 200:
                self.request_count += 1
                logger.info(f"Petición exitosa a Decolecta API. Total: {self.request_count}/{self.monthly_limit}")
                return response.json()
            elif response.status_code == 422:
                logger.warning(f"{response.url} - Parámetros inválidos: {params}")
                logger.warning(response.text)
            elif response.status_code == 403:
                logger.warning(f"{response.url} - Acceso denegado: IP bloqueada")
            elif response.status_code == 429:
                logger.warning(f"{response.url} - Demasiadas solicitudes: aplicar retardo")
            elif response.status_code == 401:
                logger.warning(f"{response.url} - Token inválido o sin permisos")
            else:
                logger.warning(f"{response.url} - Error del servidor: código {response.status_code}")
                
        except requests.exceptions.Timeout:
            logger.error(f"Timeout en petición a Decolecta API después de {self.request_timeout}s")
        except requests.exceptions.ConnectionError:
            logger.error("Error de conexión con Decolecta API")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en la solicitud HTTP: {e}")
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            
        return None
    
    def get_person_by_dni(self, dni: str) -> Optional[PersonaResponse]:
        """
        Consulta datos personales por DNI (RENIEC)
        Optimizado con cache y validación estricta
        
        Args:
            dni: Número de DNI a consultar
            
        Returns:
            Datos de la persona o None si no se encuentra
        """
        try:
            # Validación estricta del DNI antes de consumir la API
            if not self._validate_dni_format(dni):
                logger.error(f"DNI inválido: {dni} - No se consume la API")
                return None
            
            # Verificar cache primero
            cached_data = cache_service.get(dni)
            if cached_data:
                logger.info(f"Datos obtenidos del cache para DNI: {dni}")
                return cached_data
            
            # Verificar límite de peticiones
            if self.request_count >= self.monthly_limit:
                logger.error(f"Límite mensual de peticiones alcanzado: {self.request_count}/{self.monthly_limit}")
                return None
            
            # Consultar la API de Decolecta según la documentación oficial
            result = self._get("/v1/reniec/dni", {"numero": dni})
            
            if result:
                # Parsear la respuesta según el formato real de Decolecta
                persona_data = self._map_decolecta_response(result)
                
                # Guardar en cache
                cache_service.set(dni, persona_data)
                logger.info(f"Datos guardados en cache para DNI: {dni}")
                
                return persona_data
            else:
                logger.warning(f"No se encontraron datos para el DNI: {dni}")
                return None
                
        except Exception as e:
            logger.error(f"Error al consultar DNI {dni}: {e}")
            return None
    
    def _validate_dni_format(self, dni: str) -> bool:
        """
        Valida el formato del DNI antes de consumir la API
        Evita peticiones innecesarias para ahorrar el límite mensual
        
        Args:
            dni: Número de DNI a validar
            
        Returns:
            True si el formato es válido
        """
        if not dni:
            return False
        
        # Verificar que solo contenga números y tenga exactamente 8 dígitos
        if not dni.isdigit() or len(dni) != 8:
            return False
        
        # Validaciones adicionales para DNI peruano
        if dni.startswith('0'):  # DNI no puede empezar con 0
            return False
        
        # Verificar que no sea una secuencia de números repetidos
        if len(set(dni)) == 1:  # Todos los dígitos iguales
            return False
        
        return True
    
    def _map_decolecta_response(self, data: Dict[str, Any]) -> PersonaResponse:
        """
        Mapea la respuesta de la API de Decolecta al modelo en español
        
        Args:
            data: Datos de la respuesta de la API de Decolecta
            
        Returns:
            Modelo PersonaResponse con los datos mapeados al español
        """
        # Mapear campos de Decolecta al español
        nombres = data.get("first_name", "")
        apellido_paterno = data.get("first_last_name", "")
        apellido_materno = data.get("second_last_name", "")
        dni = data.get("document_number", "")
        
        # Usar el nombre completo de Decolecta o construir uno
        nombres_completos = data.get("full_name", "")
        if not nombres_completos:
            nombres_completos = f"{apellido_paterno} {apellido_materno} {nombres}".strip()
        
        return PersonaResponse(
            dni=dni,
            nombres=nombres,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            nombres_completos=nombres_completos,
            # Los campos adicionales se mantienen como None por ahora
            # ya que la API básica de Decolecta no los proporciona
        )
    
    def get_api_usage_info(self) -> Dict[str, Any]:
        """
        Obtiene información sobre el uso de la API
        Incluye estadísticas del cache
        
        Returns:
            Información sobre el uso de la API
        """
        cache_stats = cache_service.get_stats()
        
        return {
            "peticiones_usadas": self.request_count,
            "limite_mensual": self.monthly_limit,
            "peticiones_restantes": max(0, self.monthly_limit - self.request_count),
            "porcentaje_usado": (self.request_count / self.monthly_limit) * 100,
            "cache_stats": cache_stats,
            "timeout_segundos": self.request_timeout
        }
    
    def reset_request_count(self) -> None:
        """Resetea el contador de peticiones (útil para testing)"""
        self.request_count = 0
        logger.info("Contador de peticiones reseteado") 