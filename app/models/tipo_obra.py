# app/models/tipo_obra.py
from dataclasses import dataclass
from typing import List
from .database import Database
from typing import Optional


@dataclass
class TipoObra:
    id: str
    nombre: str
    descripcion: Optional[str] = None
    
    @staticmethod
    def obtener_todos() -> List['TipoObra']:
        db = Database()
        cursor = db.conn.cursor()
        
        cursor.execute('SELECT * FROM tipos_obra ORDER BY nombre')
        resultados = cursor.fetchall()
        
        return [TipoObra(**dict(row)) for row in resultados]
    
    @staticmethod
    def obtener_por_id(id: str) -> Optional['TipoObra']:
        db = Database()
        cursor = db.conn.cursor()
        
        cursor.execute('SELECT * FROM tipos_obra WHERE id = ?', (id,))
        resultado = cursor.fetchone()
        
        if resultado:
            return TipoObra(**dict(resultado))
        return None