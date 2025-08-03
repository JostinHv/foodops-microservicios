import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware para logging de peticiones HTTP
    """
    
    async def dispatch(self, request: Request, call_next):
        """
        Procesa la petición y registra información de logging
        """
        start_time = time.time()
        
        # Obtener información de la petición
        method = request.method
        url = str(request.url)
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        
        # Log de inicio de petición
        logger.info(
            f"Iniciando petición: {method} {url} - IP: {client_ip} - User-Agent: {user_agent}"
        )
        
        try:
            # Procesar la petición
            response = await call_next(request)
            
            # Calcular tiempo de respuesta
            process_time = time.time() - start_time
            
            # Log de respuesta exitosa
            logger.info(
                f"Petición completada: {method} {url} - Status: {response.status_code} - "
                f"Tiempo: {process_time:.4f}s"
            )
            
            # Agregar header con tiempo de respuesta
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            # Log de error
            process_time = time.time() - start_time
            logger.error(
                f"Error en petición: {method} {url} - Error: {str(e)} - "
                f"Tiempo: {process_time:.4f}s"
            )
            raise 