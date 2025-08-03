# Ejemplos de uso con cURL

## 1. Verificar estado del servicio

```bash
curl -X GET http://localhost:8080/email-service/api/v1/contact/health
```

**Respuesta esperada:**
```
Email Microservice is running!
```

## 2. Enviar formulario de contacto válido

```bash
curl -X POST http://localhost:8080/email-service/api/v1/contact/submit \
  -H "Content-Type: application/json" \
  -d '{
    "fullName": "María González López",
    "email": "maria.gonzalez@restaurante-elbueno.com",
    "phone": "+34 91 123 45 67",
    "companyName": "Restaurante El Bueno",
    "interestedPlan": "Plan Premium",
    "message": "Hola, me interesa mucho el plan premium para nuestro restaurante. Tenemos 3 sucursales y necesitamos una solución completa para gestionar inventarios, pedidos y reportes."
  }'
```

**Respuesta esperada:**
```json
{
  "success": true,
  "messageId": "msg_123456789",
  "provider": "Mailtrap"
}
```

## 3. Enviar formulario sin mensaje (opcional)

```bash
curl -X POST http://localhost:8080/email-service/api/v1/contact/submit \
  -H "Content-Type: application/json" \
  -d '{
    "fullName": "Carlos Rodríguez",
    "email": "carlos.rodriguez@cafeteria-central.com",
    "phone": "+34 93 456 78 90",
    "companyName": "Cafetería Central",
    "interestedPlan": "Plan Básico"
  }'
```

## 4. Ejemplo con error de validación

```bash
curl -X POST http://localhost:8080/email-service/api/v1/contact/submit \
  -H "Content-Type: application/json" \
  -d '{
    "fullName": "",
    "email": "email-invalido",
    "phone": "123",
    "companyName": "Empresa",
    "interestedPlan": "Plan"
  }'
```

**Respuesta esperada:**
```json
{
  "success": false,
  "message": "Error de validación",
  "errors": {
    "fullName": "El nombre completo es obligatorio",
    "email": "El formato del correo electrónico no es válido",
    "phone": "El formato del teléfono no es válido"
  }
}
```

## 5. Verificar endpoints de Actuator

```bash
# Estado del servicio
curl -X GET http://localhost:8080/email-service/actuator/health

# Información de la aplicación
curl -X GET http://localhost:8080/email-service/actuator/info

# Métricas del sistema
curl -X GET http://localhost:8080/email-service/actuator/metrics
```

## Configuración de variables de entorno

Antes de ejecutar los ejemplos, asegúrate de configurar las variables de entorno:

```bash
# Windows PowerShell
$env:MAILTRAP_TOKEN="tu-token-de-mailtrap"
$env:OWNER_EMAIL="tu-email@dominio.com"
$env:FROM_EMAIL="noreply@tudominio.com"

# Linux/Mac
export MAILTRAP_TOKEN="tu-token-de-mailtrap"
export OWNER_EMAIL="tu-email@dominio.com"
export FROM_EMAIL="noreply@tudominio.com"
``` 