# models/experience_manager.py
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass
import sqlite3

@dataclass
class ExperienciaLaboral:
    empresa: str
    obra: str
    tipo_obra: str
    cargo: str
    fecha_inicio: str
    fecha_fin: Optional[str]
    propietario: str
    detalle_obra: str
    monto_proyecto: float
    codigo_personal: str
    id: Optional[int] = None

class ExperienceManager:
    def __init__(self, database_connection):
        self.db = database_connection

    def add_experience(self, experiencia: ExperienciaLaboral) -> int:
        """
        Agrega una nueva experiencia laboral
        Returns:
            ID de la experiencia creada
        """
        query = """
        INSERT INTO experiencia_laboral (
            codigo_personal, empresa, obra, tipo_obra,
            cargo, fecha_inicio, fecha_fin, propietario,
            detalle_obra, monto_proyecto
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor = self.db.execute(query, (
            experiencia.codigo_personal,
            experiencia.empresa,
            experiencia.obra,
            experiencia.tipo_obra,
            experiencia.cargo,
            experiencia.fecha_inicio,
            experiencia.fecha_fin,
            experiencia.propietario,
            experiencia.detalle_obra,
            experiencia.monto_proyecto
        ))
        self.db.commit()
        return cursor.lastrowid

    def update_experience(self, experiencia: ExperienciaLaboral) -> bool:
        """
        Actualiza una experiencia existente
        """
        if not experiencia.id:
            raise ValueError("ID de experiencia no proporcionado")

        query = """
        UPDATE experiencia_laboral SET
            empresa = ?,
            obra = ?,
            tipo_obra = ?,
            cargo = ?,
            fecha_inicio = ?,
            fecha_fin = ?,
            propietario = ?,
            detalle_obra = ?,
            monto_proyecto = ?
        WHERE id = ? AND codigo_personal = ?
        """
        cursor = self.db.execute(query, (
            experiencia.empresa,
            experiencia.obra,
            experiencia.tipo_obra,
            experiencia.cargo,
            experiencia.fecha_inicio,
            experiencia.fecha_fin,
            experiencia.propietario,
            experiencia.detalle_obra,
            experiencia.monto_proyecto,
            experiencia.id,
            experiencia.codigo_personal
        ))
        self.db.commit()
        return cursor.rowcount > 0

    def get_experiences(self, codigo_personal: str) -> List[Dict[str, Any]]:
        """
        Obtiene todas las experiencias de un profesional
        """
        query = """
        SELECT 
            *,
            (julianday(COALESCE(fecha_fin, date('now'))) - 
             julianday(fecha_inicio)) / 365.25 as duracion_años
        FROM 
            experiencia_laboral
        WHERE 
            codigo_personal = ?
        ORDER BY 
            fecha_inicio DESC
        """
        cursor = self.db.execute(query, (codigo_personal,))
        return cursor.fetchall()

    def delete_experience(self, id: int, codigo_personal: str) -> bool:
        """
        Elimina una experiencia laboral
        """
        query = """
        DELETE FROM experiencia_laboral
        WHERE id = ? AND codigo_personal = ?
        """
        cursor = self.db.execute(query, (id, codigo_personal))
        self.db.commit()
        return cursor.rowcount > 0

    def get_experience_by_type(self, tipo_obra: str) -> List[Dict[str, Any]]:
        """
        Obtiene todas las experiencias de un tipo específico
        """
        query = """
        SELECT 
            e.*,
            p.nombres,
            p.profesion,
            (julianday(COALESCE(e.fecha_fin, date('now'))) - 
             julianday(e.fecha_inicio)) / 365.25 as duracion_años
        FROM 
            experiencia_laboral e
        JOIN 
            datos_personales p ON e.codigo_personal = p.codigo
        WHERE 
            e.tipo_obra = ?
        ORDER BY 
            e.fecha_inicio DESC
        """
        cursor = self.db.execute(query, (tipo_obra,))
        return cursor.fetchall()