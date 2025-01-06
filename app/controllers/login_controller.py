# app/controllers/login_controller.py
from PyQt5.QtWidgets import QMessageBox
from app.views.login_view import LoginView
from app.config import Config
from app.models.database import Database

class LoginController:
    def __init__(self):
        self.view = LoginView()
        self.db = Database()
        self.setup_connections()
    
    def setup_connections(self):
        self.view.login_btn.clicked.connect(self.validar_login)
        # Añadir eventos Enter para una mejor experiencia de usuario
        self.view.usuario_input.returnPressed.connect(self.validar_login)
        self.view.password_input.returnPressed.connect(self.validar_login)
    
    def validar_login(self):
        try:
            usuario = self.view.usuario_input.text().strip()
            password = self.view.password_input.text().strip()
            
            if not usuario or not password:
                QMessageBox.warning(
                    self.view,
                    "Error",
                    "Por favor complete todos los campos"
                )
                return
            
            # En modo debug usar credenciales de prueba
            if Config.DEBUG:
                if usuario == Config.DEMO_USER and password == Config.DEMO_PASSWORD:
                    self.view.loginSuccess.emit()
                else:
                    QMessageBox.warning(
                        self.view,
                        "Error",
                        "Credenciales incorrectas"
                    )
            else:
                # TODO: Implementar validación con base de datos real
                pass
            
        except Exception as e:
            QMessageBox.critical(
                self.view,
                "Error",
                f"Error en el inicio de sesión: {str(e)}"
            )