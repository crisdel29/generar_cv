# models/personal.py

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from .database import Database

@dataclass
class Personal:
    codigo: str
    tipo_documento: str  # Añadido campo de tipo de documento
    numero_documento: str  # Añadido campo de número de documento
    nombres: str
    apellidos: str
    profesion: str
    area: str
    cargo: str
    fecha_nacimiento: Optional[str] = None
    lugar_nacimiento: Optional[str] = None
    registro_cip: Optional[str] = None
    residencia: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None
    fecha_registro: Optional[str] = None

    @staticmethod
    def generar_codigo(area: str) -> str:
        db = Database()
        cursor = db.conn.cursor()
        
        cursor.execute('''
            SELECT codigo FROM datos_personales 
            WHERE codigo LIKE 'O-%' 
            ORDER BY codigo DESC LIMIT 1
        ''')
        
        ultimo_codigo = cursor.fetchone()
        
        if ultimo_codigo:
            num = int(ultimo_codigo[0].split('-')[1]) + 1
        else:
            num = 1
            
        return f'O-{num:06d}-EI-PE'

    def guardar(self) -> bool:
        db = Database()
        try:
            with db.conn:
                cursor = db.conn.cursor()
                cursor.execute('''
                    INSERT INTO datos_personales (
                        codigo, tipo_documento, numero_documento,
                        nombres, apellidos, profesion, 
                        fecha_nacimiento, lugar_nacimiento, 
                        registro_cip, area, cargo,
                        residencia, telefono, correo
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    self.codigo, self.tipo_documento, self.numero_documento,
                    self.nombres, self.apellidos, self.profesion,
                    self.fecha_nacimiento, self.lugar_nacimiento,
                    self.registro_cip, self.area, self.cargo,
                    self.residencia, self.telefono, self.correo
                ))
                return True
        except Exception as e:
            print(f"Error al guardar personal: {e}")
            return False