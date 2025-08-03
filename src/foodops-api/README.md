# 🍽️ FoodOps API

## 📋 Descripción

Aplicación web completa de gestión de restaurantes desarrollada con Laravel. Sistema multi-tenant que incluye gestión de mesas, órdenes, facturación, personal y administración completa.

## 🚀 Características

- **Multi-tenant**: Sistema de múltiples restaurantes
- **Roles y Permisos**: Super Admin, Admin Tenant, Gerente, Mesero, Cajero, Cocinero
- **Gestión de Mesas**: Reservas, estados, asignación
- **Órdenes**: Creación, seguimiento, estados
- **Facturación**: Generación de facturas, métodos de pago
- **Personal**: Gestión de empleados y asignaciones
- **Reportes**: Estadísticas y análisis
- **Integración**: Microservicios de email y RENIEC

## 🛠️ Requisitos

- PHP 8.2
- Composer
- MySQL/PostgreSQL
- Node.js (para assets)

## 📦 Instalación

### 1. Clonar y Configurar

```bash
# Clonar el repositorio
git clone <repository-url>
cd foodops-api

# Instalar dependencias PHP
composer install

# Instalar dependencias Node.js
npm install
```

### 2. Configuración del Entorno

```bash
# Copiar archivo de configuración
cp .env.example .env

# Generar clave de aplicación
php artisan key:generate

# Configurar base de datos en .env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=foodops
DB_USERNAME=root
DB_PASSWORD=
```

### 3. Base de Datos

```bash
# Ejecutar migraciones
php artisan migrate

# Ejecutar seeders
php artisan db:seed

# Crear enlaces simbólicos
php artisan storage:link
```

### 4. Configuración de Microservicios

```bash
# Configurar URLs de microservicios en .env
EMAIL_SERVICE_URL=http://email-microservice:8080
RENIEC_SERVICE_URL=http://reniec-microservice:8080
```

## 🏃‍♂️ Ejecución

### Desarrollo

```bash
# Servidor de desarrollo
php artisan serve

# Compilar assets
npm run dev

# En modo watch
npm run watch
```

### Producción

```bash
# Optimizar para producción
php artisan config:cache
php artisan route:cache
php artisan view:cache

# Compilar assets para producción
npm run build
```

## 🏗️ Estructura del Proyecto

```
foodops-api/
├── app/
│   ├── Http/
│   │   ├── Controllers/
│   │   │   ├── Api/          # Controladores API
│   │   │   └── Web/          # Controladores Web
│   │   ├── Middleware/       # Middleware personalizado
│   │   └── Requests/         # Validación de formularios
│   ├── Models/               # Modelos Eloquent
│   ├── Services/             # Lógica de negocio
│   │   ├── Implementations/  # Implementaciones
│   │   └── Interfaces/       # Interfaces
│   └── Providers/            # Service Providers
├── resources/
│   ├── views/                # Vistas Blade
│   ├── js/                   # JavaScript
│   └── css/                  # Estilos
├── routes/
│   ├── api.php              # Rutas API
│   └── web.php              # Rutas Web
└── public/                   # Archivos públicos
```

## 👥 Roles del Sistema

### Super Admin
- Gestión de tenants (restaurantes)
- Configuración global del sistema
- Administración de usuarios
- Reportes generales

### Admin Tenant
- Gestión de sucursales
- Configuración del restaurante
- Administración de personal
- Reportes del tenant

### Gerente de Sucursal
- Gestión de mesas
- Control de personal
- Facturación
- Reportes de sucursal

### Mesero
- Crear órdenes
- Gestionar mesas
- Consultar RENIEC (DNI)
- Seguimiento de órdenes

### Cajero
- Apertura/cierre de caja
- Facturación
- Movimientos de caja
- Reportes de ventas

### Cocinero
- Ver órdenes pendientes
- Actualizar estados
- Gestión de preparación

## 🔌 Integración con Microservicios

### Email Microservice
- Envío de formularios de contacto
- Notificaciones automáticas
- Endpoint: `/api/v1/contacto/enviar`

### RENIEC Microservice
- Consulta de datos por DNI
- Auto-completado de nombres
- Endpoint: `/api/v1/reniec/consultar`

## 📱 Interfaces

### Web Dashboard
- Interfaz administrativa completa
- Responsive design
- Múltiples roles y permisos

### API REST
- Endpoints para integración
- Autenticación JWT
- Documentación automática

## 🧪 Testing

```bash
# Ejecutar tests
php artisan test

# Tests específicos
php artisan test --filter=OrderTest
php artisan test --filter=UserTest
```

## 📊 Monitoreo

### Logs
```bash
# Ver logs de Laravel
tail -f storage/logs/laravel.log

# Logs de errores
tail -f storage/logs/error.log
```

### Health Checks
```bash
# Verificar estado de microservicios
curl http://localhost:8000/api/v1/contacto/estado
curl http://localhost:8000/api/v1/reniec/estado
```

## 🐳 Docker

### Dockerfile
```dockerfile
FROM php:8.1-fpm
# ... configuración del Dockerfile
```

### Docker Compose
```yaml
version: '3.8'
services:
  foodops-api:
    build: .
    ports:
      - "8000:80"
    environment:
      - DB_HOST=mysql
      - REDIS_HOST=redis
    depends_on:
      - mysql
      - redis
```

## 🔧 Comandos Útiles

```bash
# Limpiar cache
php artisan cache:clear
php artisan config:clear
php artisan route:clear

# Optimizar
php artisan optimize

# Ver rutas
php artisan route:list

# Crear usuario
php artisan tinker
User::create(['name' => 'Admin', 'email' => 'admin@example.com', 'password' => Hash::make('password')]);

# Backup de base de datos
php artisan db:backup
```

## 🚨 Troubleshooting

### Problemas Comunes

#### 1. **Error de Permisos**
```bash
# Dar permisos a directorios
chmod -R 775 storage bootstrap/cache
chown -R www-data:www-data storage bootstrap/cache
```

#### 2. **Error de Conexión a Base de Datos**
```bash
# Verificar configuración
php artisan config:show database

# Probar conexión
php artisan tinker
DB::connection()->getPdo();
```

#### 3. **Assets No Se Cargan**
```bash
# Recompilar assets
npm run build

# Limpiar cache
php artisan view:clear
```

## 📚 Documentación

- **Laravel Docs**: https://laravel.com/docs
- **API Documentation**: `/api/documentation` (si está habilitado)
- **Swagger**: Integrado en endpoints API

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
- Revisar documentación de Laravel

---

**Nota**: Este sistema está diseñado para ser escalable y multi-tenant. Asegúrate de configurar correctamente los microservicios antes de usar las funcionalidades de email y RENIEC. 