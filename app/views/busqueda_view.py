# app/views/busqueda_view.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
    QPushButton, QTableWidget, QTableWidgetItem, QLabel, QComboBox, 
    QCheckBox, QGroupBox)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QColor
from app.config import Config
from app.models.database import Database  # Añadida esta importación

class BusquedaView(QWidget):
    registro_seleccionado = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.db = Database()  # Inicializar conexión a base de datos
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Grupo de filtros
        filtros_group = QGroupBox("Filtros de Búsqueda")
        filtros_layout = QVBoxLayout()

        # Primera fila de filtros
        filtros_row1 = QHBoxLayout()
        
        self.busqueda_input = QLineEdit()
        self.busqueda_input.setPlaceholderText("Buscar por nombre o código...")
        
        self.area_filter = QComboBox()
        self.area_filter.addItems(['Todas las areas'] + Config.AREAS)
        
        filtros_row1.addWidget(QLabel("Buscar:"))
        filtros_row1.addWidget(self.busqueda_input)
        filtros_row1.addWidget(QLabel("Área:"))
        filtros_row1.addWidget(self.area_filter)

        # Segunda fila de filtros
        filtros_row2 = QHBoxLayout()
        
        self.tipo_obra_filter = QComboBox()
        self.tipo_obra_filter.addItems(['Todos los tipos'] + Config.TIPOS_OBRA)
        
        self.monto_filter = QComboBox()
        self.monto_filter.addItems(['Todos los montos', '< 5 MM', '5 - 20 MM', '20 - 50 MM', '50 - 100 MM'])
        
        filtros_row2.addWidget(QLabel("Tipo de Obra:"))
        filtros_row2.addWidget(self.tipo_obra_filter)
        filtros_row2.addWidget(QLabel("Rango de Monto:"))
        filtros_row2.addWidget(self.monto_filter)
        
        # Checkbox para EIMSA
        self.eimsa_check = QCheckBox("Ex-empleados EIMSA")
        
        # Añadir filtros al layout
        filtros_layout.addLayout(filtros_row1)
        filtros_layout.addLayout(filtros_row2)
        filtros_layout.addWidget(self.eimsa_check)
        filtros_group.setLayout(filtros_layout)
        layout.addWidget(filtros_group)

        # Botones de acción
        actions_layout = QHBoxLayout()
        self.btn_buscar = QPushButton("Buscar")
        self.btn_limpiar = QPushButton("Limpiar Filtros")
        self.btn_ver_detalle = QPushButton("Ver Detalle")
        self.btn_generar_cv = QPushButton("Generar CV")
        self.btn_editar = QPushButton("Editar")
        
        # Estilo para los botones
        self.btn_buscar.setStyleSheet("background-color: #3498db; color: white;")
        self.btn_limpiar.setStyleSheet("background-color: #3498db; color: white;")
        self.btn_ver_detalle.setStyleSheet("background-color: #95a5a6; color: white;")
        self.btn_generar_cv.setStyleSheet("background-color: #95a5a6; color: white;")
        self.btn_editar.setStyleSheet("background-color: #95a5a6; color: white;")
        
        actions_layout.addWidget(self.btn_buscar)
        actions_layout.addWidget(self.btn_limpiar)
        actions_layout.addWidget(self.btn_ver_detalle)
        actions_layout.addWidget(self.btn_generar_cv)
        actions_layout.addWidget(self.btn_editar)
        
        layout.addLayout(actions_layout)

        # Actualizar columnas de la tabla para que coincidan con imagen 1
        self.tabla_resultados = QTableWidget()
        self.tabla_resultados.setColumnCount(14)
        self.tabla_resultados.setHorizontalHeaderLabels([
            "F.DE REGISTRO",
            "AREA", 
            "CARGO",
            "APELLIDOS Y NOMBRES",
            "DOCUMENTO DE IDENTIDAD",
            "REF. TRABAJO EN EIMSA",
            "LUGAR DE NACIMIENTO",
            "LUGAR DE RESIDENCIA",
            "TELÉFONO",
            "CORREO",
            "PROFESIÓN",
            "COLEGIATURA",
            "F. NACIMIENTO",
            "EDAD"
        ])
        
        self.tabla_resultados.setAlternatingRowColors(True)
        self.tabla_resultados.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_resultados.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla_resultados.horizontalHeader().setStretchLastSection(True)
        
        layout.addWidget(self.tabla_resultados)
        
        self.setLayout(layout)
        
        # Conectar señales
        self.tabla_resultados.itemSelectionChanged.connect(self.on_selection_change)
        self.busqueda_input.returnPressed.connect(self.btn_buscar.click)

    def cargar_registros(self, resultados=None):
        try:
            self.tabla_resultados.setRowCount(0)
            for row, datos in enumerate(resultados):
                self.tabla_resultados.insertRow(row)
                items = [
                    datos.get('fecha_registro', ''),
                    datos.get('area', ''),
                    datos.get('cargo', ''),
                    datos.get('nombres', ''),
                    'Sí' if datos.get('trabajo_previo_eimsa') else 'No',
                    datos.get('lugar_nacimiento', ''),
                    datos.get('lugar_residencia', ''),
                    datos.get('telefono', ''),
                    datos.get('correo', ''),
                    datos.get('profesion', ''),
                    datos.get('colegiatura', ''),
                    datos.get('fecha_nacimiento', ''),
                    str(datos.get('edad', ''))
                ]

                for col, valor in enumerate(items):
                    item = QTableWidgetItem(str(valor))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.tabla_resultados.setItem(row, col, item)

            self.tabla_resultados.resizeColumnsToContents()
        except Exception as e:
            print(f"Error al cargar registros: {e}")    
    
    def on_selection_change(self):
        """Habilita/deshabilita botones según selección"""
        tiene_seleccion = len(self.tabla_resultados.selectedItems()) > 0
        self.btn_ver_detalle.setEnabled(tiene_seleccion)
        self.btn_generar_cv.setEnabled(tiene_seleccion)
        self.btn_editar.setEnabled(tiene_seleccion)

    def mostrar_resultados(self, resultados):
        """Muestra los resultados en la tabla"""
        self.tabla_resultados.setRowCount(0)
        for row, datos in enumerate(resultados):
            self.tabla_resultados.insertRow(row)
            items = [
                datos.get('codigo', ''),
                datos.get('nombres', ''),
                datos.get('profesion', ''),
                datos.get('area', ''),
                datos.get('cargo', ''),
                datos.get('monto_proyecto', ''),
                '✓' if datos.get('trabajo_previo_eimsa') else '',
                datos.get('fecha_registro', '')
            ]
            
            for col, valor in enumerate(items):
                item = QTableWidgetItem(str(valor))
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                self.tabla_resultados.setItem(row, col, item)
        
        self.tabla_resultados.resizeColumnsToContents()

    def obtener_codigo_seleccionado(self):
        items = self.tabla_resultados.selectedItems()
        if items:
            row = items[0].row()
            return self.tabla_resultados.item(row, 0).text()
        return None
    
    def limpiar_filtros(self):
        self.busqueda_input.clear()
        self.area_filter.setCurrentIndex(0)
        self.tipo_obra_filter.setCurrentIndex(0)
        self.monto_filter.setCurrentIndex(0)
        self.eimsa_check.setChecked(False)