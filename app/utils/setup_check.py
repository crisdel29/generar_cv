# En utils/setup_check.py
import os
from app.config import Config

def verificar_plantilla_cv():
    if not os.path.exists(Config.CV_TEMPLATE_PATH):
        print(f"ADVERTENCIA: No se encontró la plantilla de CV en {Config.CV_TEMPLATE_PATH}")
        print("Creando directorio de templates...")
        os.makedirs(os.path.dirname(Config.CV_TEMPLATE_PATH), exist_ok=True)
        print(f"Por favor, coloque su plantilla de CV en: {Config.CV_TEMPLATE_PATH}")
        return False
    return True