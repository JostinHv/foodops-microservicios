import re
from typing import Optional


def validate_dni_format(dni: str) -> bool:
    """
    Valida el formato del DNI de manera estricta
    Optimizado para evitar peticiones innecesarias a la API
    
    Args:
        dni: Número de DNI a validar
        
    Returns:
        True si el formato es válido, False en caso contrario
    """
    if not dni:
        return False
    
    # Verificar que solo contenga números y tenga exactamente 8 dígitos
    if not re.match(r'^\d{8}$', dni):
        return False
    
    # Validaciones específicas para DNI peruano
    if dni.startswith('0'):  # DNI no puede empezar con 0
        return False
    
    # Verificar que no sea una secuencia de números repetidos
    if len(set(dni)) == 1:  # Todos los dígitos iguales
        return False
    
    return True


def sanitize_dni(dni: str) -> Optional[str]:
    """
    Sanitiza el DNI eliminando espacios y caracteres no deseados
    
    Args:
        dni: Número de DNI a sanitizar
        
    Returns:
        DNI sanitizado o None si no es válido
    """
    if not dni:
        return None
    
    # Eliminar espacios y caracteres no numéricos
    cleaned_dni = re.sub(r'[^\d]', '', dni)
    
    # Verificar que tenga 8 dígitos y pase las validaciones
    if len(cleaned_dni) == 8 and validate_dni_format(cleaned_dni):
        return cleaned_dni
    
    return None


def format_person_name(nombres: str, apellido_paterno: str, apellido_materno: str) -> str:
    """
    Formatea el nombre completo de una persona
    
    Args:
        nombres: Nombres de la persona
        apellido_paterno: Apellido paterno
        apellido_materno: Apellido materno
        
    Returns:
        Nombre completo formateado
    """
    parts = [nombres, apellido_paterno, apellido_materno]
    # Filtrar partes vacías y unir
    return " ".join(part.strip() for part in parts if part and part.strip())


def get_dni_validation_details(dni: str) -> dict:
    """
    Obtiene detalles sobre la validación de un DNI
    Útil para debugging y mensajes de error informativos
    
    Args:
        dni: Número de DNI a analizar
        
    Returns:
        Diccionario con detalles de la validación
    """
    if not dni:
        return {
            "es_valido": False,
            "razon": "DNI vacío",
            "longitud": 0,
            "es_numerico": False,
            "empieza_con_cero": False
        }
    
    return {
        "es_valido": validate_dni_format(dni),
        "longitud": len(dni),
        "es_numerico": dni.isdigit(),
        "empieza_con_cero": dni.startswith('0') if dni else False,
        "tiene_8_digitos": len(dni) == 8,
        "todos_iguales": len(set(dni)) == 1 if dni else False
    } 