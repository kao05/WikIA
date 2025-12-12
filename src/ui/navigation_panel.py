"""
Panel de Navegación

Este módulo implementa el panel izquierdo con el árbol de navegación
que muestra semestres, materias y temas.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem,
    QLabel, QPushButton, QHBoxLayout, QLineEdit, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QIcon, QFont, QColor, QBrush
from typing import List, Dict, Any, Optional
import logging

from ..models.semester import Semester


# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NavigationPanel(QWidget):
    """
    Panel de navegación con árbol de semestres/materias/temas.
    
    Signals:
        topic_selected: Emitido cuando se selecciona un tema
                       (semestre_num, materia_id, tema_archivo)
        search_requested: Emitido cuando se solicita búsqueda (query)
    
    Attributes:
        tree (QTreeWidget): Árbol de navegación
        semestres_data (List[Semester]): Datos de semestres cargados
        current_selection (QTreeWidgetItem): Item actualmente seleccionado
        search_mode (bool): Si está en modo búsqueda
    """
    
    # Señales
    topic_selected = pyqtSignal(int, str, str)  # semestre, materia_id, archivo
    search_requested = pyqtSignal(str)  # query
    
    def __init__(self, parent=None):
        """Inicializa el panel de navegación."""
        super().__init__(parent)
        self.semestres_data = []
        self.current_selection = None
        self.search_mode = False
        self.expanded = False
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz del panel."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # === ENCABEZADO ===
        self._setup_header(layout)
        
        # === FILTRO RÁPIDO ===
        self._setup_quick_filter(layout)
        
        # === ÁRBOL DE NAVEGACIÓN ===
        self._setup_tree(layout)
        
        # === INFORMACIÓN DE ESTADO ===
        self._setup_status_info(layout)
        
        # === BOTONES DE ACCIÓN ===
        self._setup_action_buttons(layout)
    
    def _setup_header(self, layout: QVBoxLayout):
        """Configura el encabezado del panel."""
        header_layout = QHBoxLayout()
        
        # Título
        title_label = QLabel("📚 Plan de Estudios")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50; padding: 5px;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Botón para expandir/colapsar todo
        self.expand_button = QPushButton("Expandir")
        self.expand_button.setMaximumWidth(100)
        self.expand_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.expand_button.clicked.connect(self.toggle_expand_all)
        header_layout.addWidget(self.expand_button)
        
        layout.addLayout(header_layout)
    
    def _setup_quick_filter(self, layout: QVBoxLayout):
        """Configura el filtro rápido de búsqueda local."""
        filter_layout = QHBoxLayout()
        
        # Campo de filtro
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("🔍 Filtrar temas...")
        self.filter_input.setClearButtonEnabled(True)
        self.filter_input.textChanged.connect(self._on_filter_changed)
        self.filter_input.setStyleSheet("""
            QLineEdit {
                padding: 6px;
                border: 2px solid #bdc3c7;
                border-radius: 4px;
                font-size: 11px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        filter_layout.addWidget(self.filter_input)
        
        # Botón para limpiar filtro
        clear_filter_btn = QPushButton("✕")
        clear_filter_btn.setMaximumWidth(30)
        clear_filter_btn.setToolTip("Limpiar filtro")
        clear_filter_btn.clicked.connect(self._clear_filter)
        clear_filter_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        filter_layout.addWidget(clear_filter_btn)
        
        layout.addLayout(filter_layout)
    
    def _setup_tree(self, layout: QVBoxLayout):
        """Configura el árbol de navegación."""
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Contenido")
        self.tree.setAlternatingRowColors(True)
        self.tree.setAnimated(True)
        self.tree.setIndentation(20)
        
        # Configurar comportamiento
        self.tree.setExpandsOnDoubleClick(True)
        self.tree.itemClicked.connect(self.on_item_clicked)
        self.tree.itemDoubleClicked.connect(self.on_item_double_clicked)
        
        # Estilo del árbol
        self.tree.setStyleSheet("""
            QTreeWidget {
                background-color: white;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 5px;
                font-size: 12px;
            }
            QTreeWidget::item {
                padding: 5px;
                border-radius: 3px;
            }
            QTreeWidget::item:hover {
                background-color: #ecf0f1;
            }
            QTreeWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QTreeWidget::branch:has-siblings:!adjoins-item {
                border-image: url(vline.png) 0;
            }
            QTreeWidget::branch:has-siblings:adjoins-item {
                border-image: url(branch-more.png) 0;
            }
            QTreeWidget::branch:!has-children:!has-siblings:adjoins-item {
                border-image: url(branch-end.png) 0;
            }
        """)
        
        layout.addWidget(self.tree)
    
    def _setup_status_info(self, layout: QVBoxLayout):
        """Configura la información de estado."""
        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("background-color: #bdc3c7;")
        layout.addWidget(separator)
        
        # Label de información
        self.info_label = QLabel("No hay contenido cargado")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet("""
            color: #7f8c8d; 
            padding: 8px;
            font-size: 11px;
            background-color: #ecf0f1;
            border-radius: 3px;
        """)
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)
    
    def _setup_action_buttons(self, layout: QVBoxLayout):
        """Configura los botones de acción adicionales."""
        button_layout = QHBoxLayout()
        
        # Botón para volver a vista normal (después de búsqueda)
        self.back_button = QPushButton("← Volver")
        self.back_button.setVisible(False)
        self.back_button.clicked.connect(self.clear_search_results)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                padding: 5px 10px;
                border-radius: 3px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        button_layout.addWidget(self.back_button)
        
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
    
    def load_semestres(self, semestres: List[Semester]):
        """
        Carga los semestres en el árbol de navegación.
        
        Args:
            semestres: Lista de objetos Semester
        """
        try:
            logger.info(f"Cargando {len(semestres)} semestres en navegación...")
            
            self.semestres_data = semestres
            self.search_mode = False
            self.back_button.setVisible(False)
            self.tree.clear()
            
            total_temas = 0
            total_materias = 0
            
            # Crear items del árbol
            for semestre in semestres:
                # === NIVEL 1: SEMESTRE ===
                sem_item = self._create_semestre_item(semestre)
                total_materias += len(semestre.materias)
                
                # === NIVEL 2: MATERIAS ===
                for materia in semestre.materias:
                    mat_item = self._create_materia_item(materia, semestre.numero)
                    
                    # === NIVEL 3: TEMAS ===
                    for tema_info in materia.temas:
                        tema_item = self._create_tema_item(
                            tema_info, 
                            semestre.numero, 
                            materia.id
                        )
                        mat_item.addChild(tema_item)
                        total_temas += 1
                    
                    sem_item.addChild(mat_item)
                
                self.tree.addTopLevelItem(sem_item)
            
            # Actualizar información
            self._update_info_label(len(semestres), total_materias, total_temas)
            
            logger.info(f"✅ Navegación cargada: {total_temas} temas")
            
        except Exception as e:
            logger.error(f"❌ Error cargando navegación: {e}")
            self.info_label.setText("❌ Error al cargar contenido")
            self.info_label.setStyleSheet("color: #e74c3c; padding: 8px;")
    
    def _create_semestre_item(self, semestre: Semester) -> QTreeWidgetItem:
        """Crea un item de semestre para el árbol."""
        sem_item = QTreeWidgetItem([f"📘 Semestre {semestre.numero}: {semestre.nombre}"])
        sem_item.setData(0, Qt.ItemDataRole.UserRole, {
            'type': 'semestre',
            'numero': semestre.numero,
            'nombre': semestre.nombre
        })
        
        # Estilo para semestre
        font = QFont()
        font.setBold(True)
        font.setPointSize(11)
        sem_item.setFont(0, font)
        
        # Color de fondo suave
        sem_item.setBackground(0, QBrush(QColor(236, 240, 241)))
        
        # Tooltip
        sem_item.setToolTip(0, f"{semestre.total_materias} materias • {semestre.total_creditos} créditos")
        
        return sem_item
    
    def _create_materia_item(self, materia, semestre_num: int) -> QTreeWidgetItem:
        """Crea un item de materia para el árbol."""
        mat_item = QTreeWidgetItem([f"📖 {materia.nombre}"])
        mat_item.setData(0, Qt.ItemDataRole.UserRole, {
            'type': 'materia',
            'semestre': semestre_num,
            'materia_id': materia.id,
            'creditos': materia.creditos,
            'nombre': materia.nombre
        })
        
        # Estilo para materia
        font = QFont()
        font.setPointSize(10)
        mat_item.setFont(0, font)
        
        # Tooltip
        mat_item.setToolTip(0, f"{materia.creditos} créditos • {materia.total_temas} temas")
        
        return mat_item
    
    def _create_tema_item(
        self, 
        tema_info: Dict[str, str], 
        semestre_num: int, 
        materia_id: str
    ) -> QTreeWidgetItem:
        """Crea un item de tema para el árbol."""
        tema_item = QTreeWidgetItem([f"📄 {tema_info['nombre']}"])
        tema_item.setData(0, Qt.ItemDataRole.UserRole, {
            'type': 'tema',
            'semestre': semestre_num,
            'materia_id': materia_id,
            'tema_id': tema_info['id'],
            'archivo': tema_info['archivo'],
            'nombre': tema_info['nombre']
        })
        
        # Estilo para tema
        font = QFont()
        font.setPointSize(10)
        tema_item.setFont(0, font)
        
        # Tooltip
        tema_item.setToolTip(0, f"Click para abrir: {tema_info['nombre']}")
        
        return tema_item
    
    def _update_info_label(self, num_semestres: int, num_materias: int, num_temas: int):
        """Actualiza el label de información."""
        self.info_label.setText(
            f"📚 {num_semestres} semestres • {num_materias} materias • {num_temas} temas"
        )
        self.info_label.setStyleSheet("""
            color: #2c3e50; 
            padding: 8px;
            font-size: 11px;
            background-color: #d5f4e6;
            border-radius: 3px;
            font-weight: bold;
        """)
    
    def on_item_clicked(self, item: QTreeWidgetItem, column: int):
        """
        Maneja el clic en un item del árbol.
        
        Args:
            item: Item clickeado
            column: Columna clickeada
        """
        data = item.data(0, Qt.ItemDataRole.UserRole)
        
        if not data:
            return
        
        item_type = data.get('type')
        
        if item_type == 'tema':
            # Guardar selección actual
            self.current_selection = item
            
            # Resaltar tema seleccionado
            self._highlight_selected_item(item)
            
            # Emitir señal para cargar el tema
            self.topic_selected.emit(
                data['semestre'],
                data['materia_id'],
                data['archivo']
            )
            logger.info(f"Tema seleccionado: {data['nombre']}")
        
        elif item_type == 'materia':
            # Expandir/colapsar materia
            item.setExpanded(not item.isExpanded())
            logger.debug(f"Materia {'expandida' if item.isExpanded() else 'colapsada'}: {data['nombre']}")
        
        elif item_type == 'semestre':
            # Expandir/colapsar semestre
            item.setExpanded(not item.isExpanded())
            logger.debug(f"Semestre {data['numero']} {'expandido' if item.isExpanded() else 'colapsado'}")
    
    def on_item_double_clicked(self, item: QTreeWidgetItem, column: int):
        """
        Maneja el doble clic en un item del árbol.
        
        Args:
            item: Item clickeado
            column: Columna clickeada
        """
        data = item.data(0, Qt.ItemDataRole.UserRole)
        
        if not data:
            return
        
        item_type = data.get('type')
        
        # Doble click en semestre o materia = expandir/colapsar
        if item_type in ['semestre', 'materia']:
            item.setExpanded(not item.isExpanded())
    
    def _highlight_selected_item(self, item: QTreeWidgetItem):
        """Resalta visualmente el item seleccionado."""
        # Limpiar selecciones anteriores
        for i in range(self.tree.topLevelItemCount()):
            self._clear_highlight_recursive(self.tree.topLevelItem(i))
        
        # Resaltar item actual
        font = item.font(0)
        font.setBold(True)
        item.setFont(0, font)
    
    def _clear_highlight_recursive(self, item: QTreeWidgetItem):
        """Limpia el resaltado de un item y sus hijos recursivamente."""
        if item:
            data = item.data(0, Qt.ItemDataRole.UserRole)
            if data and data.get('type') == 'tema':
                font = item.font(0)
                font.setBold(False)
                item.setFont(0, font)
            
            # Procesar hijos
            for i in range(item.childCount()):
                self._clear_highlight_recursive(item.child(i))
    
    def toggle_expand_all(self):
        """Alterna entre expandir y colapsar todo el árbol."""
        self.expanded = not self.expanded
        
        if self.expanded:
            self.tree.expandAll()
            self.expand_button.setText("Colapsar")
            logger.debug("Árbol expandido completamente")
        else:
            self.tree.collapseAll()
            self.expand_button.setText("Expandir")
            logger.debug("Árbol colapsado completamente")
    
    def show_search_results(self, resultados: List[Dict[str, Any]]):
        """
        Muestra los resultados de búsqueda en el árbol.
        
        Args:
            resultados: Lista de diccionarios con info de temas encontrados
        """
        try:
            logger.info(f"Mostrando {len(resultados)} resultados de búsqueda")
            
            self.search_mode = True
            self.back_button.setVisible(True)
            self.tree.clear()
            
            if not resultados:
                # Mostrar mensaje de "sin resultados"
                empty_item = QTreeWidgetItem(["😔 No se encontraron resultados"])
                empty_item.setForeground(0, QBrush(QColor(127, 140, 141)))
                self.tree.addTopLevelItem(empty_item)
                self.info_label.setText("No se encontraron resultados")
                return
            
            # Crear item raíz para resultados
            root = QTreeWidgetItem([f"🔍 Resultados de Búsqueda ({len(resultados)})"])
            font = QFont()
            font.setBold(True)
            font.setPointSize(11)
            root.setFont(0, font)
            root.setBackground(0, QBrush(QColor(255, 243, 205)))
            
            # Agrupar por semestre
            por_semestre = {}
            for resultado in resultados:
                sem = resultado['semestre']
                if sem not in por_semestre:
                    por_semestre[sem] = []
                por_semestre[sem].append(resultado)
            
            # Crear items para cada resultado
            for sem_num in sorted(por_semestre.keys()):
                sem_item = QTreeWidgetItem([f"📘 Semestre {sem_num}"])
                font_sem = QFont()
                font_sem.setBold(True)
                sem_item.setFont(0, font_sem)
                
                for resultado in por_semestre[sem_num]:
                    # Crear item de tema con información adicional
                    tema_text = f"📄 {resultado['tema_nombre']}"
                    materia_text = f"({resultado['materia_nombre']})"
                    
                    tema_item = QTreeWidgetItem([f"{tema_text} {materia_text}"])
                    tema_item.setData(0, Qt.ItemDataRole.UserRole, {
                        'type': 'tema',
                        'semestre': resultado['semestre'],
                        'materia_id': resultado['materia_id'],
                        'archivo': resultado['archivo'],
                        'nombre': resultado['tema_nombre']
                    })
                    
                    # Agregar tooltip con relevancia si existe
                    if 'relevancia' in resultado:
                        tema_item.setToolTip(
                            0, 
                            f"Relevancia: {resultado['relevancia']:.1f}\n"
                            f"Dificultad: {resultado.get('dificultad', 'N/A')}"
                        )
                    
                    # Color según dificultad
                    dificultad = resultado.get('dificultad', '')
                    if dificultad == 'basico':
                        tema_item.setForeground(0, QBrush(QColor(39, 174, 96)))
                    elif dificultad == 'intermedio':
                        tema_item.setForeground(0, QBrush(QColor(230, 126, 34)))
                    elif dificultad == 'avanzado':
                        tema_item.setForeground(0, QBrush(QColor(231, 76, 60)))
                    
                    sem_item.addChild(tema_item)
                
                root.addChild(sem_item)
            
            self.tree.addTopLevelItem(root)
            root.setExpanded(True)
            
            # Expandir primer semestre automáticamente
            if root.childCount() > 0:
                root.child(0).setExpanded(True)
            
            # Actualizar información
            self.info_label.setText(f"🔍 {len(resultados)} resultados encontrados")
            self.info_label.setStyleSheet("""
                color: #2c3e50; 
                padding: 8px;
                font-size: 11px;
                background-color: #fff9e6;
                border-radius: 3px;
            """)
            
            logger.info(f"✅ Resultados mostrados: {len(resultados)} temas")
            
        except Exception as e:
            logger.error(f"❌ Error mostrando resultados: {e}")
            self.info_label.setText("❌ Error mostrando resultados")
    
    def clear_search_results(self):
        """Limpia los resultados de búsqueda y restaura la navegación normal."""
        if self.semestres_data:
            logger.info("Restaurando vista normal de navegación")
            self.load_semestres(self.semestres_data)
            self.filter_input.clear()
    
    def _on_filter_changed(self, text: str):
        """
        Maneja cambios en el filtro local.
        
        Args:
            text: Texto del filtro
        """
        if not text:
            # Mostrar todos los items
            self._show_all_items()
            return
        
        text_lower = text.lower()
        
        # Ocultar todos los items primero
        self._hide_all_items()
        
        # Mostrar solo los que coinciden
        for i in range(self.tree.topLevelItemCount()):
            top_item = self.tree.topLevelItem(i)
            self._filter_item_recursive(top_item, text_lower)
    
    def _filter_item_recursive(self, item: QTreeWidgetItem, filter_text: str) -> bool:
        """
        Filtra items recursivamente.
        
        Args:
            item: Item a filtrar
            filter_text: Texto de filtro
        
        Returns:
            bool: True si el item o algún hijo coincide
        """
        if not item:
            return False
        
        # Verificar si el item coincide
        item_text = item.text(0).lower()
        matches = filter_text in item_text
        
        # Verificar hijos
        has_matching_child = False
        for i in range(item.childCount()):
            child = item.child(i)
            if self._filter_item_recursive(child, filter_text):
                has_matching_child = True
        
        # Mostrar item si coincide o tiene hijos que coinciden
        if matches or has_matching_child:
            item.setHidden(False)
            return True
        else:
            item.setHidden(True)
            return False
    
    def _hide_all_items(self):
        """Oculta todos los items del árbol."""
        for i in range(self.tree.topLevelItemCount()):
            self._hide_item_recursive(self.tree.topLevelItem(i))
    
    def _hide_item_recursive(self, item: QTreeWidgetItem):
        """Oculta un item y sus hijos recursivamente."""
        if item:
            item.setHidden(True)
            for i in range(item.childCount()):
                self._hide_item_recursive(item.child(i))
    
    def _show_all_items(self):
        """Muestra todos los items del árbol."""
        for i in range(self.tree.topLevelItemCount()):
            self._show_item_recursive(self.tree.topLevelItem(i))
    
    def _show_item_recursive(self, item: QTreeWidgetItem):
        """Muestra un item y sus hijos recursivamente."""
        if item:
            item.setHidden(False)
            for i in range(item.childCount()):
                self._show_item_recursive(item.child(i))
    
    def _clear_filter(self):
        """Limpia el filtro local."""
        self.filter_input.clear()
        self._show_all_items()
    
    def get_current_selection(self) -> Optional[Dict[str, Any]]:
        """
        Obtiene la selección actual.
        
        Returns:
            Dict con datos del item seleccionado o None
        """
        if self.current_selection:
            return self.current_selection.data(0, Qt.ItemDataRole.UserRole)
        return None
    
    def select_tema(self, semestre_num: int, materia_id: str, tema_archivo: str):
        """
        Selecciona programáticamente un tema en el árbol.
        
        Args:
            semestre_num: Número de semestre
            materia_id: ID de materia
            tema_archivo: Archivo del tema
        """
        # Buscar el item en el árbol
        for i in range(self.tree.topLevelItemCount()):
            sem_item = self.tree.topLevelItem(i)
            sem_data = sem_item.data(0, Qt.ItemDataRole.UserRole)
            
            if sem_data and sem_data.get('numero') == semestre_num:
                # Expandir semestre
                sem_item.setExpanded(True)
                
                # Buscar materia
                for j in range(sem_item.childCount()):
                    mat_item = sem_item.child(j)
                    mat_data = mat_item.data(0, Qt.ItemDataRole.UserRole)
                    
                    if mat_data and mat_data.get('materia_id') == materia_id:
                        # Expandir materia
                        mat_item.setExpanded(True)
                        
                        # Buscar tema
                        for k in range(mat_item.childCount()):
                            tema_item = mat_item.child(k)
                            tema_data = tema_item.data(0, Qt.ItemDataRole.UserRole)
                            
                            if tema_data and tema_data.get('archivo') == tema_archivo:
                                # Seleccionar y hacer scroll al item
                                self.tree.setCurrentItem(tema_item)
                                self.tree.scrollToItem(tema_item)
                                self.current_selection = tema_item
                                logger.info(f"Tema seleccionado programáticamente: {tema_archivo}")
                                return
        
        logger.warning(f"No se encontró el tema: {semestre_num}/{materia_id}/{tema_archivo}")
    
    def collapse_all_except(self, semestre_num: Optional[int] = None):
        """
        Colapsa todo excepto un semestre específico.
        
        Args:
            semestre_num: Número de semestre a mantener expandido (None = colapsar todo)
        """
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            data = item.data(0, Qt.ItemDataRole.UserRole)
            
            if semestre_num and data and data.get('numero') == semestre_num:
                item.setExpanded(True)
            else:
                item.setExpanded(False)
