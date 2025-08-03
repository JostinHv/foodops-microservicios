# 📧 Email Microservice

## 📋 Descripción

Microservicio de envío de emails desarrollado con Spring Boot. Proporciona funcionalidad de envío de correos electrónicos para formularios de contacto y notificaciones del sistema FoodOps.

## 🚀 Características

- **Spring Boot 3.5.4**: Framework moderno y robusto
- **Validación de Datos**: Validación automática con Bean Validation
- **Configuración Externa**: Variables de entorno para configuración
- **Health Checks**: Endpoints de verificación de estado
- **Logging Detallado**: Sistema de logging completo
- **Documentación Automática**: Swagger UI integrado
- **Actuator**: Métricas y monitoreo
- **Context Path**: Configuración `/email-service`

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    Email Microservice                       │
├─────────────────────────────────────────────────────────────┤
│     ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│     │   Spring    │  │   Email     │  │   Contact   │       │
│     │   Boot      │  │   Service   │  │   Form      │       │
│     └─────────────┘  └─────────────┘  └─────────────┘       │
│            │                │                │              │
│            └────────────────┼────────────────┘              │
│                             │                               │
│  ┌──────────────────────────────────────────────────────┐   │ 
│  │                   Mailtrap                           │   │
│  │                     SMTP                             │   │
│  │                 (Email Service)                      │   │
│  └───────────────────────┴──────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## 🛠️ Requisitos

- Java 21+
- Maven 3.6+
- Cuenta de Mailtrap (para testing)
- Docker (opcional)

## 📦 Instalación

### 1. Clonar y Configurar

```bash
# Clonar el repositorio
git clone <repository-url>
cd email-microservice

# Compilar proyecto
mvn clean install
```

### 2. Configuración del Entorno

```bash
# Configurar variables de entorno
export MAILTRAP_HOST=smtp.mailtrap.io
export MAILTRAP_PORT=2525
export MAILTRAP_USERNAME=your_username
export MAILTRAP_PASSWORD=your_password
export OWNER_EMAIL=admin@foodops.com
export FROM_EMAIL=noreply@foodops.com
```

### 3. Archivo de Configuración

Crear `application.properties` o usar variables de entorno:

```properties
# Configuración del servidor
server.port=8080
server.servlet.context-path=/email-service

# Configuración de email
spring.mail.host=${MAILTRAP_HOST:smtp.mailtrap.io}
spring.mail.port=${MAILTRAP_PORT:2525}
spring.mail.username=${MAILTRAP_USERNAME:your_username}
spring.mail.password=${MAILTRAP_PASSWORD:your_password}
spring.mail.properties.mail.smtp.auth=true
spring.mail.properties.mail.smtp.starttls.enable=true

# Configuración de la aplicación
app.email.owner=${OWNER_EMAIL:admin@foodops.com}
app.email.from=${FROM_EMAIL:noreply@foodops.com}

# Logging
logging.level.com.foodops=INFO
logging.level.org.springframework.mail=DEBUG
```

## 🏃‍♂️ Ejecución

### Desarrollo

```bash
# Ejecutar con Maven
mvn spring-boot:run

# O con Java directamente
java -jar target/email-microservice-0.0.1-SNAPSHOT.jar
```

### Producción

```bash
# Ejecutar JAR
java -jar target/email-microservice-0.0.1-SNAPSHOT.jar \
  --spring.profiles.active=prod
```

### Docker

```bash
# Construir imagen
docker build -t email-microservice:latest .

# Ejecutar contenedor
docker run -p 8080:8080 \
  -e MAILTRAP_HOST=smtp.mailtrap.io \
  -e MAILTRAP_USERNAME=your_username \
  -e MAILTRAP_PASSWORD=your_password \
  email-microservice:latest
```

## 📡 Endpoints

### Health Check

```http
GET /email-service/api/v1/contact/health
```

**Respuesta:**
```json
{
  "status": "UP",
  "service": "email-microservice",
  "version": "0.0.1-SNAPSHOT",
  "timestamp": "2025-08-02T16:30:00Z"
}
```

### Enviar Formulario de Contacto

```http
POST /email-service/api/v1/contact/submit
Content-Type: application/json

{
  "fullName": "Juan Pérez",
  "email": "juan.perez@empresa.com",
  "phone": "+34 123 456 789",
  "companyName": "Restaurante El Bueno",
  "interestedPlan": "Plan Premium",
  "message": "Me interesa conocer más sobre el plan premium"
}
```

**Respuesta exitosa (200):**
```json
{
  "success": true,
  "message": "Formulario enviado exitosamente",
  "timestamp": "2025-08-02T16:30:00Z"
}
```

**Respuesta error (400):**
```json
{
  "success": false,
  "message": "Datos de formulario inválidos",
  "errors": [
    "El nombre completo es obligatorio",
    "El email debe tener un formato válido"
  ]
}
```

## 🔧 Configuración

### Variables de Entorno

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `MAILTRAP_HOST` | Servidor SMTP | smtp.mailtrap.io |
| `MAILTRAP_PORT` | Puerto SMTP | 2525 |
| `MAILTRAP_USERNAME` | Usuario SMTP | - |
| `MAILTRAP_PASSWORD` | Contraseña SMTP | - |
| `OWNER_EMAIL` | Email del propietario | admin@foodops.com |
| `FROM_EMAIL` | Email remitente | noreply@foodops.com |

### Validaciones

El servicio incluye validaciones estrictas:

- **fullName**: 2-100 caracteres, obligatorio
- **email**: Formato válido, obligatorio
- **phone**: Formato internacional, obligatorio
- **companyName**: 2-100 caracteres, obligatorio
- **interestedPlan**: 2-100 caracteres, obligatorio
- **message**: Opcional, máximo 1000 caracteres

## 🧪 Testing

### Tests Unitarios

```bash
# Ejecutar tests
mvn test

# Tests específicos
mvn test -Dtest=ContactFormTest
mvn test -Dtest=EmailServiceTest
```

### Tests de Integración

```bash
# Tests de integración
mvn test -Dtest=ContactControllerIntegrationTest
```

### Pruebas Manuales

```bash
# Health check
curl http://localhost:8080/email-service/api/v1/contact/health

# Enviar formulario
curl -X POST http://localhost:8080/email-service/api/v1/contact/submit \
  -H "Content-Type: application/json" \
  -d '{
    "fullName": "Test User",
    "email": "test@example.com",
    "phone": "+1234567890",
    "companyName": "Test Company",
    "interestedPlan": "Plan Básico",
    "message": "Test message"
  }'
```

## 📊 Monitoreo

### Actuator Endpoints

```bash
# Health check
curl http://localhost:8080/email-service/actuator/health

# Info de la aplicación
curl http://localhost:8080/email-service/actuator/info

# Métricas
curl http://localhost:8080/email-service/actuator/metrics
```

### Logs

```bash
# Ver logs en tiempo real
tail -f logs/email-microservice.log

# Logs específicos
grep "EMAIL_SENT" logs/email-microservice.log
grep "ERROR" logs/email-microservice.log
```

## 🐳 Docker

### Dockerfile

```dockerfile
FROM openjdk:21-jdk-slim
COPY target/email-microservice-0.0.1-SNAPSHOT.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app.jar"]
```

### Docker Compose

```yaml
version: '3.8'
services:
  email-microservice:
    build: .
    ports:
      - "8080:8080"
    environment:
      - MAILTRAP_HOST=smtp.mailtrap.io
      - MAILTRAP_USERNAME=${MAILTRAP_USERNAME}
      - MAILTRAP_PASSWORD=${MAILTRAP_PASSWORD}
      - OWNER_EMAIL=admin@foodops.com
      - FROM_EMAIL=noreply@foodops.com
    restart: unless-stopped
```

## ☁️ Kubernetes

### Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: email-microservice
spec:
  replicas: 3
  selector:
    matchLabels:
      app: email-microservice
  template:
    metadata:
      labels:
        app: email-microservice
    spec:
      containers:
      - name: email-microservice
        image: gcr.io/project-id/email-microservice:latest
        ports:
        - containerPort: 8080
        env:
        - name: MAILTRAP_HOST
          value: "smtp.mailtrap.io"
        - name: MAILTRAP_USERNAME
          valueFrom:
            secretKeyRef:
              name: email-secrets
              key: mailtrap-username
        - name: MAILTRAP_PASSWORD
          valueFrom:
            secretKeyRef:
              name: email-secrets
              key: mailtrap-password
        livenessProbe:
          httpGet:
            path: /email-service/api/v1/contact/health
            port: 8080
        readinessProbe:
          httpGet:
            path: /email-service/api/v1/contact/health
            port: 8080
```

## 🔒 Seguridad

### Configuración SMTP

- **Autenticación**: SMTP AUTH habilitado
- **TLS**: STARTTLS habilitado
- **Credenciales**: Variables de entorno seguras
- **Rate Limiting**: Protección contra spam

### Validación de Entrada

- **Sanitización**: Limpieza de datos de entrada
- **Validación**: Bean Validation con anotaciones
- **Logging**: Registro de intentos de envío
- **Error Handling**: Manejo seguro de errores

## 🚨 Troubleshooting

### Problemas Comunes

#### 1. **Error de Conexión SMTP**
```bash
# Verificar configuración SMTP
curl -v telnet://smtp.mailtrap.io:2525

# Verificar credenciales
echo $MAILTRAP_USERNAME
echo $MAILTRAP_PASSWORD
```

#### 2. **Error de Validación**
```bash
# Verificar logs de validación
grep "VALIDATION_ERROR" logs/email-microservice.log

# Probar con datos válidos
curl -X POST http://localhost:8080/email-service/api/v1/contact/submit \
  -H "Content-Type: application/json" \
  -d '{
    "fullName": "Test User",
    "email": "test@example.com",
    "phone": "+1234567890",
    "companyName": "Test Company",
    "interestedPlan": "Plan Básico"
  }'
```

#### 3. **Error de Context Path**
```bash
# Verificar que el context path esté configurado
curl http://localhost:8080/email-service/api/v1/contact/health

# Sin context path (debería fallar)
curl http://localhost:8080/api/v1/contact/health
```

### Comandos de Diagnóstico

```bash
# Verificar estado del servicio
curl http://localhost:8080/email-service/actuator/health

# Ver configuración
curl http://localhost:8080/email-service/actuator/env

# Ver logs del contenedor
docker logs email-microservice

# Ver logs de Kubernetes
kubectl logs deployment/email-microservice
```

## 📚 Documentación

- **Swagger UI**: http://localhost:8080/email-service/swagger-ui.html
- **Actuator**: http://localhost:8080/email-service/actuator
- **Health Check**: http://localhost:8080/email-service/api/v1/contact/health

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 📞 Soporte

Para soporte técnico:
- Crear issue en GitHub
- Contactar al equipo de desarrollo
- Revisar documentación de Spring Boot

---

**Nota**: Este microservicio está optimizado para el envío de formularios de contacto. Para uso en producción, considera configurar un servicio de email más robusto como SendGrid o Amazon SES.

