FROM php:8.2-apache

# Instala dependencias básicas
RUN apt-get update && apt-get install -y \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    libzip-dev \
    zip \
    git \
    unzip \
    curl \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install gd pdo pdo_mysql zip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instala Node.js y npm
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get update \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instala Composer
COPY --from=composer:2.6 /usr/bin/composer /usr/bin/composer

# Habilita mod_rewrite para Laravel
RUN a2enmod rewrite

# Configuración básica de Apache
COPY <<EOF /etc/apache2/sites-available/000-default.conf
<VirtualHost *:80>
    DocumentRoot /var/www/html/public

    <Directory /var/www/html>
        AllowOverride All
        Require all granted
    </Directory>

    <Directory /var/www/html/public>
        AllowOverride All
        Require all granted
        Options Indexes FollowSymLinks
        DirectoryIndex index.php
    </Directory>

    ErrorLog \${APACHE_LOG_DIR}/error.log
    CustomLog \${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
EOF

WORKDIR /var/www/html

# Copia e instala dependencias PHP
COPY composer.json composer.lock* ./
RUN composer install --no-scripts --no-autoloader --no-dev --no-interaction

# Copia e instala dependencias JS
COPY package*.json ./
RUN npm install

# Copia el código fuente
COPY . .

# Copia configuración de entorno
COPY .env.docker .env

# Finaliza instalación de Composer
RUN composer dump-autoload --no-dev --optimize

# Compila assets si es posible
RUN npm run build || echo "Assets compilation skipped"

# Configura permisos
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html \
    && chmod -R 775 storage bootstrap/cache

# Comandos Laravel básicos
RUN php artisan storage:link --force || true

# Cambiar Apache a puerto 8080 (Cloud Run requiere esto)
RUN sed -i 's/Listen 80/Listen 8080/' /etc/apache2/ports.conf \
 && sed -i 's/<VirtualHost \*:80>/<VirtualHost *:8080>/' /etc/apache2/sites-available/000-default.conf


EXPOSE 8080

CMD ["apache2-foreground"]