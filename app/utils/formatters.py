# app/utils/formatters.py
from datetime import datetime
import locale

def format_currency(amount: str) -> str:
    """
    Formatea un monto monetario
    """
    try:
        # Limpiar el string de caracteres no numéricos
        clean_amount = ''.join(filter(lambda x: x.isdigit() or x == '.', amount))
        value = float(clean_amount)
        
        # Formatear con separadores de miles
        locale.setlocale(locale.LC_ALL, '')
        return locale.currency(value, grouping=True, symbol='')
    except:
        return amount

def format_date(date_str: str, input_format: str = '%Y-%m-%d',
                output_format: str = '%d/%m/%Y') -> str:
    """
    Formatea una fecha al formato deseado
    """
    try:
        if date_str:
            date_obj = datetime.strptime(date_str, input_format)
            return date_obj.strftime(output_format)
        return ""
    except:
        return date_str

def format_phone(phone: str) -> str:
    """
    Formatea un número telefónico
    """
    if not phone:
        return ""
        
    # Limpiar el número
    clean_number = ''.join(filter(str.isdigit, phone))
    
    if len(clean_number) == 9:  # Número celular Perú
        return f"{clean_number[:3]} {clean_number[3:6]} {clean_number[6:]}"
    return phone