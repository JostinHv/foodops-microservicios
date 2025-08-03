#!/usr/bin/env python3
"""
Script simple para probar el microservicio RENIEC sin curl
Incluye pruebas de cache, rate limiting y nuevos endpoints
"""

import requests
import json
import time
from typing import Dict, Any


def test_health_endpoint(base_url: str) -> Dict[str, Any]:
    """
    Prueba el endpoint de health check
    """
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"✅ Health Check (/) - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   📋 Respuesta: {data}")
        return {"success": True, "status_code": response.status_code, "data": response.json()}
    except requests.exceptions.ConnectionError:
        print(f"❌ Health Check (/) - Error: No se puede conectar al servidor")
        print(f"   💡 Asegúrate de que el servidor esté ejecutándose en {base_url}")
        return {"success": False, "error": "Connection failed"}
    except Exception as e:
        print(f"❌ Health Check (/) - Error: {e}")
        return {"success": False, "error": str(e)}


def test_reniec_health_endpoint(base_url: str) -> Dict[str, Any]:
    """
    Prueba el endpoint de health check específico de RENIEC
    """
    try:
        response = requests.get(f"{base_url}/api/v1/reniec/health", timeout=10)
        print(f"✅ RENIEC Health Check - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   📋 Respuesta: {data}")
        return {"success": True, "status_code": response.status_code, "data": response.json()}
    except requests.exceptions.ConnectionError:
        print(f"❌ RENIEC Health Check - Error: No se puede conectar al servidor")
        return {"success": False, "error": "Connection failed"}
    except Exception as e:
        print(f"❌ RENIEC Health Check - Error: {e}")
        return {"success": False, "error": str(e)}


def test_api_usage_endpoint(base_url: str) -> Dict[str, Any]:
    """
    Prueba el endpoint de monitoreo de uso de API
    """
    try:
        response = requests.get(f"{base_url}/api/v1/reniec/api-usage", timeout=10)
        print(f"✅ API Usage Check - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   📋 Uso de API: {data['peticiones_usadas']}/{data['limite_mensual']} peticiones")
            print(f"   📋 Restantes: {data['peticiones_restantes']} peticiones")
            print(f"   📋 Porcentaje usado: {data['porcentaje_usado']}")
            print(f"   📋 Timeout: {data['timeout_segundos']} segundos")
            if 'cache_stats' in data:
                cache_stats = data['cache_stats']
                print(f"   📋 Cache - Hit Rate: {cache_stats.get('hit_rate_percent', 0)}%")
                print(f"   📋 Cache - Entradas: {cache_stats.get('total_entries', 0)}")
        return {"success": True, "status_code": response.status_code, "data": response.json()}
    except requests.exceptions.ConnectionError:
        print(f"❌ API Usage Check - Error: No se puede conectar al servidor")
        return {"success": False, "error": "Connection failed"}
    except Exception as e:
        print(f"❌ API Usage Check - Error: {e}")
        return {"success": False, "error": str(e)}


def test_cache_stats_endpoint(base_url: str) -> Dict[str, Any]:
    """
    Prueba el endpoint de estadísticas del cache
    """
    try:
        response = requests.get(f"{base_url}/api/v1/reniec/cache/stats", timeout=10)
        print(f"✅ Cache Stats - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   📋 Tipo: {data['cache_type']}")
            print(f"   📋 TTL: {data['ttl_minutos']} minutos")
            print(f"   📋 Entradas: {data['total_entries']}")
            print(f"   📋 Hit Rate: {data['hit_rate_percent']}%")
            print(f"   📋 Hits: {data['hits']}, Misses: {data['misses']}")
        return {"success": True, "status_code": response.status_code, "data": response.json()}
    except requests.exceptions.ConnectionError:
        print(f"❌ Cache Stats - Error: No se puede conectar al servidor")
        return {"success": False, "error": "Connection failed"}
    except Exception as e:
        print(f"❌ Cache Stats - Error: {e}")
        return {"success": False, "error": str(e)}


def test_rate_limit_stats_endpoint(base_url: str) -> Dict[str, Any]:
    """
    Prueba el endpoint de estadísticas de rate limiting
    """
    try:
        response = requests.get(f"{base_url}/api/v1/reniec/rate-limit/stats", timeout=10)
        print(f"✅ Rate Limit Stats - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   📋 Rate Limiting: {data['rate_limiting']}")
            print(f"   📋 IPs únicas: {data['unique_ips']}")
            print(f"   📋 Peticiones/minuto: {data['total_minute_requests']}")
            print(f"   📋 Peticiones/hora: {data['total_hour_requests']}")
            print(f"   📋 Límites: {data['limits']}")
        return {"success": True, "status_code": response.status_code, "data": response.json()}
    except requests.exceptions.ConnectionError:
        print(f"❌ Rate Limit Stats - Error: No se puede conectar al servidor")
        return {"success": False, "error": "Connection failed"}
    except Exception as e:
        print(f"❌ Rate Limit Stats - Error: {e}")
        return {"success": False, "error": str(e)}


def test_person_endpoint(base_url: str, dni: str) -> Dict[str, Any]:
    """
    Prueba el endpoint de consulta de persona por DNI
    """
    try:
        response = requests.get(f"{base_url}/api/v1/reniec/persona/{dni}", timeout=10)
        print(f"✅ Consulta DNI {dni} - Status: {response.status_code}")
        
        # Verificar headers de rate limiting
        rate_limit_headers = {
            'X-RateLimit-Limit-Minute': response.headers.get('X-RateLimit-Limit-Minute'),
            'X-RateLimit-Remaining-Minute': response.headers.get('X-RateLimit-Remaining-Minute'),
            'X-RateLimit-Limit-Hour': response.headers.get('X-RateLimit-Limit-Hour'),
            'X-RateLimit-Remaining-Hour': response.headers.get('X-RateLimit-Remaining-Hour')
        }
        
        if response.status_code == 200:
            data = response.json()
            print(f"   📋 Datos obtenidos: {data.get('nombres_completos', 'N/A')}")
            print(f"   📋 DNI: {data.get('dni', 'N/A')}")
            print(f"   📋 Nombres: {data.get('nombres', 'N/A')}")
            print(f"   📋 Rate Limit - Minuto: {rate_limit_headers['X-RateLimit-Remaining-Minute']}/{rate_limit_headers['X-RateLimit-Limit-Minute']}")
            print(f"   📋 Rate Limit - Hora: {rate_limit_headers['X-RateLimit-Remaining-Hour']}/{rate_limit_headers['X-RateLimit-Limit-Hour']}")
        elif response.status_code == 404:
            print(f"   ⚠️  Persona no encontrada para DNI: {dni}")
        elif response.status_code == 400:
            print(f"   ❌ DNI inválido: {dni}")
            error_data = response.json()
            print(f"   📋 Error: {error_data}")
        elif response.status_code == 429:
            print(f"   🚫 Rate limit excedido para DNI: {dni}")
            error_data = response.json()
            print(f"   📋 Error: {error_data}")
        
        return {"success": True, "status_code": response.status_code, "data": response.json()}
    except requests.exceptions.ConnectionError:
        print(f"❌ Consulta DNI {dni} - Error: No se puede conectar al servidor")
        return {"success": False, "error": "Connection failed"}
    except Exception as e:
        print(f"❌ Consulta DNI {dni} - Error: {e}")
        return {"success": False, "error": str(e)}


def test_cache_clear_endpoint(base_url: str) -> Dict[str, Any]:
    """
    Prueba el endpoint de limpiar cache
    """
    try:
        response = requests.delete(f"{base_url}/api/v1/reniec/cache/clear", timeout=10)
        print(f"✅ Cache Clear - Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   📋 Respuesta: {data}")
        return {"success": True, "status_code": response.status_code, "data": response.json()}
    except requests.exceptions.ConnectionError:
        print(f"❌ Cache Clear - Error: No se puede conectar al servidor")
        return {"success": False, "error": "Connection failed"}
    except Exception as e:
        print(f"❌ Cache Clear - Error: {e}")
        return {"success": False, "error": str(e)}


def test_rate_limiting(base_url: str) -> Dict[str, Any]:
    """
    Prueba el rate limiting haciendo múltiples peticiones rápidas
    """
    print(f"🧪 Probando rate limiting...")
    
    # Hacer 5 peticiones rápidas
    for i in range(5):
        try:
            response = requests.get(f"{base_url}/api/v1/reniec/health", timeout=5)
            remaining_minute = response.headers.get('X-RateLimit-Remaining-Minute', 'N/A')
            remaining_hour = response.headers.get('X-RateLimit-Remaining-Hour', 'N/A')
            print(f"   📋 Petición {i+1}: Status {response.status_code}, Remaining: {remaining_minute}/{remaining_hour}")
            time.sleep(0.1)  # Pequeña pausa
        except Exception as e:
            print(f"   ❌ Error en petición {i+1}: {e}")
    
    return {"success": True}


def run_tests():
    """
    Ejecuta todas las pruebas
    """
    base_url = "http://localhost:8080"
    
    print("🚀 Iniciando pruebas del microservicio RENIEC...")
    print("=" * 60)
    
    # Prueba 1: Health check general
    test_health_endpoint(base_url)
    print()
    
    # Prueba 2: Health check RENIEC
    test_reniec_health_endpoint(base_url)
    print()
    
    # Prueba 3: Monitoreo de uso de API
    test_api_usage_endpoint(base_url)
    print()
    
    # Prueba 4: Estadísticas del cache
    test_cache_stats_endpoint(base_url)
    print()
    
    # Prueba 5: Estadísticas de rate limiting
    test_rate_limit_stats_endpoint(base_url)
    print()
    
    # Prueba 6: Rate limiting
    test_rate_limiting(base_url)
    print()
    
    # Prueba 7: Consulta con DNI válido (ejemplo)
    test_person_endpoint(base_url, "46027897")
    print()
    
    # Prueba 8: Consulta con DNI inválido (menos dígitos)
    test_person_endpoint(base_url, "1234567")
    print()
    
    # Prueba 9: Consulta con DNI inválido (con letras)
    test_person_endpoint(base_url, "1234567a")
    print()
    
    # Prueba 10: Consulta con DNI inválido (empieza con 0)
    test_person_endpoint(base_url, "01234567")
    print()
    
    # Prueba 11: Limpiar cache
    test_cache_clear_endpoint(base_url)
    print()
    
    print("=" * 60)
    print("✅ Pruebas completadas!")
    print("\n📖 Para ver la documentación completa, visita:")
    print(f"   {base_url}/docs")
    print(f"   {base_url}/redoc")
    print(f"\n🌐 También puedes probar directamente en tu navegador:")
    print(f"   {base_url}/")
    print(f"   {base_url}/api/v1/reniec/health")
    print(f"   {base_url}/api/v1/reniec/api-usage")
    print(f"   {base_url}/api/v1/reniec/cache/stats")
    print(f"   {base_url}/api/v1/reniec/rate-limit/stats")


if __name__ == "__main__":
    print("⚠️  Asegúrate de que el servidor esté ejecutándose en http://localhost:8080")
    print("   Ejecuta: python main.py")
    print()
    
    try:
        run_tests()
    except KeyboardInterrupt:
        print("\n⏹️  Pruebas interrumpidas por el usuario")
    except Exception as e:
        print(f"\n❌ Error ejecutando las pruebas: {e}")
        print("   Verifica que el servidor esté ejecutándose correctamente") 