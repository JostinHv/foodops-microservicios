#!/bin/bash

# Script de deployment para Google Cloud Kubernetes
# Uso: ./k8s/deploy.sh [PROJECT_ID] [IMAGE_TAG]

set -e

PROJECT_ID=${1:-"tu-project-id"}
IMAGE_TAG=${2:-"latest"}
REGION="us-central1"
CLUSTER_NAME="reniec-cluster"

echo "🚀 Iniciando deployment en Google Cloud..."
echo "📋 Project ID: $PROJECT_ID"
echo "🏷️  Image Tag: $IMAGE_TAG"

# Configurar gcloud
echo "🔧 Configurando gcloud..."
gcloud config set project $PROJECT_ID

# Construir y subir imagen a Google Container Registry
echo "🏗️  Construyendo imagen Docker..."
docker build -t gcr.io/$PROJECT_ID/reniec-microservice:$IMAGE_TAG .

echo "📤 Subiendo imagen a Google Container Registry..."
docker push gcr.io/$PROJECT_ID/reniec-microservice:$IMAGE_TAG

# Actualizar deployment con la nueva imagen
echo "🔄 Actualizando deployment..."
sed -i "s|gcr.io/PROJECT_ID/reniec-microservice:latest|gcr.io/$PROJECT_ID/reniec-microservice:$IMAGE_TAG|g" k8s/deployment.yaml

# Aplicar configuración de Kubernetes
echo "📦 Aplicando configuración de Kubernetes..."

# Crear namespace
kubectl apply -f k8s/namespace.yaml

# Aplicar ConfigMap y Secret
kubectl apply -f k8s/configmap.yaml
echo "⚠️  Recuerda actualizar el Secret con tu token de API:"
echo "   kubectl edit secret reniec-secrets -n reniec-microservice"

# Aplicar deployment y servicios
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Aplicar HPA
kubectl apply -f k8s/hpa.yaml

# Aplicar Network Policy
kubectl apply -f k8s/network-policy.yaml

# Aplicar Ingress (opcional - requiere dominio configurado)
echo "🌐 Para configurar Ingress, edita k8s/ingress.yaml con tu dominio y ejecuta:"
echo "   kubectl apply -f k8s/ingress.yaml"

# Verificar deployment
echo "✅ Verificando deployment..."
kubectl rollout status deployment/reniec-microservice -n reniec-microservice

# Mostrar información del deployment
echo "📊 Información del deployment:"
kubectl get pods -n reniec-microservice
kubectl get services -n reniec-microservice
kubectl get hpa -n reniec-microservice

echo "🎉 Deployment completado!"
echo "📖 Para ver logs: kubectl logs -f deployment/reniec-microservice -n reniec-microservice"
echo "🌐 Para port-forward: kubectl port-forward svc/reniec-service 8080:80 -n reniec-microservice" 