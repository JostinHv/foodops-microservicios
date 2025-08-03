# Email Microservice

Microservicio de email robusto y escalable para aplicaciones multitenant de gestión de restaurantes.

## 🚀 Características

- **Arquitectura Hexagonal**: Implementa principios SOLID y arquitectura limpia
- **Múltiples Proveedores**: Soporte para Mailtrap, Google, y otros proveedores de email
- **Validación Robusta**: Validación completa de formularios de contacto
- **Logging Detallado**: Logging estructurado para monitoreo y debugging
- **Configuración Flexible**: Soporte para diferentes entornos (dev, prod)
- **API REST**: Endpoints RESTful para integración con aplicaciones frontend

## 🏗️ Arquitectura

```
src/main/java/com/foodops/emailmicroservice/
├── domain/                    # Lógica de dominio
│   ├── model/                # Modelos de dominio
│   └── port/                 # Puertos (interfaces)
├── application/               # Casos de uso
│   └── service/              # Servicios de aplicación
└── infrastructure/            # Adaptadores y configuración
    ├── adapter/              # Adaptadores para proveedores externos
    ├── controller/            # Controladores REST
    └── exception/             # Manejo de excepciones
```

## 📋 Requisitos

- Java 21+
- Maven 3.6+
- Token de Mailtrap

## 🛠️ Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd email-microservice
   ```

2. **Configurar variables de entorno**
   ```bash
   export MAILTRAP_TOKEN="tu-token-de-mailtrap"
   export OWNER_EMAIL="tu-email@dominio.com"
   export FROM_EMAIL="noreply@tudominio.com"
   ```

3. **Compilar y ejecutar**
   ```bash
   mvn clean install
   mvn spring-boot:run
   ```

## 🔧 Configuración

### Variables de Entorno

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `MAILTRAP_TOKEN` | Token de autenticación de Mailtrap | `your-mailtrap-token-here` |
| `OWNER_EMAIL` | Email del propietario del multitenant | `admin@foodops.com` |
| `FROM_EMAIL` | Email de origen para los envíos | `noreply@foodops.com` |

### Perfiles de Spring

- **dev**: Configuración para desarrollo
- **prod**: Configuración para producción

## 📡 API Endpoints

### POST `/api/v1/contact/submit`

Envía un formulario de contacto al propietario del multitenant.

**Request Body:**
```json
{
  "fullName": "Juan Pérez",
  "email": "juan.perez@empresa.com",
  "phone": "+34 123 456 789",
  "companyName": "Restaurante El Bueno",
  "interestedPlan": "Plan Premium",
  "message": "Me interesa conocer más sobre el plan premium"
}
```

**Response:**
```json
{
  "success": true,
  "messageId": "msg_123456789",
  "provider": "Mailtrap"
}
```

### GET `/api/v1/contact/health`

Verifica el estado del servicio.

**Response:**
```
Email Microservice is running!
```

## 📧 Formulario de Contacto

El microservicio procesa formularios de contacto con la siguiente información:

- **Nombre completo** (obligatorio)
- **Correo electrónico** (obligatorio)
- **Teléfono** (obligatorio)
- **Nombre de la empresa** (obligatorio)
- **Plan de interés** (obligatorio)
- **Mensaje** (opcional)

## 🔌 Proveedores de Email

### Mailtrap (Actual)

El microservicio está configurado para usar Mailtrap como proveedor principal.

### Extensibilidad

Para agregar nuevos proveedores:

1. Crear un nuevo adaptador en `infrastructure/adapter/`
2. Implementar la interfaz `EmailService`
3. Configurar el bean en la configuración de Spring

## 🧪 Testing

```bash
# Ejecutar tests unitarios
mvn test

# Ejecutar tests de integración
mvn verify
```

## 📊 Monitoreo

El microservicio incluye endpoints de Actuator para monitoreo:

- `/actuator/health`: Estado del servicio
- `/actuator/info`: Información de la aplicación
- `/actuator/metrics`: Métricas del sistema

