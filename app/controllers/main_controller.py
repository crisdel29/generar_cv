# controllers/main_controller.py
import logging
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QFileDialog, QLineEdit, QComboBox, QDateEdit
from PyQt5.QtCore import Qt
from datetime import datetime
from app.views.main_view import MainView
from app.models.database import Database
from app.utils.cv_generator import CVGenerator
from app.views.widgets.experiencia_widget import ExperienciaWidget

logger = logging.getLogger(__name__)

class MainController:
    def __init__(self):
        try:
            logger.debug("Inicializando MainController...")
            self.view = MainView()
            self.db = Database()
            self.experiencias_widgets = []
            self.setup_connections()
            self.cargar_datos_iniciales()
            logger.debug("MainController inicializado correctamente")
        except Exception as e:
            logger.error(f"Error al inicializar MainController: {str(e)}")
            raise

    def setup_connections(self):
        try:
            logger.debug("Configurando conexiones...")
            
            # Conexiones del tab de registro
            self.view.tab_registro.btn_guardar.clicked.connect(self.guardar_registro)
            self.view.tab_registro.btn_cancelar.clicked.connect(self.cancelar_registro)
            self.view.tab_registro.btn_agregar_experiencia.clicked.connect(self.agregar_experiencia)
            
            # Conexiones del tab de búsqueda
            self.view.tab_busqueda.btn_buscar.clicked.connect(self.realizar_busqueda)
            self.view.tab_busqueda.btn_limpiar.clicked.connect(self.limpiar_filtros)
            
            logger.debug("Conexiones configuradas correctamente")
        except Exception as e:
            logger.error(f"Error al configurar conexiones: {str(e)}")
            raise

    def cargar_datos_iniciales(self):
        try:
            self.actualizar_tabla_resultados()
        except Exception as e:
            logger.error(f"Error al cargar datos iniciales: {str(e)}")
            QMessageBox.critical(self.view, "Error", f"Error al cargar datos iniciales: {str(e)}")

    def realizar_busqueda(self):
        try:
            filtros = {
                'texto': self.view.tab_busqueda.busqueda_input.text().strip(),
                'area': self.view.tab_busqueda.area_filtro.currentText(),
                'tipo_obra': self.view.tab_busqueda.tipo_obra_filtro.currentText(),
                'cargo': self.view.tab_busqueda.cargo_filtro.text().strip(),
                'ex_eimsa': self.view.tab_busqueda.check_eimsa_filtro.isChecked(),
                'años_exp': self.view.tab_busqueda.años_exp_filtro.currentText()
            }
            resultados = self.db.buscar_registros(filtros)
            self.actualizar_tabla_resultados(resultados)
        except Exception as e:
            logger.error(f"Error en búsqueda: {str(e)}")
            QMessageBox.critical(self.view, "Error", f"Error al realizar la búsqueda: {str(e)}")

    def actualizar_tabla_resultados(self, resultados=None):
        try:
            if resultados is None:
                resultados = self.db.obtener_todos_registros()

            tabla = self.view.tab_busqueda.tabla_resultados
            tabla.setRowCount(0)

            for row, datos in enumerate(resultados):
                tabla.insertRow(row)
                
                # Convertir Row a diccionario si es necesario
                if not isinstance(datos, dict):
                    datos = dict(datos)

                items = [
                    datos.get('codigo', ''),
                    f"{datos.get('tipo_documento', '')} {datos.get('numero_documento', '')}",
                    f"{datos.get('nombres', '')} {datos.get('apellidos', '')}",
                    datos.get('profesion', ''),
                    datos.get('area', ''),
                    datos.get('cargo', ''),
                    datos.get('años_experiencia', '0'),
                    datos.get('ciudad_residencia', ''),
                    'Sí' if datos.get('trabajado_eimsa') else 'No',
                    datos.get('fecha_registro', '')
                ]

                for col, valor in enumerate(items):
                    item = QTableWidgetItem(str(valor))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    tabla.setItem(row, col, item)

            tabla.resizeColumnsToContents()

        except Exception as e:
            logger.error(f"Error al actualizar tabla: {str(e)}")
            QMessageBox.critical(self.view, "Error", f"Error al actualizar tabla: {str(e)}")

    def limpiar_filtros(self):
        try:
            tab_busqueda = self.view.tab_busqueda
            tab_busqueda.busqueda_input.clear()
            tab_busqueda.area_filtro.setCurrentIndex(0)
            tab_busqueda.tipo_obra_filtro.setCurrentIndex(0)
            tab_busqueda.cargo_filtro.clear()
            tab_busqueda.check_eimsa_filtro.setChecked(False)
            tab_busqueda.años_exp_filtro.setCurrentIndex(0)
            self.actualizar_tabla_resultados()
        except Exception as e:
            logger.error(f"Error al limpiar filtros: {str(e)}")
            QMessageBox.critical(self.view, "Error", f"Error al limpiar filtros: {str(e)}")

    def ver_detalle(self):
        try:
            registro_seleccionado = self.obtener_registro_seleccionado()
            if registro_seleccionado:
                # Cambiar a la pestaña de registro en modo lectura
                self.view.tab_widget.setCurrentWidget(self.view.tab_registro)
                self.cargar_datos_registro(registro_seleccionado, modo_lectura=True)
        except Exception as e:
            logger.error(f"Error al ver detalle: {str(e)}")
            QMessageBox.critical(self.view, "Error", f"Error al ver detalle: {str(e)}")

    def editar_registro(self):
        try:
            registro_seleccionado = self.obtener_registro_seleccionado()
            if registro_seleccionado:
                # Cambiar a la pestaña de registro en modo edición
                self.view.tab_widget.setCurrentWidget(self.view.tab_registro)
                self.cargar_datos_registro(registro_seleccionado, modo_lectura=False)
        except Exception as e:
            logger.error(f"Error al editar registro: {str(e)}")
            QMessageBox.critical(self.view, "Error", f"Error al editar registro: {str(e)}")

    def obtener_registro_seleccionado(self):
        tabla = self.view.tab_busqueda.tabla_resultados
        indices_seleccionados = tabla.selectedItems()
        if indices_seleccionados:
            fila = indices_seleccionados[0].row()
            codigo = tabla.item(fila, 0).text()
            return self.db.obtener_registro(codigo)
        return None

    def guardar_registro(self):
        try:
            datos = self.obtener_datos_formulario()
            if self.validar_datos(datos):
                self.db.guardar_registro(datos)
                QMessageBox.information(self.view, "Éxito", "Registro guardado correctamente")
                self.view.tab_widget.setCurrentWidget(self.view.tab_busqueda)
                self.actualizar_tabla_resultados()
        except Exception as e:
            logger.error(f"Error al guardar registro: {str(e)}")
            QMessageBox.critical(self.view, "Error", f"Error al guardar registro: {str(e)}")

    def cancelar_registro(self):
        self.view.tab_widget.setCurrentWidget(self.view.tab_busqueda)
    
    def generar_cv(self):
        try:
            registro_seleccionado = self.obtener_registro_seleccionado()
            if registro_seleccionado:
                # Generar nombre del archivo
                nombre_archivo = f"CV_{registro_seleccionado.get('nombres', 'sin_nombre')}_{datetime.now().strftime('%Y%m%d')}.docx"
                ruta_salida, _ = QFileDialog.getSaveFileName(
                    self.view,
                    "Guardar CV",
                    nombre_archivo,
                    "Documentos Word (*.docx)"
                )
                
                if ruta_salida:
                    try:
                        generator = CVGenerator()
                        experiencias = self.db.obtener_experiencias(registro_seleccionado['codigo'])
                        if generator.generar(registro_seleccionado, experiencias, ruta_salida):
                            QMessageBox.information(
                                self.view,
                                "Éxito",
                                f"CV generado correctamente en:\n{ruta_salida}"
                            )
                            # Abrir el archivo generado
                            from os import startfile
                            startfile(ruta_salida)
                        else:
                            QMessageBox.warning(
                                self.view,
                                "Advertencia",
                                "No se pudo generar el CV. Verifique que los datos estén completos."
                            )
                    except Exception as e:
                        QMessageBox.critical(
                            self.view,
                            "Error",
                            f"Error al generar CV: {str(e)}"
                        )
        except Exception as e:
            logger.error(f"Error al generar CV: {str(e)}")
            QMessageBox.critical(self.view, "Error", f"Error al generar CV: {str(e)}")

    def obtener_datos_formulario(self):
        """Obtiene todos los datos del formulario de registro"""
        try:
            tab_registro = self.view.tab_registro
            return {
                'codigo': tab_registro.codigo_input.text(),
                'tipo_documento': tab_registro.tipo_doc_combo.currentText(),
                'numero_documento': tab_registro.num_doc_input.text(),
                'nombres': tab_registro.nombres_input.text(),
                'apellidos': tab_registro.apellidos_input.text(),
                'profesion': tab_registro.profesion_input.text(),
                'fecha_nacimiento': tab_registro.fecha_nac_input.date().toString('yyyy-MM-dd'),
                'lugar_nacimiento': tab_registro.lugar_nac_input.text(),
                'registro_cip': tab_registro.registro_cip_input.text(),
                'area': tab_registro.area_combo.currentText(),
                'cargo': tab_registro.cargo_input.text(),
                'residencia': tab_registro.residencia_input.text(),
                'telefono': tab_registro.telefono_input.text(),
                'correo': tab_registro.correo_input.text(),
                'trabajado_eimsa': tab_registro.check_eimsa.isChecked(),
                'experiencias': self.obtener_experiencias_formulario()
            }
        except Exception as e:
            logger.error(f"Error al obtener datos del formulario: {str(e)}")
            raise

    def obtener_experiencias_formulario(self):
        """Obtiene la lista de experiencias del formulario"""
        experiencias = []
        for widget in self.experiencias_widgets:
            experiencias.append(widget.obtener_datos())
        return experiencias

    def agregar_experiencia(self):
        try:
            dialogo = ExperienciaWidget(parent=self.view)
            if dialogo.exec_():  # Usar exec_ en lugar de exec() para Qt
                datos = dialogo.obtener_datos()
                self.view.tab_registro.experiencias_layout.addWidget(
                    ExperienciaWidget(datos=datos, parent=self.view.tab_registro)
                )
        except Exception as e:
            logger.error(f"Error al agregar experiencia: {str(e)}")
            QMessageBox.critical(self.view, "Error", f"Error al agregar experiencia: {str(e)}")

    def eliminar_experiencia(self, widget):
        """Elimina una experiencia del formulario"""
        try:
            widget.setParent(None)
            widget.deleteLater()
            self.experiencias_widgets.remove(widget)
        except Exception as e:
            logger.error(f"Error al eliminar experiencia: {str(e)}")
            QMessageBox.critical(self.view, "Error", f"Error al eliminar experiencia: {str(e)}")

    def actualizar_experiencia(self, datos):
        """Actualiza los datos de una experiencia"""
        try:
            # Aquí puedes agregar lógica adicional si necesitas
            # hacer algo cuando se actualiza una experiencia
            pass
        except Exception as e:
            logger.error(f"Error al actualizar experiencia: {str(e)}")
            QMessageBox.critical(self.view, "Error", f"Error al actualizar experiencia: {str(e)}")

    def cargar_datos_registro(self, datos, modo_lectura=False):
        """Carga los datos en el formulario de registro"""
        try:
            tab_registro = self.view.tab_registro
            
            # Limpiar experiencias existentes
            for widget in self.experiencias_widgets:
                widget.setParent(None)
                widget.deleteLater()
            self.experiencias_widgets.clear()
            
            # Cargar datos básicos
            tab_registro.codigo_input.setText(datos.get('codigo', ''))
            tab_registro.tipo_doc_combo.setCurrentText(datos.get('tipo_documento', 'DNI'))
            tab_registro.num_doc_input.setText(datos.get('numero_documento', ''))
            tab_registro.nombres_input.setText(datos.get('nombres', ''))
            tab_registro.apellidos_input.setText(datos.get('apellidos', ''))
            tab_registro.profesion_input.setText(datos.get('profesion', ''))
            # ... (continuar con el resto de campos)
            
            # Cargar experiencias
            experiencias = self.db.obtener_experiencias(datos['codigo'])
            for exp in experiencias:
                widget = ExperienciaWidget(datos=exp, parent=self.view.tab_registro)
                widget.eliminado.connect(lambda w=widget: self.eliminar_experiencia(w))
                widget.actualizado.connect(self.actualizar_experiencia)
                self.experiencias_widgets.append(widget)
                self.view.tab_registro.experiencias_layout.addWidget(widget)
                
            # Configurar modo lectura si es necesario
            if modo_lectura:
                self.set_modo_lectura(True)
                
        except Exception as e:
            logger.error(f"Error al cargar datos en registro: {str(e)}")
            QMessageBox.critical(self.view, "Error", f"Error al cargar datos: {str(e)}")

    def set_modo_lectura(self, enabled=True):
        """Configura el formulario en modo lectura"""
        tab_registro = self.view.tab_registro
        for widget in tab_registro.findChildren((QLineEdit, QComboBox, QDateEdit)):
            widget.setReadOnly(enabled)
            widget.setEnabled(not enabled)
        tab_registro.btn_guardar.setVisible(not enabled)
        # Deshabilitar botones de experiencia en modo lectura
        for exp_widget in self.experiencias_widgets:
            exp_widget.set_modo_lectura(enabled)

    def __init__(self):
        try:
            logger.debug("Inicializando MainController...")
            self.view = MainView()
            self.db = Database()
            self.experiencias_widgets = []  # Lista para mantener referencia a widgets de experiencia
            self.setup_connections()
            self.cargar_datos_iniciales()
            logger.debug("MainController inicializado correctamente")
        except Exception as e:
            logger.error(f"Error al inicializar MainController: {str(e)}", exc_info=True)
            raise