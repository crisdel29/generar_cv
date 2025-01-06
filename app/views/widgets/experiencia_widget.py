# views/widgets/experiencia_widget.py
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                         QLineEdit, QDateEdit, QTextEdit, QPushButton,
                         QComboBox, QGroupBox, QFileDialog, QListWidget,
                         QMessageBox)
from PyQt5.QtCore import pyqtSignal, Qt, QDate, QUrl
from PyQt5.QtGui import QDesktopServices
import os
from app.config import Config

class ExperienciaWidget(QDialog):
    eliminado = pyqtSignal(QDialog)
    actualizado = pyqtSignal(dict)

    def __init__(self, datos=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Experiencia Laboral")
        self.documentos = []
        self.setup_ui()
        if datos:
            self.cargar_datos(datos)

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Contenido principal
        content_group = QGroupBox("Datos de la Experiencia")
        content_layout = QVBoxLayout()

        # Primera fila: Empresa y Cargo
        fila1 = QHBoxLayout()
        self.empresa_input = QLineEdit()
        self.cargo_input = QLineEdit()
        fila1.addWidget(QLabel("Empresa:"))
        fila1.addWidget(self.empresa_input)
        fila1.addWidget(QLabel("Cargo:"))
        fila1.addWidget(self.cargo_input)

        # Segunda fila: Fechas
        fila2 = QHBoxLayout()
        self.fecha_inicio = QDateEdit()
        self.fecha_fin = QDateEdit()
        self.fecha_inicio.setCalendarPopup(True)
        self.fecha_fin.setCalendarPopup(True)
        fila2.addWidget(QLabel("Fecha Inicio:"))
        fila2.addWidget(self.fecha_inicio)
        fila2.addWidget(QLabel("Fecha Fin:"))
        fila2.addWidget(self.fecha_fin)

        # Tercera fila: Obra y Tipo
        fila3 = QHBoxLayout()
        self.obra_input = QLineEdit()
        self.tipo_obra_combo = QComboBox()
        self.tipo_obra_combo.addItems(Config.TIPOS_OBRA)
        fila3.addWidget(QLabel("Obra:"))
        fila3.addWidget(self.obra_input)
        fila3.addWidget(QLabel("Tipo:"))
        fila3.addWidget(self.tipo_obra_combo)

        # Cuarta fila: Propietario y Monto
        fila4 = QHBoxLayout()
        self.propietario_input = QLineEdit()
        self.monto_input = QLineEdit()
        self.moneda_combo = QComboBox()
        self.moneda_combo.addItems(['S/', 'USD'])
        fila4.addWidget(QLabel("Propietario:"))
        fila4.addWidget(self.propietario_input)
        fila4.addWidget(QLabel("Monto:"))
        fila4.addWidget(self.moneda_combo)
        fila4.addWidget(self.monto_input)

        # Detalle de obra
        self.detalle_obra = QTextEdit()
        self.detalle_obra.setMaximumHeight(100)

        # Funciones
        funciones_group = QGroupBox("Funciones")
        funciones_layout = QVBoxLayout()
        
        self.funciones_list = QListWidget()
        self.funcion_input = QLineEdit()
        self.funcion_input.setPlaceholderText("Ingrese una función...")
        
        btn_agregar_funcion = QPushButton("Agregar Función")
        btn_eliminar_funcion = QPushButton("Eliminar Función")
        
        funciones_layout.addWidget(self.funcion_input)
        funciones_layout.addWidget(btn_agregar_funcion)
        funciones_layout.addWidget(self.funciones_list)
        funciones_layout.addWidget(btn_eliminar_funcion)
        
        funciones_group.setLayout(funciones_layout)

        # Documentos
        docs_group = QGroupBox("Documentos")
        docs_layout = QVBoxLayout()
        
        self.docs_list = QListWidget()
        
        docs_buttons = QHBoxLayout()
        self.btn_agregar_doc = QPushButton("Agregar Documento")
        self.btn_eliminar_doc = QPushButton("Eliminar Documento")
        self.btn_ver_doc = QPushButton("Ver Documento")
        
        docs_buttons.addWidget(self.btn_agregar_doc)
        docs_buttons.addWidget(self.btn_eliminar_doc)
        docs_buttons.addWidget(self.btn_ver_doc)
        
        docs_layout.addWidget(QLabel("Documentos adjuntos (certificados, títulos, etc.):"))
        docs_layout.addWidget(self.docs_list)
        docs_layout.addLayout(docs_buttons)
        
        docs_group.setLayout(docs_layout)

        # Agregar todo al layout principal
        content_layout.addLayout(fila1)
        content_layout.addLayout(fila2)
        content_layout.addLayout(fila3)
        content_layout.addLayout(fila4)
        content_layout.addWidget(QLabel("Detalle de la Obra:"))
        content_layout.addWidget(self.detalle_obra)
        content_layout.addWidget(funciones_group)
        content_layout.addWidget(docs_group)

        content_group.setLayout(content_layout)
        layout.addWidget(content_group)

        # Botones de acción
        buttons = QHBoxLayout()
        self.btn_aceptar = QPushButton("Aceptar")
        self.btn_cancelar = QPushButton("Cancelar")
        buttons.addWidget(self.btn_aceptar)
        buttons.addWidget(self.btn_cancelar)
        layout.addLayout(buttons)

        # Conectar señales
        self.btn_agregar_doc.clicked.connect(self.agregar_documento)
        self.btn_eliminar_doc.clicked.connect(self.eliminar_documento)
        self.btn_ver_doc.clicked.connect(self.ver_documento)
        btn_agregar_funcion.clicked.connect(self.agregar_funcion)
        btn_eliminar_funcion.clicked.connect(self.eliminar_funcion)
        self.btn_aceptar.clicked.connect(self.accept)
        self.btn_cancelar.clicked.connect(self.reject)

        # Actualizar estado de botones
        self.docs_list.itemSelectionChanged.connect(self.actualizar_botones_documento)

    # Métodos para documentos
    def agregar_documento(self):
        try:
            archivos, _ = QFileDialog.getOpenFileNames(
                self,
                "Seleccionar Documentos",
                "",
                "Documentos (*.pdf *.jpg *.jpeg *.png)"
            )
            
            for archivo in archivos:
                nombre = os.path.basename(archivo)
                items = self.docs_list.findItems(nombre, Qt.MatchExactly)
                if not items:
                    self.docs_list.addItem(nombre)
                    self.documentos.append({
                        'nombre': nombre,
                        'ruta': archivo,
                        'tipo': 'documento_experiencia'
                    })
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al agregar documento: {str(e)}")

    def eliminar_documento(self):
        item_actual = self.docs_list.currentItem()
        if item_actual:
            row = self.docs_list.row(item_actual)
            self.docs_list.takeItem(row)
            self.documentos.pop(row)

    def ver_documento(self):
        item_actual = self.docs_list.currentItem()
        if item_actual:
            nombre = item_actual.text()
            for doc in self.documentos:
                if doc['nombre'] == nombre:
                    QDesktopServices.openUrl(QUrl.fromLocalFile(doc['ruta']))
                    break

    def actualizar_botones_documento(self):
        tiene_seleccion = self.docs_list.currentItem() is not None
        self.btn_eliminar_doc.setEnabled(tiene_seleccion)
        self.btn_ver_doc.setEnabled(tiene_seleccion)

    # Métodos para funciones
    def agregar_funcion(self):
        texto = self.funcion_input.text().strip()
        if texto:
            self.funciones_list.addItem(texto)
            self.funcion_input.clear()

    def eliminar_funcion(self):
        item = self.funciones_list.currentItem()
        if item:
            self.funciones_list.takeItem(self.funciones_list.row(item))

    def obtener_datos(self):
        return {
            'empresa': self.empresa_input.text(),
            'cargo': self.cargo_input.text(),
            'fecha_inicio': self.fecha_inicio.date().toString('dd/MM/yyyy'),
            'fecha_fin': self.fecha_fin.date().toString('dd/MM/yyyy'),
            'obra': self.obra_input.text(),
            'tipo_obra': self.tipo_obra_combo.currentText(),
            'propietario': self.propietario_input.text(),
            'monto_proyecto': f"{self.moneda_combo.currentText()} {self.monto_input.text()}",
            'detalle_obra': self.detalle_obra.toPlainText(),
            'funciones': [self.funciones_list.item(i).text() 
                         for i in range(self.funciones_list.count())],
            'documentos': self.documentos
        }

    def cargar_datos(self, datos):
        self.empresa_input.setText(datos.get('empresa', ''))
        self.cargo_input.setText(datos.get('cargo', ''))
        
        if 'fecha_inicio' in datos:
            self.fecha_inicio.setDate(QDate.fromString(datos['fecha_inicio'], 'dd/MM/yyyy'))
        if 'fecha_fin' in datos:
            self.fecha_fin.setDate(QDate.fromString(datos['fecha_fin'], 'dd/MM/yyyy'))
            
        self.obra_input.setText(datos.get('obra', ''))
        
        tipo_obra = datos.get('tipo_obra', '')
        index = self.tipo_obra_combo.findText(tipo_obra)
        if index >= 0:
            self.tipo_obra_combo.setCurrentIndex(index)
            
        self.propietario_input.setText(datos.get('propietario', ''))
        
        monto = datos.get('monto_proyecto', '')
        if monto:
            if monto.startswith('S/'):
                self.moneda_combo.setCurrentText('S/')
                self.monto_input.setText(monto[2:].strip())
            elif monto.startswith('USD'):
                self.moneda_combo.setCurrentText('USD')
                self.monto_input.setText(monto[3:].strip())
                
        self.detalle_obra.setPlainText(datos.get('detalle_obra', ''))
        
        self.funciones_list.clear()
        funciones = datos.get('funciones', [])
        if isinstance(funciones, str):
            funciones = funciones.split(';')
        for funcion in funciones:
            if funcion.strip():
                self.funciones_list.addItem(funcion.strip())
                
        self.docs_list.clear()
        self.documentos = []
        if 'documentos' in datos and datos['documentos']:
            for doc in datos['documentos']:
                if isinstance(doc, dict) and 'nombre' in doc and 'ruta' in doc:
                    self.docs_list.addItem(doc['nombre'])
                    self.documentos.append(doc)