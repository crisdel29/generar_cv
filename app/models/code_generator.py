# utils/code_generator.py
from datetime import datetime
import re
from typing import Optional

class CodeGenerator:
    def __init__(self):
        self._counter = 0
        self._used_codes = set()
    
    def generate_code(self, tipo: str = 'O') -> str:
        """
        Genera un código único con el formato O/A-000001-EI-PE
        Args:
            tipo: 'O' para Obra, 'A' para Administración
        Returns:
            Código único generado
        """
        if tipo not in ['O', 'A']:
            raise ValueError("Tipo debe ser 'O' para Obra o 'A' para Administración")
        
        self._counter += 1
        code = f"{tipo}-{self._counter:06d}-EI-PE"
        
        while code in self._used_codes:
            self._counter += 1
            code = f"{tipo}-{self._counter:06d}-EI-PE"
        
        self._used_codes.add(code)
        return code
    
    def validate_code(self, code: str) -> bool:
        """
        Valida el formato del código
        """
        pattern = r'^[OA]-\d{6}-EI-PE$'
        return bool(re.match(pattern, code))

class ExperienceCalculator:
    @staticmethod
    def calculate_years(fecha_inicio: str, fecha_fin: Optional[str] = None) -> float:
        """
        Calcula los años de experiencia entre dos fechas
        """
        inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fin = datetime.strptime(fecha_fin, '%Y-%m-%d') if fecha_fin else datetime.now()
        
        diff = fin - inicio
        return round(diff.days / 365.25, 2)

    @staticmethod
    def calculate_total_experience(experiencias: list) -> float:
        """
        Calcula la experiencia total sumando todas las experiencias
        """
        total = 0.0
        for exp in experiencias:
            total += ExperienceCalculator.calculate_years(
                exp['fecha_inicio'],
                exp.get('fecha_fin')
            )
        return round(total, 2)

class MontoValidator:
    @staticmethod
    def format_monto(monto: float) -> str:
        """
        Formatea un monto en millones
        """
        if monto < 1_000_000:
            return f"{monto:,.2f}"
        
        millones = monto / 1_000_000
        return f"{millones:,.2f}MM"

    @staticmethod
    def get_range(monto: float) -> str:
        """
        Obtiene el rango del monto del proyecto
        """
        if monto < 5_000_000:
            return "< 5 MM"
        elif monto < 20_000_000:
            return "5 - 20 MM"
        elif monto < 50_000_000:
            return "20 - 50 MM"
        else:
            return "> 50 MM"