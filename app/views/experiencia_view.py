from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
                           QLabel, QComboBox, QPushButton, QDateEdit,
                           QTextEdit, QDialog, QListWidget, QFileDialog, 
                           QMessageBox, QGroupBox)
import os
from PyQt5.QtCore import pyqtSignal, Qt, QDate
from app.config import Config

class ExperienciaView(QDialog):
    guardado_success = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Experiencia Laboral")
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Campos de la experiencia
        self.empresa_input = QLineEdit()
        self.obra_input = QLineEdit()
        self.tipo_obra_combo = QComboBox()
        self.tipo_obra_combo.addItems(Config.TIPOS_OBRA)
        self.cargo_input = QLineEdit()
        
        self.fecha_inicio = QDateEdit()
        self.fecha_inicio.setCalendarPopup(True)
        self.fecha_fin = QDateEdit()
        self.fecha_fin.setCalendarPopup(True)
        
        self.detalle_obra = QTextEdit()
        self.propietario = QLineEdit()
        
        # Layout para monto con selector de moneda
        monto_container = QWidget()
        monto_layout = QHBoxLayout(monto_container)
        monto_layout.setContentsMargins(0, 0, 0, 0)
        
        self.moneda_combo = QComboBox()
        self.moneda_combo.addItems(['S/', '$'])
        self.monto_input = QLineEdit()
        self.monto_input.setPlaceholderText("0.00")
        self.monto_input.textChanged.connect(self.validar_monto)
        
        monto_layout.addWidget(self.moneda_combo)
        monto_layout.addWidget(self.monto_input)
        
        # Agregar campos al layout
        campos = [
            ('Empresa:', self.empresa_input),
            ('Obra:', self.obra_input),
            ('Tipo de Obra:', self.tipo_obra_combo),
            ('Cargo:', self.cargo_input),
            ('Fecha de Inicio:', self.fecha_inicio),
            ('Fecha de Fin:', self.fecha_fin),
            ('Detalle de la Obra:', self.detalle_obra),
            ('Monto del Proyecto:', monto_container),
            ('Propietario:', self.propietario)
        ]
        
        for label_text, widget in campos:
            container = QWidget()
            field_layout = QHBoxLayout(container)
            label = QLabel(label_text)
            label.setMinimumWidth(120)
            field_layout.addWidget(label)
            field_layout.addWidget(widget)
            layout.addWidget(container)

        # Sección de funciones
        funciones_group = QGroupBox("Funciones")
        funciones_layout = QVBoxLayout()
        
        nueva_funcion_layout = QHBoxLayout()
        self.nueva_funcion_input = QLineEdit()
        self.btn_agregar_funcion = QPushButton("Agregar Función")
        self.btn_agregar_funcion.clicked.connect(self.agregar_funcion)
        nueva_funcion_layout.addWidget(self.nueva_funcion_input)
        nueva_funcion_layout.addWidget(self.btn_agregar_funcion)
        
        self.funciones_list = QListWidget()
        self.btn_eliminar_funcion = QPushButton("Eliminar Función")
        self.btn_eliminar_funcion.clicked.connect(self.eliminar_funcion)
        
        funciones_layout.addLayout(nueva_funcion_layout)
        funciones_layout.addWidget(self.funciones_list)
        funciones_layout.addWidget(self.btn_eliminar_funcion)
        funciones_group.setLayout(funciones_layout)
        layout.addWidget(funciones_group)

        # Sección de imágenes
        images_group = QGroupBox("Imágenes")
        images_layout = QVBoxLayout()
        
        self.images_list = QListWidget()
        self.btn_agregar_imagen = QPushButton("Agregar Imagen")
        self.btn_agregar_imagen.clicked.connect(self.adjuntar_imagen)
        self.btn_eliminar_imagen = QPushButton("Eliminar Imagen")
        self.btn_eliminar_imagen.clicked.connect(self.eliminar_imagen)
        self.btn_eliminar_imagen.setEnabled(False)
        
        images_layout.addWidget(self.images_list)
        images_layout.addWidget(self.btn_agregar_imagen)
        images_layout.addWidget(self.btn_eliminar_imagen)
        
        images_group.setLayout(images_layout)
        layout.addWidget(images_group)
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar")
        self.btn_cancelar = QPushButton("Cancelar")
        self.btn_guardar.clicked.connect(self.guardar)
        self.btn_cancelar.clicked.connect(self.reject)
        
        buttons_layout.addWidget(self.btn_guardar)
        buttons_layout.addWidget(self.btn_cancelar)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
        
        # Conexiones para imágenes
        self.images_list.itemSelectionChanged.connect(
            lambda: self.btn_eliminar_imagen.setEnabled(self.images_list.currentItem() is not None)
        )
    
    def agregar_funcion(self):
        funcion = self.nueva_funcion_input.text().strip()
        if funcion:
            self.funciones_list.addItem(funcion)
            self.nueva_funcion_input.clear()

    def eliminar_funcion(self):
        current_item = self.funciones_list.currentItem()
        if current_item:
            self.funciones_list.takeItem(self.funciones_list.row(current_item))
    
    def validar_monto(self, texto):
        texto_limpio = ''.join(c for c in texto if c.isdigit() or c == '.')
        if texto_limpio.count('.') > 1:
            texto_limpio = texto_limpio[:texto_limpio.rfind('.')]
        if '.' in texto_limpio:
            partes = texto_limpio.split('.')
            texto_limpio = f"{partes[0]}.{partes[1][:2]}"
        if texto_limpio != texto:
            self.monto_input.setText(texto_limpio)


    def adjuntar_imagen(self):
        try:
            archivos, _ = QFileDialog.getOpenFileNames(
                self,
                "Seleccionar Imágenes",
                "",
                "Imágenes (*.png *.jpg *.jpeg *.bmp)"
            )
            
            if archivos:
                for archivo in archivos:
                    nombre = os.path.basename(archivo)
                    # Verificar si ya existe la imagen
                    existe = False
                    for i in range(self.images_list.count()):
                        if self.images_list.item(i).text() == nombre:
                            existe = True
                            break
                    
                    if not existe:
                        self.images_list.addItem(nombre)
                        if not hasattr(self, 'imagenes'):
                            self.imagenes = []
                        self.imagenes.append({
                            'nombre': nombre,
                            'ruta': archivo,
                            'tipo': 'experiencia'
                        })
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al adjuntar imagen: {str(e)}")
    
    def eliminar_imagen(self):
        current_row = self.images_list.currentRow()
        if current_row >= 0:
            self.images_list.takeItem(current_row)
            if hasattr(self, 'imagenes'):
                self.imagenes.pop(current_row)
    
    def guardar(self):
        datos = self.obtener_datos()
        self.guardado_success.emit(datos)
        self.accept()
    
    def obtener_datos(self):
        funciones = []
        for i in range(self.funciones_list.count()):
            funciones.append(self.funciones_list.item(i).text())
        
        documentos = []
        for i in range(self.images_list.count()):
            nombre = self.images_list.item(i).text()
            # Buscar la ruta en las imágenes guardadas
            for img in getattr(self, 'imagenes', []):
                if img['nombre'] == nombre:
                    documentos.append({
                        'nombre': img['nombre'],
                        'ruta': img['ruta'],
                        'tipo': img.get('tipo', 'experiencia')
                    })
                    break
        
        return {
            'empresa': self.empresa_input.text().strip(),
            'obra': self.obra_input.text().strip(),
            'tipo_obra': self.tipo_obra_combo.currentText(),
            'cargo': self.cargo_input.text().strip(),
            'fecha_inicio': self.fecha_inicio.date().toString('dd/MM/yyyy'),
            'fecha_fin': self.fecha_fin.date().toString('dd/MM/yyyy'),
            'detalle_obra': self.detalle_obra.toPlainText().strip(),
            'monto_proyecto': f"{self.moneda_combo.currentText()} {self.monto_input.text()}",
            'propietario': self.propietario.text().strip(),
            'funciones': funciones,
            'documentos': documentos  # Usar la lista de documentos procesada
        }

    def cargar_datos(self, experiencia):
        try:
            self.empresa_input.setText(experiencia['empresa'])
            self.obra_input.setText(experiencia['obra'])
            
            index = self.tipo_obra_combo.findText(experiencia['tipo_obra'])
            if index >= 0:
                self.tipo_obra_combo.setCurrentIndex(index)
                
            self.cargo_input.setText(experiencia['cargo'])
            self.fecha_inicio.setDate(QDate.fromString(experiencia['fecha_inicio'], 'dd-MM-yyyy'))
            
            if experiencia['fecha_fin']:
                self.fecha_fin.setDate(QDate.fromString(experiencia['fecha_fin'], 'dd-MM-yyyy'))
                
            self.detalle_obra.setPlainText(experiencia['detalle_obra'])
            
            # Separar monto y moneda
            monto = experiencia['monto_proyecto']
            if monto.startswith('S/'):
                self.moneda_combo.setCurrentText('S/')
                self.monto_input.setText(monto[2:].strip())
            elif monto.startswith('$'):
                self.moneda_combo.setCurrentText('$')
                self.monto_input.setText(monto[1:].strip())
            else:
                self.monto_input.setText(monto)
                
            self.propietario.setText(experiencia['propietario'])
            
            # Cargar funciones
            self.funciones_list.clear()
            if isinstance(experiencia['funciones'], list):
                for funcion in experiencia['funciones']:
                    self.funciones_list.addItem(funcion)
            elif isinstance(experiencia['funciones'], str):
                for funcion in experiencia['funciones'].split(';'):
                    if funcion.strip():
                        self.funciones_list.addItem(funcion.strip())
            
            # Cargar imágenes
            self.images_list.clear()
            if 'documentos' in experiencia and experiencia['documentos']:
                self.imagenes = experiencia['documentos']  # Guardamos la lista completa de imágenes
                for doc in experiencia['documentos']:
                    self.images_list.addItem(doc['nombre'])
                        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar experiencia: {str(e)}")

    
    