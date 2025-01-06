# app/utils/code_generator.py
import random
import string
from datetime import datetime
from typing import Optional
from app.models.database import Database

def generate_code(area: str = 'O', company: str = 'EI', 
                 country: str = 'PE') -> str:
    """
    Genera un código único para un nuevo registro
    Formato: O-000001-EI-PE
    """
    db = Database()
    cursor = db.conn.cursor()
    
    # Obtener el último código
    cursor.execute('''
        SELECT codigo FROM datos_personales 
        WHERE codigo LIKE ? 
        ORDER BY codigo DESC LIMIT 1
    ''', (f'{area}-%',))
    
    result = cursor.fetchone()
    
    if result:
        # Extraer el número del último código y aumentar en 1
        last_number = int(result[0].split('-')[1])
        new_number = last_number + 1
    else:
        new_number = 1
    
    # Generar el nuevo código
    return f"{area}-{new_number:06d}-{company}-{country}"

def generate_temp_code() -> str:
    """
    Genera un código temporal para archivos o registros temporales
    """
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"TEMP-{timestamp}-{random_chars}"