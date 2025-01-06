# app/views/login_view.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
                           QPushButton, QLabel)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from app.config import Config

class LoginView(QWidget):
    loginSuccess = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{Config.APP_NAME} - Login")
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Logo
        logo_label = QLabel()
        pixmap = QPixmap(Config.LOGO_PATH)
        logo_label.setPixmap(pixmap.scaled(200, 200))
        logo_label.setAlignment(Qt.AlignCenter)
        
        # Título
        title = QLabel(Config.APP_NAME)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        
        # Campos de login
        self.usuario_input = QLineEdit()
        self.usuario_input.setPlaceholderText("Usuario")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        # Botón de login
        self.login_btn = QPushButton("Iniciar Sesión")
        
        layout.addWidget(logo_label)
        layout.addWidget(title)
        layout.addWidget(self.usuario_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)
        
        self.setLayout(layout)
        
        # Estilo
        self.setStyleSheet("""
            QWidget {
                background-color: white;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
        """)