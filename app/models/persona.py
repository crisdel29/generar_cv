# models/persona.py
from dataclasses import dataclass
from datetime import date
from typing import List, Optional
from enum import Enum

class TipoDocumento(Enum):
    DNI = "DNI"
    RUC = "RUC"
    CE = "CE"  # Carnet de Extranjería
    CPP = "CPP" # Carnet de Permiso Temporal
    PASAPORTE = "PASAPORTE"

@dataclass
class DatosPersonales:
    # Campos requeridos (sin valores por defecto)
    codigo: str
    tipo_documento: TipoDocumento
    numero_documento: str
    nombres: str
    apellidos: str
    profesion: str
    area: str
    cargo_actual: str
    
    # Campos opcionales (con valores por defecto)
    fecha_nacimiento: Optional[date] = None
    lugar_nacimiento: Optional[str] = None
    nacionalidad: str = "Peruana"
    telefono: Optional[str] = None
    correo: Optional[str] = None
    direccion: Optional[str] = None
    ciudad_residencia: Optional[str] = None
    pais_residencia: str = "Perú"
    numero_colegiatura: Optional[str] = None
    años_experiencia: float = 0.0
    fecha_registro: date = date.today()
    trabajado_eimsa: bool = False
    estado_cv: str = "Activo"

@dataclass
class Experiencia:
    # Campos requeridos
    empresa: str
    cargo: str
    fecha_inicio: date
    obra: str
    tipo_obra: str
    propietario: str
    
    # Campos opcionales
    id: Optional[int] = None
    fecha_fin: Optional[date] = None
    detalle_obra: str = ""
    ubicacion: str = ""
    monto_proyecto: float = 0.0
    moneda_proyecto: str = "PEN"
    funciones: List[str] = None
    logros: List[str] = None
    tecnologias_usadas: List[str] = None
    documentos: List[str] = None
    
    def __post_init__(self):
        if self.funciones is None:
            self.funciones = []
        if self.logros is None:
            self.logros = []
        if self.tecnologias_usadas is None:
            self.tecnologias_usadas = []
        if self.documentos is None:
            self.documentos = []
    
    @property
    def duracion_meses(self) -> int:
        fin = self.fecha_fin or date.today()
        return (fin.year - self.fecha_inicio.year) * 12 + (fin.month - self.fecha_inicio.month)

@dataclass
class CV:
    datos_personales: DatosPersonales
    experiencias: List[Experiencia]
    habilidades: List[str] = None
    certificaciones: List[str] = None
    idiomas: List[dict] = None
    educacion: List[dict] = None
    
    def __post_init__(self):
        if self.habilidades is None:
            self.habilidades = []
        if self.certificaciones is None:
            self.certificaciones = []
        if self.idiomas is None:
            self.idiomas = []
        if self.educacion is None:
            self.educacion = []