from enum import Enum
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class ExperienciaObra:
    """Clase para almacenar la experiencia en un tipo de obra"""
    años: float
    meses: int
    proyectos: List[str]

class CategoriaObra(Enum):
    INDUSTRIA = "Industria"
    MINERIA = "Minería"
    ENERGIA = "Energía"
    INFRAESTRUCTURA = "Infraestructura"
    SERVICIOS = "Servicios"

class TipoObra:
    def __init__(self):
        self.tipos = {
            # Industria
            "CEMENTO_CAL": {
                "nombre": "Planta de Cemento y Cal",
                "categoria": CategoriaObra.INDUSTRIA
            },
            "NAVES_INDUSTRIALES": {
                "nombre": "Naves Industriales",
                "categoria": CategoriaObra.INDUSTRIA
            },
            
            # Minería
            "CHANCADORAS": {
                "nombre": "Chancadoras/Fajas",
                "categoria": CategoriaObra.MINERIA
            },
            "MOLINOS": {
                "nombre": "Molinos/Celdas de Flotación",
                "categoria": CategoriaObra.MINERIA
            },
            
            # Energía
            "HIDROELECTRICA": {
                "nombre": "Hidroeléctrica",
                "categoria": CategoriaObra.ENERGIA
            },
            "TERMOELECTRICA": {
                "nombre": "Central Termoeléctrica",
                "categoria": CategoriaObra.ENERGIA
            },
            
            # Infraestructura
            "TUBERIAS": {
                "nombre": "Tubería Agua/Relaves",
                "categoria": CategoriaObra.INFRAESTRUCTURA
            },
            "TRUCK_SHOP": {
                "nombre": "Truck Shop/Almacenes",
                "categoria": CategoriaObra.INFRAESTRUCTURA
            },
            
            # Servicios
            "ELECTR_INSTRUM": {
                "nombre": "Electricidad e Instrumentación",
                "categoria": CategoriaObra.SERVICIOS
            },
            "MONTAJE": {
                "nombre": "Montaje de Estructuras Pesadas",
                "categoria": CategoriaObra.SERVICIOS
            }
        }
        
    def get_categorias(self) -> List[CategoriaObra]:
        """Obtiene todas las categorías disponibles"""
        return list(set(tipo["categoria"] for tipo in self.tipos.values()))
        
    def get_tipos_por_categoria(self, categoria: CategoriaObra) -> List[str]:
        """Obtiene los tipos de obra de una categoría específica"""
        return [
            codigo for codigo, datos in self.tipos.items()
            if datos["categoria"] == categoria
        ]
        
    def get_nombre(self, codigo: str) -> Optional[str]:
        """Obtiene el nombre de un tipo de obra por su código"""
        if codigo in self.tipos:
            return self.tipos[codigo]["nombre"]
        return None

class CalculadorExperiencia:
    def __init__(self):
        self.experiencias: Dict[str, ExperienciaObra] = {}
        
    def agregar_experiencia(self, tipo_obra: str, años: float, proyecto: str):
        """
        Agrega experiencia para un tipo de obra específico
        """
        if tipo_obra not in self.experiencias:
            self.experiencias[tipo_obra] = ExperienciaObra(
                años=años,
                meses=int(años * 12),
                proyectos=[proyecto]
            )
        else:
            exp = self.experiencias[tipo_obra]
            exp.años += años
            exp.meses = int(exp.años * 12)
            exp.proyectos.append(proyecto)
            
    def get_experiencia_total(self) -> float:
        """
        Calcula la experiencia total en años
        """
        return sum(exp.años for exp in self.experiencias.values())
        
    def get_experiencia_por_categoria(self, categoria: CategoriaObra) -> Dict[str, ExperienciaObra]:
        """
        Obtiene la experiencia agrupada por categoría
        """
        tipos_obra = TipoObra()
        resultado = {}
        
        for tipo, exp in self.experiencias.items():
            if tipos_obra.tipos[tipo]["categoria"] == categoria:
                resultado[tipo] = exp
                
        return resultado

