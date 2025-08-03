# 🔍 RENIEC Microservice

## 📋 Descripción

Microservicio de consulta de datos personales de RENIEC a través de la API de Decolecta. Optimizado para minimizar el consumo de peticiones (2/1000 mensuales) con cache en memoria y validación estricta.

## 🚀 Características

- **FastAPI**: Framework moderno y rápido
- **Cache en Memoria**: TTL de 30 minutos para optimizar peticiones
- **Rate Limiting**: Protección por IP (60/min, 1000/hora)
- **Validación Estricta**: Evita peticiones innecesarias
- **Logging Detallado**: Monitoreo completo de operaciones
- **Health Checks**: Endpoints de verificación de estado
- **Documentación Automática**: Swagger UI en `/docs`

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                    RENIEC Microservice                  │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │   FastAPI   │  │   Cache     │  │ Rate Limiter│      │
│  │   Server    │  │   Memory    │  │   Per IP    │      │
│  └─────────────┘  └─────────────┘  └─────────────┘      │
│         │                │                │             │
│         └────────────────┼────────────────┘             │
│                          │                              │
│  ┌───────────────────────┼─────────────────────────┐    │
│  │                   Decolecta                     │    │
│  │                      API                        │    │
│  │                 (RENIEC Data)                   │    │
│  └───────────────────────────────────────── ───────┘    │
└─────────────────────────────────────────────────────────┘
```

## 🛠️ Requisitos

- Python 3.12
- pip
- Token de API de Decolecta

## 📦 Instalación

### 1. Clonar y Configurar

```bash
# Clonar el repositorio
git clone <repository-url>
cd reniec-microservice

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp env.example .env
# Editar .env con tu token de Decolecta
```

### 2. Variables de Entorno

```env
# Token de API de Decolecta (obligatorio)
DECOLECTA_API_TOKEN=your_api_token_here

# Configuración del servidor
HOST=localhost
PORT=8080
DEBUG=false

# Configuración de logging
LOG_LEVEL=INFO

# Configuración de la API de Decolecta
DECOLECTA_BASE_URL=https://api.decolecta.com
```

## 🏃‍♂️ Ejecución

### Desarrollo

```bash
# Ejecutar en modo desarrollo
python main.py

# O con uvicorn directamente
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

### Producción

```bash
# Ejecutar con uvicorn
uvicorn main:app --host 0.0.0.0 --port 8080 --workers 1
```

### Docker

```bash
# Construir imagen
docker build -t reniec-microservice:latest .

# Ejecutar contenedor
docker run -p 8080:8080 --env-file .env reniec-microservice:latest
```

## 📡 Endpoints

### Health Check

```http
GET /api/v1/reniec/health
```

**Respuesta:**
```json
{
  "status": "healthy",
  "service": "reniec-microservice",
  "version": "1.0.0",
  "api_provider": "Decolecta",
  "optimizacion": "Validación estricta para ahorrar peticiones",
  "cache": "Habilitado (30 minutos TTL)",
  "rate_limiting": "Habilitado"
}
```

### Consulta de Persona

```http
GET /api/v1/reniec/persona/{dni}
```

**Parámetros:**
- `dni`: Número de DNI de 8 dígitos (requerido)

**Respuesta exitosa (200):**
```json
{
  "dni": "12345678",
  "nombres": "JUAN CARLOS",
  "apellido_paterno": "PEREZ",
  "apellido_materno": "GARCIA",
  "nombres_completos": "JUAN CARLOS PEREZ GARCIA"
}
```

**Respuesta error (400):**
```json
{
  "error": "DNI_INVALIDO",
  "message": "El DNI debe contener exactamente 8 dígitos numéricos y no puede empezar con 0",
  "status_code": 400,
  "detalles": {
    "dni_proporcionado": "1234567",
    "longitud": 7,
    "es_numerico": true
  }
}
```

**Respuesta error (404):**
```json
{
  "error": "PERSONA_NO_ENCONTRADA",
  "message": "No se encontraron datos para el DNI: 12345678",
  "status_code": 404,
  "detalles": {
    "dni": "12345678"
  }
}
```

### Monitoreo de API

```http
GET /api/v1/reniec/api-usage
```

**Respuesta:**
```json
{
  "api_provider": "Decolecta",
  "limite_mensual": 1000,
  "peticiones_usadas": 2,
  "peticiones_restantes": 998,
  "porcentaje_usado": "0.2%",
  "timeout_segundos": 15,
  "cache_stats": {
    "total_entries": 5,
    "hit_rate_percent": 75.5,
    "hits": 15,
    "misses": 5
  },
  "recomendacion": "Validar DNI antes de consultar para optimizar uso"
}
```

### Estadísticas de Cache

```http
GET /api/v1/reniec/cache/stats
```

**Respuesta:**
```json
{
  "cache_type": "Memory Cache",
  "ttl_minutos": 30,
  "total_entries": 5,
  "hit_rate_percent": 75.5,
  "hits": 15,
  "misses": 5,
  "sets": 5,
  "evictions": 0,
  "total_requests": 20
}
```

### Limpiar Cache

```http
DELETE /api/v1/reniec/cache/clear
```

**Respuesta:**
```json
{
  "message": "Cache limpiado exitosamente",
  "status": "success",
  "timestamp": 1703123456.789
}
```

### Estadísticas de Rate Limiting

```http
GET /api/v1/reniec/rate-limit/stats
```

**Respuesta:**
```json
{
  "rate_limiting": "Habilitado",
  "total_minute_requests": 25,
  "total_hour_requests": 150,
  "unique_ips": 3,
  "limits": {
    "per_minute": 60,
    "per_hour": 1000
  }
}
```

## 🔧 Configuración

### Validación de DNI

El servicio incluye validación estricta para evitar peticiones innecesarias:

- ✅ Exactamente 8 dígitos numéricos
- ✅ No puede empezar con 0
- ✅ No puede ser una secuencia de números repetidos
- ❌ No acepta letras o caracteres especiales

### Cache

- **Tipo**: Memoria en proceso
- **TTL**: 30 minutos por defecto
- **Thread-safe**: Seguro para múltiples workers
- **Estadísticas**: Hit rate y métricas disponibles

### Rate Limiting

- **Por minuto**: 60 peticiones por IP
- **Por hora**: 1000 peticiones por IP
- **Headers**: Incluye información de límites en respuestas
- **Cleanup**: Limpieza automática de registros antiguos

## 🧪 Testing

### Script de Pruebas

```bash
# Ejecutar pruebas automáticas
python test_simple.py
```

### Pruebas Manuales

```bash
# Health check
curl http://localhost:8080/api/v1/reniec/health

# Consulta de persona
curl http://localhost:8080/api/v1/reniec/persona/12345678

# Estadísticas de cache
curl http://localhost:8080/api/v1/reniec/cache/stats

# Monitoreo de API
curl http://localhost:8080/api/v1/reniec/api-usage
```

## 📊 Monitoreo

### Logs

El servicio genera logs detallados:

```bash
# Ver logs en tiempo real
tail -f logs/reniec-microservice.log
```

### Métricas Disponibles

- **Uso de API**: Peticiones consumidas vs límite
- **Cache**: Hit rate, entradas, evicciones
- **Rate Limiting**: Peticiones por IP, límites
- **Performance**: Tiempo de respuesta, timeouts

## 🐳 Docker

### Construir Imagen

```bash
docker build -t reniec-microservice:latest .
```

### Ejecutar Contenedor

```bash
docker run -d \
  --name reniec-microservice \
  -p 8080:8080 \
  --env-file .env \
  reniec-microservice:latest
```

### Docker Compose

```yaml
version: '3.8'
services:
  reniec-microservice:
    build: .
    ports:
      - "8080:8080"
    environment:
      - DECOLECTA_API_TOKEN=${DECOLECTA_API_TOKEN}
      - HOST=0.0.0.0
      - PORT=8080
      - DEBUG=false
    restart: unless-stopped
```

## ☁️ Kubernetes

### Deployment

```bash
# Aplicar configuración
kubectl apply -f k8s/

# Verificar estado
kubectl get pods -n reniec-microservice
kubectl get services -n reniec-microservice

# Ver logs
kubectl logs -f deployment/reniec-microservice -n reniec-microservice
```

### Configuración de Secret

```bash
# Crear secret con token de API
kubectl create secret generic reniec-secrets \
  --from-literal=DECOLECTA_API_TOKEN=your_token_here \
  -n reniec-microservice
```

## 🔒 Seguridad

### Rate Limiting

- Protección contra abuso por IP
- Límites configurables por minuto/hora
- Headers informativos en respuestas

### Validación

- Validación estricta de entrada
- Sanitización de datos
- Prevención de inyección

### Logging

- Logs estructurados
- Información de auditoría
- Sin datos sensibles en logs

## 🚨 Troubleshooting

### Problemas Comunes

#### 1. **Error de Conexión con Decolecta**
```bash
# Verificar token de API
echo $DECOLECTA_API_TOKEN

# Verificar conectividad
curl -H "Authorization: Bearer $DECOLECTA_API_TOKEN" \
  https://api.decolecta.com/v1/reniec/dni?numero=12345678
```

#### 2. **Cache No Funciona**
```bash
# Verificar estadísticas de cache
curl http://localhost:8080/api/v1/reniec/cache/stats

# Limpiar cache
curl -X DELETE http://localhost:8080/api/v1/reniec/cache/clear
```

#### 3. **Rate Limiting Muy Restrictivo**
```bash
# Verificar estadísticas de rate limiting
curl http://localhost:8080/api/v1/reniec/rate-limit/stats
```

### Comandos de Diagnóstico

```bash
# Verificar estado del servicio
curl http://localhost:8080/api/v1/reniec/health

# Ver uso de API
curl http://localhost:8080/api/v1/reniec/api-usage

# Ver logs del contenedor
docker logs reniec-microservice

# Ver logs de Kubernetes
kubectl logs deployment/reniec-microservice -n reniec-microservice
```

## 📚 Documentación

- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc
- **Health Check**: http://localhost:8080/api/v1/reniec/health

## 🤝 Contribución

1. Fork el repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o preguntas:

- **Issues**: Crear issue en GitHub
- **Documentación**: `/docs` endpoint
- **Logs**: Verificar logs del servicio

---

**Nota**: Este microservicio está optimizado para minimizar el consumo de peticiones de la API de Decolecta. Se recomienda implementar validación del lado del cliente antes de hacer peticiones. 