# app/config.py
import os
from pathlib import Path
from datetime import datetime

class Config:
    # Información de la aplicación
    APP_NAME = 'Sistema de Gestión de CVs'
    VERSION = '1.0.0'
    DEBUG = True
    
    # Rutas base
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    APP_DIR = os.path.join(BASE_DIR, 'app')
    
    # Directorios de recursos
    RESOURCES_DIR = os.path.join(APP_DIR, 'resources')
    TEMPLATES_DIR = os.path.join(RESOURCES_DIR, 'templates')
    IMAGES_DIR = os.path.join(RESOURCES_DIR, 'images')
    STYLES_DIR = os.path.join(RESOURCES_DIR, 'styles')
    
    # Directorios de datos
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    OUTPUT_DIR = os.path.join(DATA_DIR, 'output')
    TEMP_DIR = os.path.join(DATA_DIR, 'temp')
    
    # Rutas de archivos
    DB_PATH = os.path.join(DATA_DIR, 'cv_database.db')
    CV_TEMPLATE_PATH = os.path.join(TEMPLATES_DIR, 'cv_template.docx')
    LOGO_PATH = os.path.join(IMAGES_DIR, 'logo.png')
    
    # Credenciales de demo
    DEMO_USER = 'admin'
    DEMO_PASSWORD = 'admin123'
    
    # Configuraciones de la aplicación
    AREAS = [
        'Administración',
        'Oficina Técnica',
        'Construcción',
        'Calidad',
        'SSOMA'
    ]
    
    TIPOS_OBRA = [
        'Planta de Cemento y Cal',
        'Naves Industriales',
        'Hidroeléctrica',
        'Central Termoeléctrica',
        'Planta Eléctrica',
        'Puentes',
        'Planta Petróleo',
        'Obras Civiles',
        'Planta de Gas',
        'Construcción Estructuras',
        'Montaje de Estructura Pesada',
        'Chancadora/Fajas (seca)',
        'Molinos/Celda de Flotación',
        'Túneles',
        'Desmontaje',
        'Electricidad & Instrumentación',
        'Tubería Agua/Relaves',
        'Planta Desalinizadora',
        'Truckshop - Almacenes (Auxiliares)'
    ]
    
    @classmethod
    def create_directories(cls):
        """Crea todos los directorios necesarios para la aplicación"""
        directories = [
            cls.DATA_DIR,
            cls.OUTPUT_DIR,
            cls.TEMP_DIR,
            cls.RESOURCES_DIR,
            cls.TEMPLATES_DIR,
            cls.IMAGES_DIR,
            cls.STYLES_DIR
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    @classmethod
    def get_output_path(cls, filename: str) -> str:
        """Genera una ruta única para archivos de salida"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return os.path.join(cls.OUTPUT_DIR, f'{filename}_{timestamp}.docx')
    
    @classmethod
    def clean_temp_files(cls):
        """Limpia archivos temporales antiguos"""
        if os.path.exists(cls.TEMP_DIR):
            for file in os.listdir(cls.TEMP_DIR):
                file_path = os.path.join(cls.TEMP_DIR, file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f'Error al eliminar {file_path}: {e}')