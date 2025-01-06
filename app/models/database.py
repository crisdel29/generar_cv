# app/models/database.py
import sqlite3
from pathlib import Path
from app.config import Config
import os
import logging
from datetime import datetime

class MontoRango:
    MENOR_5MM = 1
    ENTRE_5_20MM = 2
    ENTRE_20_50MM = 3
    ENTRE_50_100MM = 4

    @staticmethod
    def obtener_rango(monto):
        """Determina el rango de un monto en millones"""
        try:
            monto = float(monto)
            if monto < 5_000_000:
                return MontoRango.MENOR_5MM
            elif monto < 20_000_000:
                return MontoRango.ENTRE_5_20MM
            elif monto < 50_000_000:
                return MontoRango.ENTRE_20_50MM
            else:
                return MontoRango.ENTRE_50_100MM
        except:
            return MontoRango.MENOR_5MM

    @staticmethod
    def obtener_texto_rango(rango):
        rangos = {
            MontoRango.MENOR_5MM: "< 5 MM",
            MontoRango.ENTRE_5_20MM: "5 - 20 MM",
            MontoRango.ENTRE_20_50MM: "20 - 50 MM",
            MontoRango.ENTRE_50_100MM: "50 - 100 MM"
        }
        return rangos.get(rango, "No especificado")

logger = logging.getLogger(__name__)

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            try:
                cls._instance = super().__new__(cls)
                db_path = Path(Config.DB_PATH)
                db_path.parent.mkdir(parents=True, exist_ok=True)
                cls._instance.conn = sqlite3.connect(str(db_path))
                cls._instance.conn.row_factory = sqlite3.Row
                logger.info(f"Conexión a base de datos establecida: {db_path}")
                cls._instance.crear_tablas()
            except Exception as e:
                logger.error(f"Error al crear instancia de base de datos: {str(e)}")
                raise
        return cls._instance

    def crear_tablas(self):
        """Crea todas las tablas necesarias en la base de datos"""
        try:
            with self.conn:
                cursor = self.conn.cursor()
                # Tabla de datos personales
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS datos_personales (
                    codigo TEXT PRIMARY KEY,
                    tipo_documento TEXT,
                    numero_documento TEXT,
                    nombres TEXT NOT NULL,
                    apellidos TEXT,
                    profesion TEXT NOT NULL,
                    fecha_nacimiento TEXT,
                    lugar_nacimiento TEXT,
                    registro_cip TEXT,
                    area TEXT NOT NULL,
                    cargo TEXT NOT NULL,
                    residencia TEXT,
                    telefono TEXT,
                    correo TEXT,
                    trabajo_previo_eimsa BOOLEAN DEFAULT 0,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                ''')

                # Tabla de experiencia laboral
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS experiencia_laboral (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo_personal TEXT NOT NULL,
                    empresa TEXT NOT NULL,
                    obra TEXT NOT NULL,
                    detalle_obra TEXT,
                    tipo_obra TEXT NOT NULL,
                    monto_proyecto TEXT,
                    cargo TEXT NOT NULL,
                    fecha_inicio TEXT NOT NULL,
                    fecha_fin TEXT,
                    propietario TEXT,
                    funciones TEXT,
                    FOREIGN KEY (codigo_personal) REFERENCES datos_personales(codigo)
                )
                ''')

                # Tabla de documentos
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS documentos_experiencia (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    experiencia_id INTEGER NOT NULL,
                    tipo_documento TEXT NOT NULL,
                    nombre_archivo TEXT NOT NULL,
                    contenido BLOB NOT NULL,
                    descripcion TEXT,
                    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (experiencia_id) REFERENCES experiencia_laboral(id)
                )
                ''')

                logger.info("Todas las tablas creadas/verificadas exitosamente")

        except Exception as e:
            logger.error(f"Error al crear tablas: {str(e)}")
            raise

    
    def execute(self, query, parameters=()):
        """Ejecuta una consulta SQL y retorna el cursor"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, parameters)
            return cursor
        except Exception as e:
            logger.error(f"Error ejecutando query: {str(e)}")
            raise

    def commit(self):
        """Realiza commit de la transacción actual"""
        self.conn.commit()

    def rollback(self):
        """Realiza rollback de la transacción actual"""
        self.conn.rollback()

    def close(self):
        """Cierra la conexión a la base de datos"""
        self.conn.close()
    
    def inicializar_tipos_obra(self):
        try:
            tipos_obra = [
                ('IND_CEM', 'Planta de Cemento y Cal', 'Industria de cemento y cal'),
                ('NAV_IND', 'Naves Industriales', 'Construcción de naves industriales'),
                ('HIDRO', 'Hidroeléctrica', 'Centrales hidroeléctricas'),
                ('PUENTE', 'Puentes', 'Construcción de puentes'),
                ('PET', 'Plantas de Petróleo', 'Infraestructura petrolera'),
                ('TUB', 'Tuberías', 'Sistemas de tuberías'),
                ('GAS', 'Planta de Gas', 'Plantas procesadoras de gas'),
                ('MIN', 'Minería', 'Proyectos mineros'),
                ('TUNEL', 'Túneles', 'Construcción de túneles'),
                ('DESM', 'Desmontaje', 'Trabajos de desmontaje'),
                ('CIV', 'Obras Civiles', 'Construcciones civiles'),
                ('ELEC', 'Electricidad e Instrumentación', 'Sistemas eléctricos'),
                ('DESAL', 'Planta Desalinizadora', 'Plantas de desalinización'),
                ('TRUCK', 'Truck Shop', 'Talleres y almacenes')
            ]
            
            with self.conn:
                for tipo in tipos_obra:
                    self.conn.execute('''
                        INSERT OR IGNORE INTO tipos_obra (id, nombre, descripcion)
                        VALUES (?, ?, ?)
                    ''', tipo)
            logger.debug("Tipos de obra inicializados correctamente")
        except Exception as e:
            logger.error(f"Error al inicializar tipos de obra: {str(e)}")
            raise
    
    def guardar_registro(self, datos):
        try:
            with self.conn:
                cursor = self.conn.cursor()
                logger.debug(f"Iniciando guardado de registro para código: {datos.get('codigo', 'Nuevo')}")
                
                # Si hay monto_proyecto, convertir a decimal
                if 'monto_proyecto' in datos:
                    monto_str = datos['monto_proyecto']
                    # Limpiar el string de moneda
                    monto_num = ''.join(filter(str.isdigit, monto_str))
                    if monto_num:
                        datos['monto_decimal'] = float(monto_num)
                
                # Extraer las experiencias
                experiencias = datos.pop('experiencias', [])
                
                if datos['codigo']:  # Actualización
                    cursor.execute('''
                        UPDATE datos_personales SET 
                            nombres=?, profesion=?, fecha_nacimiento=?,
                            lugar_nacimiento=?, registro_cip=?, area=?,
                            cargo=?, residencia=?, telefono=?, correo=?
                        WHERE codigo=?
                    ''', (
                        datos['nombres'], datos['profesion'], datos['fecha_nacimiento'],
                        datos['lugar_nacimiento'], datos['registro_cip'], datos['area'],
                        datos['cargo'], datos['residencia'], datos['telefono'],
                        datos['correo'], datos['codigo']
                    ))
                    logger.debug(f"Actualizado registro existente: {datos['codigo']}")
                else:  # Nuevo registro
                    datos['codigo'] = self.generar_codigo(datos['area'])
                    cursor.execute('''
                        INSERT INTO datos_personales (
                            codigo, nombres, profesion, fecha_nacimiento,
                            lugar_nacimiento, registro_cip, area, cargo,
                            residencia, telefono, correo, fecha_registro
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                    ''', (
                        datos['codigo'], datos['nombres'], datos['profesion'],
                        datos['fecha_nacimiento'], datos['lugar_nacimiento'],
                        datos['registro_cip'], datos['area'], datos['cargo'],
                        datos['residencia'], datos['telefono'], datos['correo']
                    ))
                    logger.debug(f"Creado nuevo registro: {datos['codigo']}")

                # Manejar las experiencias
                experiencias_actuales = set()
                logger.debug("Iniciando procesamiento de experiencias")
                
                for exp in experiencias:
                    if 'id' in exp:  # Experiencia existente
                        experiencias_actuales.add(exp['id'])
                        cursor.execute('''
                            UPDATE experiencia_laboral SET
                                empresa=?, obra=?, tipo_obra=?,
                                detalle_obra=?, monto_proyecto=?, cargo=?,
                                fecha_inicio=?, fecha_fin=?, propietario=?, funciones=?
                            WHERE id=? AND codigo_personal=?
                        ''', (
                            exp['empresa'], exp['obra'], exp['tipo_obra'],
                            exp['detalle_obra'], exp['monto_proyecto'], exp['cargo'],
                            exp['fecha_inicio'], exp['fecha_fin'], exp['propietario'],
                            ';'.join(exp['funciones']) if isinstance(exp['funciones'], list) else exp['funciones'],
                            exp['id'], datos['codigo']
                        ))
                        exp_id = exp['id']
                        logger.debug(f"Actualizada experiencia ID: {exp_id}")
                    else:  # Nueva experiencia
                        cursor.execute('''
                            INSERT INTO experiencia_laboral (
                                codigo_personal, empresa, obra, tipo_obra,
                                detalle_obra, monto_proyecto, cargo,
                                fecha_inicio, fecha_fin, propietario, funciones
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            datos['codigo'], exp['empresa'], exp['obra'],
                            exp['tipo_obra'], exp['detalle_obra'], exp['monto_proyecto'],
                            exp['cargo'], exp['fecha_inicio'], exp['fecha_fin'],
                            exp['propietario'], ';'.join(exp['funciones']) if isinstance(exp['funciones'], list) else exp['funciones']
                        ))
                        exp_id = cursor.lastrowid
                        experiencias_actuales.add(exp_id)
                        logger.debug(f"Creada nueva experiencia ID: {exp_id}")
                    
                    # Manejar documentos/imágenes
                    if 'documentos' in exp and exp['documentos']:
                        logger.debug(f"Procesando documentos para experiencia ID: {exp_id}")
                        for doc in exp['documentos']:
                            with open(doc['ruta'], 'rb') as img_file:
                                contenido_imagen = img_file.read()
                            
                            cursor.execute('''
                                INSERT INTO imagenes_cv (
                                    codigo_personal, experiencia_id, nombre_archivo,
                                    contenido_imagen, tipo_imagen
                                ) VALUES (?, ?, ?, ?, ?)
                            ''', (
                                datos['codigo'],
                                exp_id,
                                doc['nombre'],
                                contenido_imagen,
                                'experiencia'
                            ))
                            logger.debug(f"Guardada imagen: {doc['nombre']}")

                # Eliminar experiencias que ya no existen
                if experiencias_actuales:
                    cursor.execute('''
                        DELETE FROM experiencia_laboral 
                        WHERE codigo_personal = ? AND id NOT IN ({})
                    '''.format(','.join('?' * len(experiencias_actuales))), 
                        [datos['codigo']] + list(experiencias_actuales))
                    logger.debug("Eliminadas experiencias obsoletas")

                logger.info(f"Registro guardado exitosamente: {datos['codigo']}")
                return datos['codigo']
                    
        except Exception as e:
            logger.error(f"Error al guardar registro: {str(e)}")
            raise Exception(f"Error al guardar en la base de datos: {str(e)}")
    
    def obtener_registro(self, codigo):
        try:
            cursor = self.conn.cursor()
            logger.debug(f"Buscando registro con código: {codigo}")
            
            # Obtener datos personales
            cursor.execute('SELECT * FROM datos_personales WHERE codigo = ?', (codigo,))
            datos_personales = cursor.fetchone()
            
            if datos_personales:
                datos = dict(datos_personales)
                logger.debug(f"Datos personales encontrados para código: {codigo}")
                
                # Obtener experiencias
                cursor.execute('''
                    SELECT * FROM experiencia_laboral
                    WHERE codigo_personal = ?
                    ORDER BY fecha_inicio DESC
                ''', (codigo,))
                
                experiencias = []
                for exp in cursor.fetchall():
                    exp_dict = dict(exp)
                    logger.debug(f"Procesando experiencia ID: {exp_dict['id']}")
                    
                    # Obtener imágenes para esta experiencia
                    cursor.execute('''
                        SELECT id, nombre_archivo, contenido_imagen, tipo_imagen 
                        FROM imagenes_cv 
                        WHERE codigo_personal = ? AND experiencia_id = ?
                    ''', (codigo, exp_dict['id']))
                    
                    documentos = []
                    for img in cursor.fetchall():
                        # Guardar temporalmente la imagen
                        temp_path = os.path.join(Config.TEMP_DIR, img['nombre_archivo'])
                        with open(temp_path, 'wb') as f:
                            f.write(img['contenido_imagen'])
                        
                        documentos.append({
                            'nombre': img['nombre_archivo'],
                            'ruta': temp_path,
                            'tipo': img['tipo_imagen']
                        })
                        logger.debug(f"Imagen procesada: {img['nombre_archivo']}")
                    exp_dict['documentos'] = documentos
                    experiencias.append(exp_dict)
                
                datos['experiencias'] = experiencias
                logger.info(f"Registro obtenido exitosamente: {codigo}")
                return datos
            
            logger.warning(f"No se encontró registro para código: {codigo}")
            return None
            
        except Exception as e:
            logger.error(f"Error al obtener registro {codigo}: {str(e)}")
            raise Exception(f"Error al obtener registro: {str(e)}")

    def generar_codigo(self, area):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT codigo FROM datos_personales 
                WHERE codigo LIKE 'O-%' 
                ORDER BY codigo DESC LIMIT 1
            ''')
            result = cursor.fetchone()
            
            if result:
                ultimo_num = int(result[0].split('-')[1])
                nuevo_num = ultimo_num + 1
            else:
                nuevo_num = 1
            
            nuevo_codigo = f"O-{nuevo_num:06d}-EI-PE"
            logger.debug(f"Generado nuevo código: {nuevo_codigo}")
            return nuevo_codigo
        except Exception as e:
            logger.error(f"Error al generar código: {str(e)}")
            raise

    def obtener_todos_registros(self):
        """Obtiene todos los registros de la base de datos"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT dp.*, COUNT(el.id) as total_experiencias 
                FROM datos_personales dp
                LEFT JOIN experiencia_laboral el ON dp.codigo = el.codigo_personal
                GROUP BY dp.codigo
                ORDER BY dp.fecha_registro DESC
            ''')
            logger.debug("Obteniendo todos los registros")
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error al obtener todos los registros: {str(e)}")
            raise

    def buscar_registros(self, filtros):
        """
        Busca registros según los filtros proporcionados
        filtros: diccionario con los criterios de búsqueda
        """
        try:
            logger.debug(f"Iniciando búsqueda con filtros: {filtros}")
            query = """
                SELECT DISTINCT dp.* 
                FROM datos_personales dp
                LEFT JOIN experiencia_laboral el ON dp.codigo = el.codigo_personal
                WHERE 1=1
            """
            params = []

            if filtros.get('nombres'):
                query += " AND dp.nombres LIKE ?"
                params.append(f"%{filtros['nombres']}%")

            if filtros.get('area') and filtros['area'] != 'Todas las áreas':
                query += " AND dp.area = ?"
                params.append(filtros['area'])

            if filtros.get('cargo'):
                query += " AND dp.cargo LIKE ?"
                params.append(f"%{filtros['cargo']}%")

            if filtros.get('residencia'):
                query += " AND dp.residencia LIKE ?"
                params.append(f"%{filtros['residencia']}%")

            cursor = self.conn.cursor()
            cursor.execute(query, params)
            resultados = cursor.fetchall()
            logger.debug(f"Búsqueda completada. Resultados encontrados: {len(resultados)}")
            return resultados
        except Exception as e:
            logger.error(f"Error en búsqueda de registros: {str(e)}")
            raise

    def eliminar_registro(self, codigo):
        """Elimina un registro y todos sus datos relacionados"""
        try:
            logger.debug(f"Iniciando eliminación de registro: {codigo}")
            with self.conn:
                # Eliminar imágenes primero
                self.conn.execute("""
                    DELETE FROM imagenes_cv 
                    WHERE codigo_personal = ?
                """, (codigo,))

                # Eliminar experiencias
                self.conn.execute("""
                    DELETE FROM experiencia_laboral 
                    WHERE codigo_personal = ?
                """, (codigo,))

                # Eliminar datos personales
                self.conn.execute("""
                    DELETE FROM datos_personales 
                    WHERE codigo = ?
                """, (codigo,))

            logger.info(f"Registro eliminado exitosamente: {codigo}")
            return True
        except Exception as e:
            logger.error(f"Error al eliminar registro {codigo}: {str(e)}")
            raise

    def verificar_duplicado(self, nombres, registro_cip):
        """Verifica si ya existe un registro con el mismo nombre o CIP"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT codigo FROM datos_personales 
                WHERE nombres = ? OR registro_cip = ?
            """, (nombres, registro_cip))
            
            resultado = cursor.fetchone()
            if resultado:
                logger.warning(f"Encontrado registro duplicado: {resultado['codigo']}")
            return resultado is not None
        except Exception as e:
            logger.error(f"Error al verificar duplicados: {str(e)}")
            raise

    def obtener_experiencias_por_tipo(self, tipo_obra):
        """Obtiene todas las experiencias de un tipo de obra específico"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT dp.nombres, el.* 
                FROM experiencia_laboral el
                JOIN datos_personales dp ON el.codigo_personal = dp.codigo
                WHERE el.tipo_obra = ?
                ORDER BY el.fecha_inicio DESC
            """, (tipo_obra,))
            
            logger.debug(f"Obteniendo experiencias para tipo de obra: {tipo_obra}")
            return cursor.fetchall()
        except Exception as e:
            logger.error(f"Error al obtener experiencias por tipo: {str(e)}")
            raise

    def actualizar_imagenes(self, experiencia_id, imagenes):
        """Actualiza las imágenes de una experiencia"""
        try:
            logger.debug(f"Actualizando imágenes para experiencia ID: {experiencia_id}")
            with self.conn:
                # Eliminar imágenes existentes
                self.conn.execute("""
                    DELETE FROM imagenes_cv 
                    WHERE experiencia_id = ?
                """, (experiencia_id,))

                # Insertar nuevas imágenes
                for img in imagenes:
                    with open(img['ruta'], 'rb') as f:
                        contenido = f.read()
                    
                    self.conn.execute("""
                        INSERT INTO imagenes_cv (
                            codigo_personal, experiencia_id, 
                            nombre_archivo, contenido_imagen, tipo_imagen
                        ) VALUES (?, ?, ?, ?, ?)
                    """, (
                        img['codigo_personal'],
                        experiencia_id,
                        img['nombre'],
                        contenido,
                        img['tipo']
                    ))

            logger.info(f"Imágenes actualizadas para experiencia ID: {experiencia_id}")
        except Exception as e:
            logger.error(f"Error al actualizar imágenes: {str(e)}")
            raise

    def exportar_datos(self, ruta_archivo):
        """Exporta todos los datos a un archivo SQL"""
        try:
            logger.debug(f"Iniciando exportación de datos a: {ruta_archivo}")
            with open(ruta_archivo, 'w') as f:
                for line in self.conn.iterdump():
                    f.write(f'{line}\n')
            logger.info(f"Datos exportados exitosamente a: {ruta_archivo}")
            return True
        except Exception as e:
            logger.error(f"Error al exportar datos: {str(e)}")
            raise

    def importar_datos(self, ruta_archivo):
        """Importa datos desde un archivo SQL"""
        try:
            logger.debug(f"Iniciando importación de datos desde: {ruta_archivo}")
            with open(ruta_archivo, 'r') as f:
                sql = f.read()
            self.conn.executescript(sql)
            logger.info(f"Datos importados exitosamente desde: {ruta_archivo}")
            return True
        except Exception as e:
            logger.error(f"Error al importar datos: {str(e)}")
            raise

    def backup_database(self):
        """Realiza una copia de seguridad de la base de datos"""
        try:
            fecha = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = os.path.join(Config.DATA_DIR, f'backup_{fecha}.db')
            
            # Crear una copia de la base de datos
            with open(backup_path, 'wb') as backup_file:
                backup_file.write(self.conn.execute('vacuum into ?', (backup_path,)))
            
            logger.info(f"Backup creado exitosamente: {backup_path}")
            return backup_path
        except Exception as e:
            logger.error(f"Error al crear backup: {str(e)}")
            raise
    
    def obtener_experiencias(self, codigo_personal):
        """Obtiene todas las experiencias de un personal específico"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
            SELECT * FROM experiencia_laboral 
            WHERE codigo_personal = ?
            ORDER BY fecha_inicio DESC
            ''', (codigo_personal,))
            
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            logger.error(f"Error al obtener experiencias: {str(e)}")
            raise