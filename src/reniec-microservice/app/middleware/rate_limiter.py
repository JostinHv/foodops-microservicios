import time
import logging
from typing import Dict, Tuple
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from collections import defaultdict
import threading

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Rate limiter simple en memoria para proteger la API
    """
    
    def __init__(self, requests_per_minute: int = 60, requests_per_hour: int = 1000):
        """
        Inicializa el rate limiter
        
        Args:
            requests_per_minute: Máximo de peticiones por minuto por IP
            requests_per_hour: Máximo de peticiones por hora por IP
        """
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self.minute_requests: Dict[str, list] = defaultdict(list)
        self.hour_requests: Dict[str, list] = defaultdict(list)
        self.lock = threading.Lock()
    
    def _get_client_ip(self, request: Request) -> str:
        """
        Obtiene la IP del cliente
        
        Args:
            request: Request de FastAPI
            
        Returns:
            IP del cliente
        """
        # Intentar obtener IP real detrás de proxy
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        return request.client.host if request.client else "unknown"
    
    def _cleanup_old_requests(self, ip: str) -> None:
        """
        Limpia peticiones antiguas
        
        Args:
            ip: IP del cliente
        """
        current_time = time.time()
        
        # Limpiar peticiones de hace más de 1 minuto
        self.minute_requests[ip] = [
            req_time for req_time in self.minute_requests[ip]
            if current_time - req_time < 60
        ]
        
        # Limpiar peticiones de hace más de 1 hora
        self.hour_requests[ip] = [
            req_time for req_time in self.hour_requests[ip]
            if current_time - req_time < 3600
        ]
    
    def is_allowed(self, request: Request) -> Tuple[bool, Dict[str, any]]:
        """
        Verifica si la petición está permitida
        
        Args:
            request: Request de FastAPI
            
        Returns:
            Tuple con (permitido, información del rate limit)
        """
        client_ip = self._get_client_ip(request)
        current_time = time.time()
        
        with self.lock:
            # Limpiar peticiones antiguas
            self._cleanup_old_requests(client_ip)
            
            # Verificar límite por minuto
            minute_count = len(self.minute_requests[client_ip])
            if minute_count >= self.requests_per_minute:
                return False, {
                    "error": "RATE_LIMIT_EXCEEDED",
                    "message": "Demasiadas peticiones por minuto",
                    "limit_type": "per_minute",
                    "limit": self.requests_per_minute,
                    "current": minute_count,
                    "retry_after": 60
                }
            
            # Verificar límite por hora
            hour_count = len(self.hour_requests[client_ip])
            if hour_count >= self.requests_per_hour:
                return False, {
                    "error": "RATE_LIMIT_EXCEEDED",
                    "message": "Demasiadas peticiones por hora",
                    "limit_type": "per_hour",
                    "limit": self.requests_per_hour,
                    "current": hour_count,
                    "retry_after": 3600
                }
            
            # Registrar petición
            self.minute_requests[client_ip].append(current_time)
            self.hour_requests[client_ip].append(current_time)
            
            return True, {
                "remaining_minute": self.requests_per_minute - minute_count - 1,
                "remaining_hour": self.requests_per_hour - hour_count - 1,
                "reset_minute": 60,
                "reset_hour": 3600
            }
    
    def get_stats(self) -> Dict[str, any]:
        """
        Obtiene estadísticas del rate limiter
        
        Returns:
            Estadísticas del rate limiter
        """
        with self.lock:
            total_minute_requests = sum(len(requests) for requests in self.minute_requests.values())
            total_hour_requests = sum(len(requests) for requests in self.hour_requests.values())
            unique_ips = len(self.minute_requests)
            
            return {
                "total_minute_requests": total_minute_requests,
                "total_hour_requests": total_hour_requests,
                "unique_ips": unique_ips,
                "limits": {
                    "per_minute": self.requests_per_minute,
                    "per_hour": self.requests_per_hour
                }
            }


# Instancia global del rate limiter
rate_limiter = RateLimiter()


async def rate_limit_middleware(request: Request, call_next):
    """
    Middleware para aplicar rate limiting
    
    Args:
        request: Request de FastAPI
        call_next: Función para continuar el procesamiento
        
    Returns:
        Response de FastAPI
    """
    # Aplicar rate limiting solo a endpoints de RENIEC
    if request.url.path.startswith("/api/v1/reniec"):
        is_allowed, rate_limit_info = rate_limiter.is_allowed(request)
        
        if not is_allowed:
            logger.warning(f"Rate limit excedido para IP: {rate_limiter._get_client_ip(request)}")
            return JSONResponse(
                status_code=429,
                content={
                    "error": rate_limit_info["error"],
                    "message": rate_limit_info["message"],
                    "status_code": 429,
                    "details": rate_limit_info
                }
            )
        
        # Agregar headers de rate limit a la respuesta
        response = await call_next(request)
        response.headers["X-RateLimit-Limit-Minute"] = str(rate_limiter.requests_per_minute)
        response.headers["X-RateLimit-Limit-Hour"] = str(rate_limiter.requests_per_hour)
        response.headers["X-RateLimit-Remaining-Minute"] = str(rate_limit_info["remaining_minute"])
        response.headers["X-RateLimit-Remaining-Hour"] = str(rate_limit_info["remaining_hour"])
        response.headers["X-RateLimit-Reset-Minute"] = str(rate_limit_info["reset_minute"])
        response.headers["X-RateLimit-Reset-Hour"] = str(rate_limit_info["reset_hour"])
        
        return response
    
    return await call_next(request) 