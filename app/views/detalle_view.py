from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame
)
from PyQt5.QtCore import Qt


class DetalleView(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Área scrollable para el contenido
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        # Widget contenedor
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        
        # Sección de datos personales
        self.datos_personales = QFrame()
        self.datos_personales.setFrameStyle(QFrame.StyledPanel)
        datos_layout = QVBoxLayout(self.datos_personales)
        
        self.lbl_titulo_datos = QLabel("Datos Personales")
        self.lbl_titulo_datos.setStyleSheet("font-size: 16px; font-weight: bold;")
        datos_layout.addWidget(self.lbl_titulo_datos)
        
        self.grid_datos = QVBoxLayout()
        datos_layout.addLayout(self.grid_datos)
        
        self.content_layout.addWidget(self.datos_personales)
        
        # Sección de experiencias
        self.experiencias = QFrame()
        self.experiencias.setFrameStyle(QFrame.StyledPanel)
        exp_layout = QVBoxLayout(self.experiencias)
        
        self.lbl_titulo_exp = QLabel("Experiencia Laboral")
        self.lbl_titulo_exp.setStyleSheet("font-size: 16px; font-weight: bold;")
        exp_layout.addWidget(self.lbl_titulo_exp)
        
        self.experiencias_layout = QVBoxLayout()
        exp_layout.addLayout(self.experiencias_layout)
        
        self.content_layout.addWidget(self.experiencias)
        
        scroll.setWidget(self.content_widget)
        layout.addWidget(scroll)
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        self.btn_editar = QPushButton("Editar")
        self.btn_generar_cv = QPushButton("Generar CV")
        self.btn_volver = QPushButton("Volver")
        
        buttons_layout.addWidget(self.btn_editar)
        buttons_layout.addWidget(self.btn_generar_cv)
        buttons_layout.addWidget(self.btn_volver)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def mostrar_datos(self, datos_personales, experiencias):
        """Muestra los datos del registro en los campos correspondientes"""
        if not datos_personales:
            raise ValueError("Datos personales no proporcionados.")
        if experiencias is None:
            experiencias = []

        # Limpiar layouts previos
        self._limpiar_layout(self.grid_datos)
        self._limpiar_layout(self.experiencias_layout)

        # Mostrar datos personales
        campos = [
            ('Código:', datos_personales.get('codigo', '')),
            ('Apellidos y Nombres:', datos_personales.get('nombres', '')),
            ('Profesión:', datos_personales.get('profesion', '')),
            ('Área:', datos_personales.get('area', '')),
            ('Cargo:', datos_personales.get('cargo', '')),
            ('Fecha de Nacimiento:', datos_personales.get('fecha_nacimiento', '')),
            ('Lugar de Nacimiento:', datos_personales.get('lugar_nacimiento', '')),
            ('Registro CIP:', datos_personales.get('registro_cip', '')),
            ('Residencia:', datos_personales.get('residencia', '')),
            ('Teléfono:', datos_personales.get('telefono', '')),
            ('Correo:', datos_personales.get('correo', ''))
        ]
        
        for label_text, valor in campos:
            if valor:
                container = QWidget()
                layout = QHBoxLayout(container)
                label = QLabel(label_text)
                label.setMinimumWidth(150)
                label.setStyleSheet("font-weight: bold;")
                valor_label = QLabel(str(valor))
                layout.addWidget(label)
                layout.addWidget(valor_label)
                layout.addStretch()
                self.grid_datos.addWidget(container)
        
        # Mostrar experiencias
        for exp in experiencias:
            exp_frame = QFrame()
            exp_frame.setFrameStyle(QFrame.StyledPanel)
            exp_layout = QVBoxLayout(exp_frame)
            
            # Título de la experiencia
            titulo = QLabel(f"{exp.get('cargo', 'N/A')} en {exp.get('empresa', 'N/A')}")
            titulo.setStyleSheet("font-weight: bold; font-size: 14px;")
            exp_layout.addWidget(titulo)
            
            # Detalles de la experiencia
            detalles = [
                ('Obra:', exp.get('obra', 'N/A')),
                ('Periodo:', f"{exp.get('fecha_inicio', '')} - {exp.get('fecha_fin', 'Actualidad')}"),
                ('Tipo de Obra:', exp.get('tipo_obra', 'N/A')),
                ('Monto del Proyecto:', exp.get('monto_proyecto', 'N/A')),
                ('Propietario:', exp.get('propietario', 'N/A'))
            ]
            
            for label_text, valor in detalles:
                if valor:
                    container = QWidget()
                    layout = QHBoxLayout(container)
                    label = QLabel(label_text)
                    label.setMinimumWidth(120)
                    label.setStyleSheet("font-weight: bold;")
                    valor_label = QLabel(str(valor))
                    layout.addWidget(label)
                    layout.addWidget(valor_label)
                    layout.addStretch()
                    exp_layout.addWidget(container)
            
            # Funciones
            if exp.get('funciones'):
                funciones_label = QLabel("Funciones:")
                funciones_label.setStyleSheet("font-weight: bold;")
                exp_layout.addWidget(funciones_label)
                
                funciones = exp['funciones'].split('\n')
                for funcion in funciones:
                    if funcion.strip():
                        func_label = QLabel(f"• {funcion.strip()}")
                        exp_layout.addWidget(func_label)
            
            self.experiencias_layout.addWidget(exp_frame)
        
        # Agregar espacio al final
        self.experiencias_layout.addStretch()
    
    def _limpiar_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._limpiar_layout(item.layout())
    