# views/main_view.py
from PyQt5.QtWidgets import QMainWindow, QWidget, QTabWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from .personal_view import RegistroPersonalView
from .busqueda_view import BusquedaView

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestión de CVs")
        self.setMinimumSize(1200, 800)
        self.setup_ui()

    def setup_ui(self):
        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Layout principal
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        # Configuración de tabs
        self.tab_widget = QTabWidget()
        
        # Instanciar las vistas
        self.tab_busqueda = BusquedaView()
        self.tab_registro = RegistroPersonalView()  # Usar RegistroPersonalView
        
        # Agregar las pestañas
        self.tab_widget.addTab(self.tab_busqueda, "Búsqueda")
        self.tab_widget.addTab(self.tab_registro, "Registro/Edición")
        
        # Asegurar que las vistas ocupen todo el espacio disponible
        self.tab_busqueda.setMinimumSize(800, 600)
        self.tab_registro.setMinimumSize(800, 600)

        # Agregar el widget de tabs al layout principal
        self.main_layout.addWidget(self.tab_widget)

        # Configurar estilo básico
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background: white;
            }
            QTabBar::tab {
                padding: 8px 20px;
                background: #e0e0e0;
            }
            QTabBar::tab:selected {
                background: #2196F3;
                color: white;
            }
        """)

        # Conectar señales si es necesario
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
        # Configuraciones adicionales de la ventana
        self.setWindowState(Qt.WindowMaximized)

    def on_tab_changed(self, index):
        """Manejar cambios entre pestañas"""
        if index == 1:  # Pestaña de registro
            self.tab_registro.setup_ui()  # Asegurar que la UI esté configurada