import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Configuración de la aplicación usando Pydantic Settings
    """
    
    # Configuración de la aplicación
    app_name: str = "RENIEC Microservice"
    app_version: str = "1.0.0"
    app_description: str = "Microservicio para consultar datos de RENIEC"
    
    # Configuración del servidor
    host: str = "localhost"  # Cambiado a localhost para evitar problemas DNS
    port: int = 8080  # Cambiado a puerto 8080 como Laravel/Spring
    debug: bool = False
    
    # Configuración de la API de Decolecta
    decolecta_api_token: Optional[str] = None
    decolecta_base_url: str = "https://api.decolecta.com"
    
    # Configuración de logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Instancia global de configuración
settings = Settings() 