# models/experience_filter.py
from typing import List, Dict, Any
from datetime import datetime
from dataclasses import dataclass

@dataclass
class FilterCriteria:
    area: str = None
    cargo: str = None
    tipo_obra: str = None
    rango_monto: str = None
    ex_eimsa: bool = False
    años_experiencia: int = None
    residencia: str = None

class ExperienceFilter:
    def __init__(self, database_connection):
        self.db = database_connection

    def apply_filters(self, criteria: FilterCriteria) -> List[Dict[str, Any]]:
        """
        Aplica los filtros especificados a la búsqueda de experiencias
        """
        query = """
        SELECT DISTINCT 
            p.*,
            e.tipo_obra,
            e.monto_proyecto,
            e.cargo as ultimo_cargo
        FROM 
            datos_personales p
        LEFT JOIN experiencia_laboral e ON 
            p.codigo = e.codigo_personal
        WHERE 1=1
        """
        params = []

        if criteria.area:
            query += " AND p.area = ?"
            params.append(criteria.area)

        if criteria.cargo:
            query += " AND (p.cargo_referencia LIKE ? OR e.cargo LIKE ?)"
            params.extend([f"%{criteria.cargo}%", f"%{criteria.cargo}%"])

        if criteria.tipo_obra:
            query += " AND e.tipo_obra = ?"
            params.append(criteria.tipo_obra)

        if criteria.rango_monto:
            ranges = {
                "< 5 MM": (0, 5_000_000),
                "5 - 20 MM": (5_000_000, 20_000_000),
                "20 - 50 MM": (20_000_000, 50_000_000),
                "> 50 MM": (50_000_000, float('inf'))
            }
            min_val, max_val = ranges[criteria.rango_monto]
            query += " AND e.monto_proyecto >= ? AND e.monto_proyecto < ?"
            params.extend([min_val, max_val])

        if criteria.ex_eimsa:
            query += " AND p.trabajo_previo_eimsa = 1"

        if criteria.residencia:
            query += " AND p.lugar_residencia LIKE ?"
            params.append(f"%{criteria.residencia}%")

        cursor = self.db.execute(query, params)
        results = cursor.fetchall()

        # Filtrar por años de experiencia si se especifica
        if criteria.años_experiencia:
            filtered_results = []
            for result in results:
                total_exp = self._calculate_total_experience(result['codigo'])
                if total_exp >= criteria.años_experiencia:
                    result['años_experiencia'] = total_exp
                    filtered_results.append(result)
            return filtered_results

        return results

    def _calculate_total_experience(self, codigo_personal: str) -> float:
        """
        Calcula la experiencia total para un profesional
        """
        query = """
        SELECT 
            fecha_inicio,
            fecha_fin
        FROM 
            experiencia_laboral
        WHERE 
            codigo_personal = ?
        """
        cursor = self.db.execute(query, (codigo_personal,))
        experiences = cursor.fetchall()
        
        total = 0.0
        for exp in experiences:
            inicio = datetime.strptime(exp['fecha_inicio'], '%Y-%m-%d')
            fin = datetime.strptime(exp['fecha_fin'], '%Y-%m-%d') if exp['fecha_fin'] else datetime.now()
            total += (fin - inicio).days / 365.25
            
        return round(total, 2)

    def get_experience_summary(self, codigo_personal: str) -> Dict[str, Any]:
        """
        Obtiene un resumen de la experiencia por tipo de obra
        """
        query = """
        SELECT 
            tipo_obra,
            COUNT(*) as total_proyectos,
            SUM(
                (julianday(COALESCE(fecha_fin, date('now'))) - 
                 julianday(fecha_inicio)) / 365.25
            ) as años_experiencia,
            MAX(monto_proyecto) as mayor_monto
        FROM 
            experiencia_laboral
        WHERE 
            codigo_personal = ?
        GROUP BY 
            tipo_obra
        """
        cursor = self.db.execute(query, (codigo_personal,))
        return {row['tipo_obra']: dict(row) for row in cursor.fetchall()}