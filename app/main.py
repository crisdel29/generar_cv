# app/main.py
import sys
import os
import logging
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt
from app.controllers.login_controller import LoginController
from app.controllers.main_controller import MainController
from app.config import Config
from app.utils.setup_check import verificar_plantilla_cv

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    from views.main_view import MainView
    
    app = QApplication(sys.argv)
    window = MainView()
    window.show()
    sys.exit(app.exec_())

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('app.log')
        ]
    )

class Application:
    def __init__(self):
        setup_logging()
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Iniciando aplicación...")
        
        # Crear las carpetas necesarias
        Config.create_directories()
        
        # Inicializar la aplicación
        self.app = QApplication(sys.argv)
        self.app.setStyle('Fusion')
        
        # Cargar estilos
        style_path = os.path.join(Config.STYLES_DIR, 'style.qss')
        if os.path.exists(style_path):
            with open(style_path, 'r') as f:
                self.app.setStyleSheet(f.read())
        
        # Mantener referencias a los controladores
        self.login_controller = None
        self.main_controller = None
    
    def start(self):
        try:
            # Iniciar con ventana de login
            self.login_controller = LoginController()
            
            # Auto-login en modo debug
            if Config.DEBUG:
                self.login_controller.view.usuario_input.setText(Config.DEMO_USER)
                self.login_controller.view.password_input.setText(Config.DEMO_PASSWORD)
            
            self.login_controller.view.show()
            self.login_controller.view.loginSuccess.connect(self.on_login_success)
            
            return self.app.exec_()
            
        except Exception as e:
            self.logger.error(f"Error en la aplicación: {str(e)}", exc_info=True)
            QMessageBox.critical(None, "Error Fatal", f"Error en la aplicación: {str(e)}")
            return 1
    
    def on_login_success(self):
        try:
            self.logger.debug("Login exitoso, creando ventana principal...")
            self.main_controller = MainController()
            self.main_controller.view.show()
            self.login_controller.view.close()
        except Exception as e:
            self.logger.error(f"Error al crear ventana principal: {str(e)}", exc_info=True)
            QMessageBox.critical(None, "Error Fatal", f"Error al iniciar la aplicación: {str(e)}")

def main():
    if not verificar_plantilla_cv():
        print("La aplicación continuará, pero la generación de CVs no estará disponible.")
    # Configurar logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    application = Application()
    return application.start()

if __name__ == '__main__':
    sys.exit(main())