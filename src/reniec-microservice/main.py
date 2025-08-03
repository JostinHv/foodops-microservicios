import logging
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config.settings import settings
from app.controllers.reniec_controller import router as reniec_router
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.rate_limiter import rate_limit_middleware
from app.exceptions.custom_exceptions import RENIECException
import time


# Configuración de logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager para el ciclo de vida de la aplicación
    """
    # Startup
    logger.info("🚀 Iniciando microservicio RENIEC...")
    logger.info(f"📋 Configuración: RENIEC Microservice v{settings.app_version}")
    logger.info(f"🌐 Servidor: {settings.host}:{settings.port}")
    logger.info(f"🔧 Debug: {settings.debug}")
    logger.info(f"📊 Log Level: {settings.log_level}")
    
    yield
    
    # Shutdown
    logger.info("🛑 Cerrando microservicio RENIEC...")


# Crear aplicación FastAPI
app = FastAPI(
    title=settings.app_name,
    description="Microservicio para consultar datos de RENIEC a través de la API de Decolecta",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agregar middleware personalizado
app.add_middleware(LoggingMiddleware)


@app.middleware("http")
async def add_rate_limiting(request: Request, call_next):
    """
    Middleware para rate limiting
    """
    return await rate_limit_middleware(request, call_next)


@app.exception_handler(RENIECException)
async def reniec_exception_handler(request: Request, exc: RENIECException):
    """
    Manejador de excepciones personalizadas de RENIEC
    """
    logger.error(f"RENIEC Exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "RENIEC_ERROR",
            "message": str(exc.detail),
            "status_code": exc.status_code,
            "timestamp": time.time()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Manejador de excepciones generales
    """
    logger.error(f"Error inesperado: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": "Error interno del servidor",
            "status_code": 500,
            "timestamp": time.time()
        }
    )


@app.get("/", tags=["Health"])
async def root():
    """
    Endpoint raíz con información del servicio
    """
    return {
        "message": "RENIEC Microservice API",
        "version": settings.app_version,
        "status": "running",
        "docs": "/docs",
        "health": "/api/v1/reniec/health"
    }


@app.get("/docs", include_in_schema=False)
async def redirect_docs():
    """
    Redirección a la documentación
    """
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")


# Registrar routers
app.include_router(reniec_router)


if __name__ == "__main__":
    logger.info("🚀 Iniciando servidor...")
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
