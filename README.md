# 🚀 FoodOps - Sistema de Gestión de Restaurantes

## 📋 Descripción

FoodOps es una aplicación completa de gestión de restaurantes que incluye microservicios para envío de emails y consulta de datos RENIEC. El sistema está construido con Laravel, Spring Boot y FastAPI, desplegado en Google Cloud Platform con Kubernetes.

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    Google Cloud Platform                    │
├─────────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────────┐  │
│  │                 Kubernetes Cluster                    │  │
│  │                  (foodops-cluster)                    │  │
│  ├───────────────────────────────────────────────────────┤  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐   │  │
│  │  │ foodops-api │  │email-service│  │reniec-service│   │  │
│  │  │   (Laravel) │  │  (Spring)   │  │  (FastAPI)   │   │  │
│  │  └─────────────┘  └─────────────┘  └──────────────┘   │  │
│  │         │                │                │           │  │
│  │         └────────────────┼────────────────┘           │  │
│  │                          │                            │  │
│  │  ┌──────────────────────────────────────────────────┐ │  │
│  │  │                   Ingress                        │ │  │
│  │  │                (Load Balancer)                   │ │  │
│  │  └──────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Estructura del Proyecto

```
foodops-microservicios/
├── src/
│   ├── foodops-api/                 # Aplicación Laravel
│   │   ├── app/
│   │   ├── resources/
│   │   ├── routes/
│   │   └── Dockerfile
│   ├── email-microservice/          # Microservicio Java Spring Boot
│   │   ├── src/
│   │   ├── pom.xml
│   │   └── Dockerfile
│   └── reniec-microservice/         # Microservicio Python FastAPI
│       ├── app/
│       ├── main.py
│       └── Dockerfile
├── release/ (Principal)
│   └── kubernetes-manifests.yaml    # Configuración Kubernetes
├── kubernetes-manifests/ (Extra-Opcional)
│   ├── foodops-api-service.yaml
│   ├── foodops-api-configmap.yaml
│   └── foodops-api-ingress.yaml
├── DEPLOYMENT_GUIDE.md
└── README.md
```

## 🛠️ Prerrequisitos

### Software Requerido

1. **Docker Desktop**
   - Descargar desde: https://www.docker.com/products/docker-desktop
   - Versión mínima: 20.10+

2. **Google Cloud SDK**
   - Descargar desde: https://cloud.google.com/sdk/docs/install
   - Incluye: `gcloud`, `kubectl`, `docker`

3. **Git**
   - Descargar desde: https://git-scm.com/

### Cuentas Requeridas

1. **Google Cloud Platform**
   - Cuenta activa con facturación habilitada
   - Proyecto creado con ID: `appnube2025-459114`

2. **Google Container Registry**
   - Habilitado en el proyecto GCP

## 🔧 Configuración Inicial

### 1. Instalar Google Cloud SDK

#### Windows
```bash
# Descargar e instalar desde:
# https://cloud.google.com/sdk/docs/install#windows

# Verificar instalación
gcloud --version
kubectl version --client
```

#### macOS
```bash
# Instalar con Homebrew
brew install google-cloud-sdk

# Verificar instalación
gcloud --version
kubectl version --client
```

#### Linux
```bash
# Instalar con curl
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Verificar instalación
gcloud --version
kubectl version --client
```

### 2. Configurar Google Cloud

```bash
# Inicializar gcloud
gcloud init

# Seleccionar proyecto
gcloud config set project appnube2025-459114

# Configurar zona por defecto
gcloud config set compute/zone us-central1-a

# Verificar configuración
gcloud config list
```

### 3. Autenticar con Google Cloud

```bash
# Autenticar con Google Cloud
gcloud auth login

# Configurar Docker para usar GCR
gcloud auth configure-docker

# Verificar autenticación
gcloud auth list
```

## 🐳 Construcción de Imágenes Docker

### 1. Construir Imagen de Email Microservice

```bash
# Navegar al directorio del microservicio
cd src/email-microservice

# Construir imagen
docker build -t gcr.io/appnube2025-459114/email-microservice:latest .

# Verificar imagen creada
docker images
```

### 2. Construir Imagen de RENIEC Microservice

```bash
# Navegar al directorio del microservicio
cd ../reniec-microservice

# Construir imagen
docker build -t gcr.io/appnube2025-459114/reniec-microservice:latest .

# Verificar imagen creada
docker images 
```

### 3. Construir Imagen de FoodOps API

```bash
# Navegar al directorio de la API
cd ../foodops-api

# Construir imagen
docker build -t gcr.io/appnube2025-459114/foodops-api:latest .

# Verificar imagen creada
docker images 
```

## 📤 Subir Imágenes a Google Container Registry

### 1. Subir Email Microservice

```bash
# Subir imagen a GCR
docker push gcr.io/appnube2025-459114/email-microservice:latest

# Verificar subida
gcloud container images list-tags gcr.io/appnube2025-459114/email-microservice --limit=5
```

### 2. Subir RENIEC Microservice

```bash
# Subir imagen a GCR
docker push gcr.io/appnube2025-459114/reniec-microservice:latest

# Verificar subida
gcloud container images list-tags gcr.io/appnube2025-459114/reniec-microservice --limit=5
```

### 3. Subir FoodOps API

```bash
# Subir imagen a GCR
docker push gcr.io/appnube2025-459114/foodops-api:latest

# Verificar subida
gcloud container images list-tags gcr.io/appnube2025-459114/foodops-api --limit=5
```

## ☁️ Crear Cluster de Kubernetes en GCP

### 1. Crear Cluster

```bash
# Crear cluster con configuración específica
gcloud container clusters create foodops-cluster \
    --zone=us-central1-a \
    --num-nodes=3 \
    --min-nodes=3 \
    --max-nodes=10 \
    --enable-autoscaling \
    --machine-type=e2-medium \
    --disk-size=50 \
    --disk-type=pd-standard \
    --enable-network-policy \
    --enable-ip-alias \
    --project=appnube2025-459114

# Verificar cluster creado
gcloud container clusters list
```

### 2. Configurar kubectl

```bash
# Obtener credenciales del cluster
gcloud container clusters get-credentials foodops-cluster \
    --zone=us-central1-a \
    --project=appnube2025-459114

# Verificar conexión
kubectl cluster-info
kubectl get nodes
```

### 3. Verificar Configuración

```bash
# Ver nodos del cluster
kubectl get nodes -o wide

# Ver información del cluster
kubectl cluster-info dump
```

## 🚀 Desplegar Aplicación en Kubernetes

### 1. Aplicar Configuración de Microservicios

```bash
# Navegar al directorio raíz del proyecto
cd ../../../

# Aplicar configuración de microservicios
kubectl apply -f release/kubernetes-manifests.yaml

# Verificar recursos creados
kubectl get all
```

### 2. Verificar Estado de los Pods

```bash
# Ver pods creados
kubectl get pods
```
Ejemplo de respuesta:

```console
NAME                                   READY   STATUS    RESTARTS      AGE
email-microservice-555966f586-s5p7k    1/1     Running   0             98m
foodops-api-9b9989dc9-p5795            1/1     Running   0             39m
reniec-microservice-5ccdddc8fd-fsxrw   1/1     Running   0             125m
```
```bash
# Ver servicios
kubectl get services
```

```bash
# Ver configmaps
kubectl get configmaps
```

```bash
# Ver secrets
kubectl get secrets
```

### 3. Verificar Logs de los Servicios

```bash
# Ver logs de email-microservice
kubectl logs deployment/email-microservice --tail=20

# Ver logs de reniec-microservice
kubectl logs deployment/reniec-microservice --tail=20

# Ver logs de foodops-api
kubectl logs deployment/foodops-api --tail=20
```

### 4. Verificar Conectividad Interna

```bash
# Probar conectividad entre servicios
kubectl exec -it deployment/foodops-api -- curl email-microservice:8080/email-service/api/v1/contact/health

kubectl exec -it deployment/foodops-api -- curl reniec-microservice:8080/api/v1/reniec/health
```

## 🌐 Configurar Acceso Externo

### 1. Verificar Ingress

```bash
# Ver ingress creado
kubectl get ingress

# Ver detalles del ingress
kubectl describe ingress foodops-api-ingress
```

```console
Name:             foodops-api-ingress
Labels:           <none>
Namespace:        default
Address:          34.49.155.249
Ingress Class:    <none>
Default backend:  <default>
Rules:
Host        Path  Backends
  ----        ----  --------
*
          /   foodops-api:80 (10.4.2.7:8080)
Annotations:  ingress.kubernetes.io/backends:
{"k8s1-e0c89a6c-default-foodops-api-80-fdbac9fc":"HEALTHY","k8s1-e0c89a6c-kube-system-default-http-backend-80-26e8f05f":"HEALTHY"}
ingress.kubernetes.io/forwarding-rule: k8s2-fr-92fqb41c-default-foodops-api-ingress-1c2z1m9n
ingress.kubernetes.io/target-proxy: k8s2-tp-92fqb41c-default-foodops-api-ingress-1c2z1m9n
ingress.kubernetes.io/url-map: k8s2-um-92fqb41c-default-foodops-api-ingress-1c2z1m9n
kubernetes.io/ingress.class: gce
Events:
Type    Reason  Age                    From                     Message
  ----    ------  ----                   ----                     -------
Normal  Sync    4m41s (x142 over 21h)  loadbalancer-controller  Scheduled for sync
```

### 2. Obtener IP Externa

```bash
# Esperar a que se asigne IP externa
kubectl get ingress foodops-api-ingress -w

# Una vez asignada la IP, verificar
kubectl get ingress foodops-api-ingress
```
Respuesta esperada:
```console
NAME                  CLASS    HOSTS   ADDRESS         PORTS   AGE
foodops-api-ingress   <none>   *       34.49.155.249   80      21h
```

## 🔧 Comandos de Mantenimiento

### 1. Ver Estado de los Servicios

```bash
# Ver todos los recursos
kubectl get all

# Ver pods con más detalles
kubectl get pods -o wide

# Ver servicios
kubectl get services

# Ver ingress
kubectl get ingress
```

### 2. Ver Logs

```bash
# Ver logs en tiempo real
kubectl logs -f deployment/email-microservice
kubectl logs -f deployment/reniec-microservice
kubectl logs -f deployment/foodops-api

# Ver logs de un pod específico
kubectl logs <pod-name>
```

### 3. Reiniciar Servicios

```bash
# Reiniciar deployment específico
kubectl rollout restart deployment/email-microservice
kubectl rollout restart deployment/reniec-microservice
kubectl rollout restart deployment/foodops-api

# Verificar estado del rollout
kubectl rollout status deployment/email-microservice
```

### 4. Escalar Servicios

```bash
# Escalar número de réplicas
kubectl scale deployment/email-microservice --replicas=3
kubectl scale deployment/reniec-microservice --replicas=2
kubectl scale deployment/foodops-api --replicas=2
```

## 🔄 Actualizar Aplicación

### 1. Reconstruir y Subir Nueva Imagen

```bash
# Para email-microservice
cd src/email-microservice
docker build -t gcr.io/appnube2025-459114/email-microservice:latest .
docker push gcr.io/appnube2025-459114/email-microservice:latest

# Para reniec-microservice
cd ../reniec-microservice
docker build -t gcr.io/appnube2025-459114/reniec-microservice:latest .
docker push gcr.io/appnube2025-459114/reniec-microservice:latest

# Para foodops-api
cd ../foodops-api
docker build -t gcr.io/appnube2025-459114/foodops-api:latest .
docker push gcr.io/appnube2025-459114/foodops-api:latest
```

### 2. Aplicar Actualización

```bash
# Reiniciar deployments para usar nueva imagen
kubectl rollout restart deployment/email-microservice
kubectl rollout restart deployment/reniec-microservice
kubectl rollout restart deployment/foodops-api

# Verificar estado
kubectl rollout status deployment/email-microservice
kubectl rollout status deployment/reniec-microservice
kubectl rollout status deployment/foodops-api
```

## 🧹 Limpieza

### 1. Eliminar Aplicación

```bash
# Eliminar recursos de la aplicación
kubectl delete -f release/kubernetes-manifests.yaml

# Verificar eliminación
kubectl get all
```

### 2. Eliminar Cluster

```bash
# Eliminar cluster (¡CUIDADO! Esto elimina todo)
gcloud container clusters delete foodops-cluster \
    --zone=us-central1-a \
    --project=appnube2025-459114

# Verificar eliminación
gcloud container clusters list
```

### 3. Eliminar Imágenes de GCR

```bash
# Eliminar imágenes de GCR
gcloud container images delete gcr.io/appnube2025-459114/email-microservice:latest --force-delete-tags
gcloud container images delete gcr.io/appnube2025-459114/reniec-microservice:latest --force-delete-tags
gcloud container images delete gcr.io/appnube2025-459114/foodops-api:latest --force-delete-tags
```

## 🔧 Troubleshooting

### Problemas Comunes

#### 1. **Error de Autenticación con GCR**
```bash
# Reautenticar
gcloud auth login
gcloud auth configure-docker
```

#### 2. **Pods en estado Pending**
```bash
# Verificar recursos
kubectl describe pod <pod-name>
kubectl get events --sort-by='.lastTimestamp'
```

#### 3. **Error de Conectividad entre Servicios**
```bash
# Verificar DNS interno
kubectl exec -it <pod-name> -- nslookup <service-name>

# Verificar conectividad
kubectl exec -it <pod-name> -- curl <service-name>:<port>
```

#### 4. **Ingress sin IP Externa**
```bash
# Verificar eventos del ingress
kubectl describe ingress foodops-api-ingress

# Verificar servicios de backend
kubectl get endpoints
```

### Comandos de Diagnóstico

```bash
# Ver todos los eventos
kubectl get events --sort-by='.lastTimestamp'

# Ver configuración de pods
kubectl describe pod <pod-name>

# Ver configuración de servicios
kubectl describe service <service-name>

# Ver configuración de ingress
kubectl describe ingress <ingress-name>

# Ver logs de todos los pods
kubectl logs -l app=<app-label>
```

## 📊 Monitoreo

### 1. Ver Métricas de Recursos

```bash
# Instalar métricas server (si no está instalado)
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Ver uso de CPU y memoria
kubectl top pods
kubectl top nodes
```

### 2. Ver Health Checks

```bash
# Verificar health checks
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.containerStatuses[0].ready}{"\n"}{end}'
```

## 🔐 Seguridad

### 1. Verificar Secrets

```bash
# Ver secrets creados
kubectl get secrets

# Ver detalles de un secret
kubectl describe secret <secret-name>
```

### 2. Verificar Network Policies

```bash
# Ver network policies
kubectl get networkpolicies

# Ver detalles de network policy
kubectl describe networkpolicy <policy-name>
```

## 📝 Notas Importantes

1. **Costos**: El cluster con 3 nodos e2-medium tiene costos asociados
2. **Escalado**: El cluster está configurado con autoscaling (3-10 nodos)
3. **Persistencia**: No hay volúmenes persistentes configurados
4. **Backup**: Implementar estrategia de backup para datos importantes
5. **Monitoreo**: Considerar implementar Stackdriver para monitoreo avanzado

## 🆘 Soporte

Para problemas específicos:

1. **Revisar logs**: `kubectl logs deployment/<service-name>`
2. **Verificar estado**: `kubectl get pods`
3. **Revisar eventos**: `kubectl get events`
4. **Verificar conectividad**: Usar port-forward para debugging

```bash
# Port forward para debugging
kubectl port-forward service/email-microservice 8080:8080
kubectl port-forward service/reniec-microservice 8081:8080
kubectl port-forward service/foodops-api 8082:80
``` 