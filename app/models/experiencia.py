# models/experiencia.py
from typing import List, Optional
from dataclasses import dataclass
from.database import Database

@dataclass
class Experiencia:
    codigo_personal: str
    empresa: str
    obra: str
    tipo_obra: str
    cargo: str
    fecha_inicio: str
    fecha_fin: Optional[str]
    detalle_obra: Optional[str] = None
    monto_proyecto: Optional[str] = None
    propietario: Optional[str] = None
    funciones: Optional[str] = None
    documentos: List[dict] = None  # Para certificados, títulos, etc.
    id: Optional[int] = None

    def guardar(self) -> bool:
        db = Database()
        try:
            with db.conn:
                cursor = db.conn.cursor()
                cursor.execute('''
                    INSERT INTO experiencia_laboral (
                        codigo_personal, empresa, obra, detalle_obra,
                        tipo_obra, monto_proyecto, cargo, fecha_inicio,
                        fecha_fin, propietario, funciones
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    self.codigo_personal, self.empresa, self.obra,
                    self.detalle_obra, self.tipo_obra, self.monto_proyecto,
                    self.cargo, self.fecha_inicio, self.fecha_fin,
                    self.propietario, self.funciones
                ))
                
                self.id = cursor.lastrowid
                
                # Guardar documentos
                if self.documentos:
                    for doc in self.documentos:
                        with open(doc['ruta'], 'rb') as f:
                            contenido = f.read()
                            cursor.execute('''
                                INSERT INTO documentos_experiencia (
                                    experiencia_id, tipo_documento, 
                                    nombre_archivo, contenido, descripcion
                                ) VALUES (?, ?, ?, ?, ?)
                            ''', (
                                self.id, doc['tipo'],
                                doc['nombre'], contenido,
                                doc.get('descripcion', '')
                            ))
                
                return True
        except Exception as e:
            print(f"Error al guardar experiencia: {e}")
            return False