import time
import logging
from typing import Optional, Dict, Any
from threading import Lock
from dataclasses import dataclass
from app.models.request_models import PersonaResponse

logger = logging.getLogger(__name__)


@dataclass
class CacheEntry:
    """Entrada del cache con datos y timestamp"""
    data: Any
    timestamp: float
    ttl: int = 1800  # 30 minutos en segundos


class MemoryCacheService:
    """
    Servicio de cache en memoria con TTL de 30 minutos
    Thread-safe para uso en producción
    """
    
    def __init__(self, default_ttl: int = 1800):
        """
        Inicializa el cache en memoria
        
        Args:
            default_ttl: Tiempo de vida por defecto en segundos (30 minutos)
        """
        self._cache: Dict[str, CacheEntry] = {}
        self._lock = Lock()
        self.default_ttl = default_ttl
        self.stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "evictions": 0
        }
    
    def get(self, key: str) -> Optional[PersonaResponse]:
        """
        Obtiene un valor del cache
        
        Args:
            key: Clave del cache (DNI)
            
        Returns:
            Datos de la persona o None si no existe o expiró
        """
        with self._lock:
            if key not in self._cache:
                self.stats["misses"] += 1
                return None
            
            entry = self._cache[key]
            current_time = time.time()
            
            # Verificar si expiró
            if current_time - entry.timestamp > entry.ttl:
                del self._cache[key]
                self.stats["evictions"] += 1
                self.stats["misses"] += 1
                logger.debug(f"Cache entry expirada para DNI: {key}")
                return None
            
            self.stats["hits"] += 1
            logger.debug(f"Cache hit para DNI: {key}")
            return entry.data
    
    def set(self, key: str, value: PersonaResponse, ttl: Optional[int] = None) -> None:
        """
        Almacena un valor en el cache
        
        Args:
            key: Clave del cache (DNI)
            value: Datos de la persona
            ttl: Tiempo de vida en segundos (opcional)
        """
        with self._lock:
            cache_ttl = ttl if ttl is not None else self.default_ttl
            self._cache[key] = CacheEntry(
                data=value,
                timestamp=time.time(),
                ttl=cache_ttl
            )
            self.stats["sets"] += 1
            logger.debug(f"Cache set para DNI: {key} con TTL: {cache_ttl}s")
    
    def delete(self, key: str) -> bool:
        """
        Elimina una entrada del cache
        
        Args:
            key: Clave del cache
            
        Returns:
            True si se eliminó, False si no existía
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                logger.debug(f"Cache delete para DNI: {key}")
                return True
            return False
    
    def clear(self) -> None:
        """Limpia todo el cache"""
        with self._lock:
            self._cache.clear()
            logger.info("Cache limpiado completamente")
    
    def cleanup_expired(self) -> int:
        """
        Limpia entradas expiradas
        
        Returns:
            Número de entradas eliminadas
        """
        with self._lock:
            current_time = time.time()
            expired_keys = [
                key for key, entry in self._cache.items()
                if current_time - entry.timestamp > entry.ttl
            ]
            
            for key in expired_keys:
                del self._cache[key]
                self.stats["evictions"] += 1
            
            if expired_keys:
                logger.debug(f"Limpiadas {len(expired_keys)} entradas expiradas del cache")
            
            return len(expired_keys)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del cache
        
        Returns:
            Estadísticas del cache
        """
        with self._lock:
            total_requests = self.stats["hits"] + self.stats["misses"]
            hit_rate = (self.stats["hits"] / total_requests * 100) if total_requests > 0 else 0
            
            return {
                "total_entries": len(self._cache),
                "hits": self.stats["hits"],
                "misses": self.stats["misses"],
                "sets": self.stats["sets"],
                "evictions": self.stats["evictions"],
                "hit_rate_percent": round(hit_rate, 2),
                "total_requests": total_requests
            }
    
    def is_cached(self, key: str) -> bool:
        """
        Verifica si una clave existe en el cache (sin expiración)
        
        Args:
            key: Clave del cache
            
        Returns:
            True si existe y no ha expirado
        """
        with self._lock:
            if key not in self._cache:
                return False
            
            entry = self._cache[key]
            current_time = time.time()
            
            return current_time - entry.timestamp <= entry.ttl


# Instancia global del cache
cache_service = MemoryCacheService() 