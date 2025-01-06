# app/models/project_filters.py

from enum import Enum
from typing import List, Dict, Optional
from dataclasses import dataclass
from decimal import Decimal

class MontoRango(Enum):
    """Rangos de montos de proyecto definidos"""
    MENOR_5MM = "< 5 MM"
    ENTRE_5_20MM = "5 - 20 MM"
    ENTRE_20_50MM = "20 - 50 MM"
    ENTRE_50_100MM = "50 - 100 MM"
    MAYOR_100MM = "> 100 MM"

@dataclass
class ProyectoMonto:
    """Clase para manejar el monto de un proyecto"""
    valor: Decimal
    moneda: str
    
    def get_rango(self) -> MontoRango:
        """Determina el rango del monto del proyecto"""
        monto_mm = float(self.valor) / 1_000_000
        
        if monto_mm < 5:
            return MontoRango.MENOR_5MM
        elif monto_mm < 20:
            return MontoRango.ENTRE_5_20MM
        elif monto_mm < 50:
            return MontoRango.ENTRE_20_50MM
        elif monto_mm < 100:
            return MontoRango.ENTRE_50_100MM
        else:
            return MontoRango.MAYOR_100MM

class ProjectFilters:
    """Clase para manejar los filtros de búsqueda de proyectos y personal"""
    
    def __init__(self, db_connection):
        self.db = db_connection
    
    def filter_by_residence(self, residence: str) -> List[Dict]:
        """
        Filtra personal por lugar de residencia
        """
        query = """
        SELECT * FROM datos_personales 
        WHERE LOWER(residencia) LIKE LOWER(?)
        """
        return self.db.execute(query, (f"%{residence}%",)).fetchall()
    
    def filter_by_name(self, name: str) -> List[Dict]:
        """
        Filtra personal por nombre o apellido
        """
        query = """
        SELECT * FROM datos_personales 
        WHERE LOWER(nombres) LIKE LOWER(?)
        """
        return self.db.execute(query, (f"%{name}%",)).fetchall()
    
    def filter_by_area(self, area: str) -> List[Dict]:
        """
        Filtra personal por área
        """
        query = """
        SELECT * FROM datos_personales 
        WHERE area = ?
        """
        return self.db.execute(query, (area,)).fetchall()
    
    def filter_by_reference_position(self, position: str) -> List[Dict]:
        """
        Filtra personal por cargo de referencia
        """
        query = """
        SELECT DISTINCT dp.* 
        FROM datos_personales dp
        JOIN experiencia_laboral el ON dp.codigo = el.codigo_personal
        WHERE LOWER(el.cargo) LIKE LOWER(?)
        """
        return self.db.execute(query, (f"%{position}%",)).fetchall()
    
    def filter_by_project_amount(self, rango: MontoRango) -> List[Dict]:
        """
        Filtra proyectos por rango de monto
        """
        ranges = {
            MontoRango.MENOR_5MM: (0, 5_000_000),
            MontoRango.ENTRE_5_20MM: (5_000_000, 20_000_000),
            MontoRango.ENTRE_20_50MM: (20_000_000, 50_000_000),
            MontoRango.ENTRE_50_100MM: (50_000_000, 100_000_000),
            MontoRango.MAYOR_100MM: (100_000_000, float('inf'))
        }
        
        min_val, max_val = ranges[rango]
        
        query = """
        SELECT DISTINCT dp.* 
        FROM datos_personales dp
        JOIN experiencia_laboral el ON dp.codigo = el.codigo_personal
        WHERE CAST(REPLACE(REPLACE(el.monto_proyecto, 'S/', ''), '$', '') AS DECIMAL) 
        BETWEEN ? AND ?
        """
        return self.db.execute(query, (min_val, max_val)).fetchall()
    
    def filter_previous_eimsa(self) -> List[Dict]:
        """
        Filtra personal que trabajó anteriormente en EIMSA
        """
        query = """
        SELECT * FROM datos_personales 
        WHERE trabajo_previo_eimsa = 1
        """
        return self.db.execute(query).fetchall()

# Actualización de la estructura de la base de datos
DB_UPDATES = """
-- Agregar campo para trabajo previo en EIMSA
ALTER TABLE datos_personales ADD COLUMN trabajo_previo_eimsa BOOLEAN DEFAULT 0;

-- Actualizar tabla de experiencia_laboral para manejar montos como decimal
ALTER TABLE experiencia_laboral ADD COLUMN monto_decimal DECIMAL(15,2);
"""