# views/personal_view.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
                           QLabel, QComboBox, QPushButton, QDateEdit,
                           QScrollArea, QMessageBox, QGroupBox, QGridLayout, QCheckBox)
from PyQt5.QtCore import pyqtSignal, Qt, QDate, QRegExp
from PyQt5.QtGui import QRegExpValidator
from app.config import Config
from .widgets.experiencia_widget import ExperienciaWidget
import re

class RegistroPersonalView(QWidget):
    guardado_success = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        # Inicializar campos primero
        self.experiencias = []
        self.inicializar_campos()
        self.setup_ui()
        self.setup_validations()

    def inicializar_campos(self):
        """Inicializa todos los campos antes de crear la UI"""
        self.campos = {
            'nombres': QLineEdit(),
            'apellidos': QLineEdit(),
            'profesion': QLineEdit(),
            'fecha_nacimiento': QDateEdit(),
            'lugar_nacimiento': QLineEdit(),
            'registro_cip': QLineEdit(),
            'area': QComboBox(),
            'cargo': QLineEdit(),
            'residencia': QLineEdit(),
            'telefono': QLineEdit(),
            'correo': QLineEdit(),
        }

        # Configuraciones especiales
        self.campos['fecha_nacimiento'].setCalendarPopup(True)
        self.campos['area'].addItems(Config.AREAS)

        # Inicializar otros campos que no están en el diccionario
        self.tipo_doc_combo = QComboBox()
        self.num_doc_input = QLineEdit()
        self.codigo_input = QLineEdit()
        self.check_eimsa = QCheckBox("Ex-empleado EIMSA")

    
    def setup_validations(self):
        """Configurar validaciones de campos"""
        # Usar self.campos[] en lugar de acceder directamente
        self.campos['correo'].textChanged.connect(self.validar_correo)
        self.campos['telefono'].textChanged.connect(self.validar_telefono)
        self.campos['fecha_nacimiento'].setMaximumDate(QDate.currentDate())
        self.tipo_doc_combo.currentIndexChanged.connect(self.configurar_validacion_documento)

    def validar_correo(self):
        """Valida el formato del correo electrónico"""
        correo = self.campos['correo'].text()
        if correo:
            patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            es_valido = bool(re.match(patron, correo))
            self.campos['correo'].setStyleSheet(
                "background-color: #E8F5E9;" if es_valido else "background-color: #FFEBEE;"
            )

    def validar_telefono(self):
        """Valida el formato del teléfono"""
        telefono = self.campos['telefono'].text()
        if telefono:
            patron = r'^\+?[0-9]{9,15}$'
            es_valido = bool(re.match(patron, telefono))
            self.campos['telefono'].setStyleSheet(
                "background-color: #E8F5E9;" if es_valido else "background-color: #FFEBEE;"
            )
    
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Crear scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        content_layout = QVBoxLayout(content)

        # 1. Grupo de Identificación
        grupo_id = QGroupBox("Documento de Identidad")
        id_layout = QGridLayout()
        
        self.tipo_doc_combo = QComboBox()
        self.tipo_doc_combo.addItems(['DNI', 'CE', 'PAS', 'CPP'])
        self.num_doc_input = QLineEdit()
        self.codigo_input = QLineEdit()
        self.codigo_input.setReadOnly(True)
        
        id_layout.addWidget(QLabel("Tipo de Documento:"), 0, 0)
        id_layout.addWidget(self.tipo_doc_combo, 0, 1)
        id_layout.addWidget(QLabel("Número:"), 0, 2)
        id_layout.addWidget(self.num_doc_input, 0, 3)
        id_layout.addWidget(QLabel("Código de Registro:"), 1, 0)
        id_layout.addWidget(self.codigo_input, 1, 1, 1, 3)
        
        grupo_id.setLayout(id_layout)
        content_layout.addWidget(grupo_id)

        # 2. Grupo de Datos Personales
        datos_group = QGroupBox("Datos Personales")
        datos_layout = QGridLayout()
        
        # Campos básicos
        self.campos = {
            'nombres': QLineEdit(),
            'apellidos': QLineEdit(),
            'profesion': QLineEdit(),
            'fecha_nacimiento': QDateEdit(),
            'lugar_nacimiento': QLineEdit(),
            'registro_cip': QLineEdit(),
            'area': QComboBox(),
            'cargo': QLineEdit(),
            'residencia': QLineEdit(),
            'telefono': QLineEdit(),
            'correo': QLineEdit(),
        }

        # Configuraciones especiales
        self.campos['fecha_nacimiento'].setCalendarPopup(True)
        self.campos['area'].addItems(Config.AREAS)

        row = 0
        for label, key in [
            ('Nombres:', 'nombres'),
            ('Apellidos:', 'apellidos'),
            ('Profesión:', 'profesion'),
            ('Fecha Nacimiento:', 'fecha_nacimiento'),
            ('Lugar Nacimiento:', 'lugar_nacimiento'),
            ('Registro CIP:', 'registro_cip'),
            ('Área:', 'area'),
            ('Cargo:', 'cargo'),
            ('Residencia:', 'residencia'),
            ('Teléfono:', 'telefono'),
            ('Correo:', 'correo')
        ]:
            label_widget = QLabel(label)
            label_widget.setMinimumWidth(150)
            datos_layout.addWidget(label_widget, row, 0)
            datos_layout.addWidget(self.campos[key], row, 1)
            row += 1

        self.check_eimsa = QCheckBox("Ex-empleado EIMSA")
        datos_layout.addWidget(self.check_eimsa, row, 0, 1, 2)
        
        datos_group.setLayout(datos_layout)
        content_layout.addWidget(datos_group)

        # 3. Grupo de Experiencias Laborales
        exp_group = QGroupBox("Experiencias Laborales")
        exp_layout = QVBoxLayout()
        
        # Contenedor scrollable para experiencias
        exp_scroll = QScrollArea()
        exp_content = QWidget()
        self.experiencias_layout = QVBoxLayout(exp_content)
        exp_scroll.setWidget(exp_content)
        exp_scroll.setWidgetResizable(True)
        
        self.btn_agregar_experiencia = QPushButton("Agregar Experiencia")
        self.btn_agregar_experiencia.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        exp_layout.addWidget(self.btn_agregar_experiencia)
        exp_layout.addWidget(exp_scroll)
        exp_group.setLayout(exp_layout)
        content_layout.addWidget(exp_group)

        # Botones de acción
        buttons_layout = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar")
        self.btn_cancelar = QPushButton("Cancelar")
        
        self.btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }
        """)
        
        self.btn_cancelar.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }
        """)
        
        buttons_layout.addWidget(self.btn_guardar)
        buttons_layout.addWidget(self.btn_cancelar)
        content_layout.addLayout(buttons_layout)

        # Finalizar scroll area principal
        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        # Conectar señales
        self.btn_guardar.clicked.connect(self.validar_datos)
        self.btn_cancelar.clicked.connect(self.cancelar)
        self.btn_agregar_experiencia.clicked.connect(self.agregar_experiencia)
        self.tipo_doc_combo.currentIndexChanged.connect(self.configurar_validacion_documento)

    def configurar_validacion_documento(self):
        """Configura el validador según el tipo de documento"""
        tipo_doc = self.tipo_doc_combo.currentText()
        
        if tipo_doc == "DNI":
            regex = QRegExp("[0-9]{8}")
            validator = QRegExpValidator(regex)
            self.num_doc_input.setMaxLength(8)
            self.num_doc_input.setPlaceholderText("Ingrese 8 dígitos")
        elif tipo_doc in ["CE", "PAS", "CPP"]:
            regex = QRegExp("[A-Za-z0-9]{1,12}")
            validator = QRegExpValidator(regex)
            self.num_doc_input.setMaxLength(12)
            self.num_doc_input.setPlaceholderText("Máximo 12 caracteres")
        
        self.num_doc_input.setValidator(validator)
        self.num_doc_input.clear()

    def validar_documento(self):
        """Valida el formato del documento según tipo"""
        tipo_doc = self.tipo_doc_combo.currentText()
        numero = self.num_doc_input.text()

        if tipo_doc == "DNI":
            numero = ''.join(filter(str.isdigit, numero))[:8]
            self.num_doc_input.setText(numero)
            self.num_doc_input.setStyleSheet(
                "background-color: #FFEBEE;" if len(numero) < 8 
                else "background-color: #E8F5E9;"
            )
        elif tipo_doc in ["CE", "PAS", "CPP"]:
            numero = numero[:12]
            self.num_doc_input.setText(numero)
            self.num_doc_input.setStyleSheet(
                "background-color: #FFEBEE;" if len(numero) == 0
                else "background-color: #E8F5E9;"
            )

    def validar_correo(self):
        """Valida el formato del correo electrónico"""
        correo = self.campos['correo'].text()
        if correo:
            patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            es_valido = bool(re.match(patron, correo))
            self.campos['correo'].setStyleSheet(
                "background-color: #E8F5E9;" if es_valido else "background-color: #FFEBEE;"
            )

    def validar_telefono(self):
        """Valida el formato del teléfono"""
        telefono = self.campos['telefono'].text()
        if telefono:
            patron = r'^\+?[0-9]{9,15}$'
            es_valido = bool(re.match(patron, telefono))
            self.campos['telefono'].setStyleSheet(
                "background-color: #E8F5E9;" if es_valido else "background-color: #FFEBEE;"
            )

    def agregar_experiencia(self):
        """Abre el diálogo para agregar una nueva experiencia laboral"""
        try:
            dialogo = ExperienciaWidget(parent=self)
            if dialogo.exec_():
                datos_experiencia = dialogo.obtener_datos()
                self.experiencias.append(datos_experiencia)
                self.actualizar_lista_experiencias()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error al agregar experiencia: {str(e)}"
            )

    def actualizar_lista_experiencias(self):
        """Actualiza la visualización de la lista de experiencias"""
        try:
            # Limpiar experiencias existentes
            while self.experiencias_layout.count():
                item = self.experiencias_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            
            # Agregar experiencias actualizadas
            for i, exp in enumerate(self.experiencias):
                exp_widget = QWidget()
                exp_layout = QVBoxLayout(exp_widget)
                
                titulo = QLabel(f"{exp['cargo']} en {exp['empresa']}")
                titulo.setStyleSheet("font-weight: bold;")
                periodo = QLabel(f"Periodo: {exp['fecha_inicio']} - {exp['fecha_fin'] or 'Actualidad'}")
                
                exp_layout.addWidget(titulo)
                exp_layout.addWidget(periodo)
                
                botones_layout = QHBoxLayout()
                btn_editar = QPushButton("Editar")
                btn_eliminar = QPushButton("Eliminar")
                
                btn_editar.clicked.connect(lambda checked, idx=i: self.editar_experiencia(idx))
                btn_eliminar.clicked.connect(lambda checked, idx=i: self.eliminar_experiencia(idx))
                
                botones_layout.addWidget(btn_editar)
                botones_layout.addWidget(btn_eliminar)
                exp_layout.addLayout(botones_layout)
                
                # Si hay documentos, mostrar lista
                if 'documentos' in exp and exp['documentos']:
                    docs_label = QLabel("Documentos adjuntos:")
                    docs_label.setStyleSheet("font-weight: bold;")
                    exp_layout.addWidget(docs_label)
                    for doc in exp['documentos']:
                        exp_layout.addWidget(QLabel(f"• {doc['nombre']}"))
                
                self.experiencias_layout.addWidget(exp_widget)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error al actualizar lista de experiencias: {str(e)}"
            )

    def editar_experiencia(self, index):
        """Abre el diálogo para editar una experiencia existente"""
        try:
            dialogo = ExperienciaWidget(parent=self)
            dialogo.cargar_datos(self.experiencias[index])
            if dialogo.exec_():
                self.experiencias[index] = dialogo.obtener_datos()
                self.actualizar_lista_experiencias()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error al editar experiencia: {str(e)}"
            )

    def eliminar_experiencia(self, index):
        """Elimina una experiencia de la lista"""
        try:
            respuesta = QMessageBox.question(
                self,
                "Confirmar eliminación",
                "¿Está seguro de que desea eliminar esta experiencia?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if respuesta == QMessageBox.Yes:
                self.experiencias.pop(index)
                self.actualizar_lista_experiencias()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Error al eliminar experiencia: {str(e)}"
            )

    def obtener_datos(self):
        """Recopila todos los datos del formulario"""
        return {
            'tipo_documento': self.tipo_doc_combo.currentText(),
            'numero_documento': self.num_doc_input.text(),
            'codigo': self.codigo_input.text(),
            'nombres': self.campos['nombres'].text().strip(),
            'apellidos': self.campos['apellidos'].text().strip(),
            'profesion': self.campos['profesion'].text().strip(),
            'fecha_nacimiento': self.campos['fecha_nacimiento'].date().toString('yyyy-MM-dd'),
            'lugar_nacimiento': self.campos['lugar_nacimiento'].text().strip(),
            'registro_cip': self.campos['registro_cip'].text().strip(),
            'area': self.campos['area'].currentText(),
            'cargo': self.campos['cargo'].text().strip(),
            'residencia': self.campos['residencia'].text().strip(),
            'telefono': self.campos['telefono'].text().strip(),
            'correo': self.campos['correo'].text().strip(),
            'trabajo_previo_eimsa': self.check_eimsa.isChecked(),
            'experiencias': self.experiencias
        }

    def limpiar_campos(self):
        """Limpia todos los campos del formulario"""
        self.codigo_input.clear()
        self.num_doc_input.clear()
        self.tipo_doc_combo.setCurrentIndex(0)
        
        for campo in self.campos.values():
            if isinstance(campo, QLineEdit):
                campo.clear()
                campo.setStyleSheet("")  # Limpiar estilos de validación
            elif isinstance(campo, QComboBox):
                campo.setCurrentIndex(0)
            elif isinstance(campo, QDateEdit):
                campo.setDate(campo.minimumDate())
        
        self.check_eimsa.setChecked(False)
        
        # Limpiar experiencias
        self.experiencias = []
        self.actualizar_lista_experiencias()

    def cargar_datos(self, datos):
        """Carga los datos en el formulario"""
        try:
            # Cargar documento de identidad
            self.tipo_doc_combo.setCurrentText(datos.get('tipo_documento', 'DNI'))
            self.num_doc_input.setText(datos.get('numero_documento', ''))
            self.codigo_input.setText(datos.get('codigo', ''))
            
            # Cargar datos personales
            for key, value in datos.items():
                if key in self.campos:
                    campo = self.campos[key]
                    if isinstance(campo, QLineEdit):
                        campo.setText(str(value))
                    elif isinstance(campo, QComboBox) and value:
                        index = campo.findText(str(value))
                        if index >= 0:
                            campo.setCurrentIndex(index)
                    elif isinstance(campo, QDateEdit) and value:
                        campo.setDate(QDate.fromString(value, 'yyyy-MM-dd'))
            
            # Cargar checkbox EIMSA
            self.check_eimsa.setChecked(datos.get('trabajo_previo_eimsa', False))
            
            # Cargar experiencias
            self.experiencias = datos.get('experiencias', [])
            self.actualizar_lista_experiencias()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar datos: {str(e)}")

    def validar_datos(self):
        """Valida los campos del formulario antes de guardar"""
        try:
            # Validar documento
            if not self.num_doc_input.text().strip():
                QMessageBox.warning(self, "Error", "El número de documento es requerido")
                self.num_doc_input.setFocus()
                return False

            # Validar campos requeridos
            campos_requeridos = {
                'nombres': "Nombres y Apellidos",
                'profesion': "Profesión",
                'cargo': "Cargo"
            }

            for key, nombre in campos_requeridos.items():
                if not self.campos[key].text().strip():
                    QMessageBox.warning(self, "Error", f"El campo {nombre} es requerido")
                    self.campos[key].setFocus()
                    return False

            # Validar correo si se ha ingresado
            correo = self.campos['correo'].text().strip()
            if correo and not self._validar_formato_correo(correo):
                QMessageBox.warning(self, "Error", "El formato del correo electrónico no es válido")
                self.campos['correo'].setFocus()
                return False

            # Validar teléfono si se ha ingresado
            telefono = self.campos['telefono'].text().strip()
            if telefono and not self._validar_formato_telefono(telefono):
                QMessageBox.warning(self, "Error", "El formato del teléfono no es válido")
                self.campos['telefono'].setFocus()
                return False

            # Si todas las validaciones pasan, emitir señal con los datos
            datos = self.obtener_datos()
            self.guardado_success.emit(datos)
            return True

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al validar datos: {str(e)}")
            return False

    def _validar_formato_correo(self, correo):
        """Valida el formato del correo electrónico"""
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(patron, correo))

    def _validar_formato_telefono(self, telefono):
        """Valida el formato del teléfono"""
        patron = r'^\+?[0-9]{9,15}$'
        return bool(re.match(patron, telefono))

    def cancelar(self):
        """Cancela el registro y limpia el formulario"""
        self.limpiar_campos()
        # Emitir señal de cancelación si es necesario
        # self.cancelado.emit()  # Si necesitas manejar la cancelación en el controlador

    def set_modo_lectura(self, enabled=True):
        """Configura el formulario en modo lectura"""
        # Deshabilitar campos de identificación
        self.tipo_doc_combo.setEnabled(not enabled)
        self.num_doc_input.setEnabled(not enabled)

        # Deshabilitar campos personales
        for campo in self.campos.values():
            if isinstance(campo, (QLineEdit, QComboBox, QDateEdit)):
                campo.setEnabled(not enabled)
        
        self.check_eimsa.setEnabled(not enabled)
        
        # Deshabilitar experiencias
        self.btn_agregar_experiencia.setEnabled(not enabled)
        
        # Mostrar/ocultar botones según corresponda
        self.btn_guardar.setVisible(not enabled)
        self.btn_cancelar.setVisible(not enabled)