# app/logger.py
import logging
import os
from datetime import datetime
from .config import Config

def setup_logger():
    # Crear directorio de logs si no existe
    log_dir = os.path.join(Config.DATA_DIR, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Configurar logger
    log_file = os.path.join(
        log_dir,
        f'cv_system_{datetime.now().strftime("%Y%m%d")}.log'
    )
    
    logging.basicConfig(
        level=logging.DEBUG if Config.DEBUG else logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger('cv_system')

logger = setup_logger()