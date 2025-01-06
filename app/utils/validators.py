# app/utils/validators.py
import re
from datetime import datetime
from typing import Tuple

def validate_email(email: str) -> Tuple[bool, str]:
    """
    Valida el formato de un correo electrónico
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not email:
        return True, ""  # El email es opcional
    if re.match(pattern, email):
        return True, ""
    return False, "Formato de correo electrónico inválido"

def validate_phone(phone: str) -> Tuple[bool, str]:
    """
    Valida el formato de un número telefónico
    """
    pattern = r'^\+?[0-9]{9,15}$'
    if not phone:
        return True, ""  # El teléfono es opcional
    if re.match(pattern, phone):
        return True, ""
    return False, "Formato de teléfono inválido"

def validate_date(date_str: str) -> Tuple[bool, str]:
    """
    Valida el formato de una fecha (YYYY-MM-DD)
    """
    try:
        if date_str:
            datetime.strptime(date_str, '%Y-%m-%d')
        return True, ""
    except ValueError:
        return False, "Formato de fecha inválido (YYYY-MM-DD)"

def validate_required(value: str, field_name: str) -> Tuple[bool, str]:
    """
    Valida que un campo requerido no esté vacío
    """
    if not value or not value.strip():
        return False, f"El campo {field_name} es requerido"
    return True, ""