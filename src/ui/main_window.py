"""
Ventana Principal de Wikia Cognitiva

Este módulo define la ventana principal de la aplicación que integra
todos los componentes: navegación, contenido y búsqueda.
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QSplitter, QStatusBar, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QIcon
import logging

from ..core.data_manager import DataManager
from .navigation_panel import NavigationPanel
from .content_viewer import ContentViewer
from .search_bar import SearchBar


# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    Ventana principal de la aplicación.
    
    Integra:
    - Barra de búsqueda superior
    - Panel de navegación izquierdo (árbol de semestres/materias/temas)
    - Panel de contenido derecho (visualización de temas)
    - Barra de estado inferior
    
    Attributes:
        data_manager (DataManager): Gestor central de datos
        navigation_panel (NavigationPanel): Panel de navegación
        content_viewer (ContentViewer): Visor de contenido
        search_bar (SearchBar): Barra de búsqueda
        initialized (bool): Estado de inicialización
    """
    
    def __init__(self):
        """Inicializa la ventana principal."""
        super().__init__()
        
        self.initialized = False
        
        # Inicializar Data Manager
        logger.info("Inicializando Data Manager...")
        self.data_manager = DataManager()
        
        # Configurar UI
        self.setup_ui()
        
        # Cargar datos
        self.load_data()
    
    def setup_ui(self):
        """Configura la interfaz de usuario."""
        # Configurar ventana
        self.setWindowTitle("Wikia Cognitiva - Licenciatura en Inteligencia Artificial")
        self.setGeometry(100, 100, 1400, 900)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal vertical
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # === BARRA DE BÚSQUEDA SUPERIOR ===
        self.search_bar = SearchBar()
        self.search_bar.search_triggered.connect(self.on_search)
        main_layout.addWidget(self.search_bar)
        
        # === SPLITTER HORIZONTAL (Navegación | Contenido) ===
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)  # No permitir colapsar paneles
        
        # Panel de navegación (izquierda)
        self.navigation_panel = NavigationPanel()
        self.navigation_panel.topic_selected.connect(self.on_topic_selected)
        splitter.addWidget(self.navigation_panel)
        
        # Visor de contenido (derecha)
        self.content_viewer = ContentViewer()
        splitter.addWidget(self.content_viewer)
        
        # Configurar proporciones: 25% navegación, 75% contenido
        splitter.setSizes([350, 1050])
        splitter.setStretchFactor(0, 1)  # Navegación menos flexible
        splitter.setStretchFactor(1, 3)  # Contenido más flexible
        
        main_layout.addWidget(splitter)
        
        # === BARRA DE ESTADO ===
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Listo")
        
        logger.info("✅ Interfaz configurada")
    
    def load_data(self):
        """Carga los datos del curriculum."""
        try:
            logger.info("Cargando curriculum...")
            self.status_bar.showMessage("Cargando curriculum...")
            
            # Inicializar Data Manager
            if not self.data_manager.initialize():
                logger.error("❌ Error inicializando Data Manager")
                self.show_error(
                    "Error de Carga",
                    "No se pudo cargar el curriculum.\n\n"
                    "Verifica que el archivo curriculum.json existe."
                )
                return
            
            # Obtener semestres
            semestres = self.data_manager.get_semestres()
            
            if not semestres:
                logger.warning("⚠️  No se encontraron semestres")
                self.show_warning(
                    "Advertencia",
                    "No se encontraron semestres en el curriculum."
                )
                return
            
            # Cargar semestres en el panel de navegación
            self.navigation_panel.load_semestres(semestres)
            
            # Obtener estadísticas
            stats = self.data_manager.get_estadisticas_generales()
            
            # Actualizar barra de estado
            status_msg = (
                f"Cargados: {stats['total_semestres']} semestres, "
                f"{stats['total_materias']} materias, "
                f"{stats['total_temas']} temas"
            )
            self.status_bar.showMessage(status_msg)
            
            self.initialized = True
            logger.info("✅ Datos cargados exitosamente")
            
        except Exception as e:
            logger.error(f"❌ Error cargando datos: {e}")
            self.show_error(
                "Error Fatal",
                f"Error al cargar los datos:\n\n{str(e)}"
            )
    
    def is_initialized(self) -> bool:
        """
        Verifica si la ventana se inicializó correctamente.
        
        Returns:
            bool: True si está inicializada
        """
        return self.initialized
    
    # ==================== SLOTS ====================
    
    @pyqtSlot(int, str, str)
    def on_topic_selected(self, semestre_num: int, materia_id: str, tema_archivo: str):
        """
        Maneja la selección de un tema desde el panel de navegación.
        
        Args:
            semestre_num: Número del semestre
            materia_id: ID de la materia
            tema_archivo: Nombre del archivo del tema
        """
        try:
            logger.info(f"Cargando tema: {semestre_num}/{materia_id}/{tema_archivo}")
            self.status_bar.showMessage(f"Cargando tema...")
            
            # Cargar tema desde Data Manager
            topic = self.data_manager.get_topic(
                semestre_num, 
                materia_id, 
                tema_archivo
            )
            
            if not topic:
                logger.error("❌ No se pudo cargar el tema")
                self.show_error(
                    "Error de Carga",
                    f"No se pudo cargar el tema:\n{tema_archivo}"
                )
                return
            
            # Mostrar tema en el visor de contenido
            self.content_viewer.display_topic(topic)
            
            # Actualizar barra de estado
            self.status_bar.showMessage(
                f"Tema cargado: {topic.titulo} ({topic.materia})"
            )
            
            logger.info(f"✅ Tema mostrado: {topic.titulo}")
            
        except Exception as e:
            logger.error(f"❌ Error al cargar tema: {e}")
            self.show_error(
                "Error",
                f"Error al cargar el tema:\n\n{str(e)}"
            )
    
    @pyqtSlot(str)
    def on_search(self, query: str):
        """
        Maneja la búsqueda de temas.
        
        Args:
            query: Término de búsqueda
        """
        try:
            if not query.strip():
                return
            
            logger.info(f"Buscando: {query}")
            self.status_bar.showMessage(f"Buscando: {query}...")
            
            # Buscar temas
            resultados = self.data_manager.buscar_temas(query)
            
            if not resultados:
                self.status_bar.showMessage(f"No se encontraron resultados para: {query}")
                self.show_info(
                    "Sin Resultados",
                    f"No se encontraron temas que coincidan con:\n'{query}'"
                )
                return
            
            # Actualizar navegación con resultados
            self.navigation_panel.show_search_results(resultados)
            
            # Actualizar barra de estado
            self.status_bar.showMessage(
                f"Encontrados {len(resultados)} resultados para: {query}"
            )
            
            logger.info(f"✅ Búsqueda completada: {len(resultados)} resultados")
            
        except Exception as e:
            logger.error(f"❌ Error en búsqueda: {e}")
            self.show_error(
                "Error de Búsqueda",
                f"Error al buscar:\n\n{str(e)}"
            )
    
    # ==================== DIÁLOGOS ====================
    
    def show_error(self, title: str, message: str):
        """Muestra un diálogo de error."""
        QMessageBox.critical(self, title, message)
    
    def show_warning(self, title: str, message: str):
        """Muestra un diálogo de advertencia."""
        QMessageBox.warning(self, title, message)
    
    def show_info(self, title: str, message: str):
        """Muestra un diálogo de información."""
        QMessageBox.information(self, title, message)
    
    # ==================== EVENTOS ====================
    
    def closeEvent(self, event):
        """
        Maneja el evento de cierre de la ventana.
        
        Args:
            event: Evento de cierre
        """
        # Limpiar caché antes de cerrar
        if self.data_manager:
            logger.info("Limpiando caché...")
            self.data_manager.limpiar_cache()
        
        logger.info("👋 Cerrando aplicación")
        event.accept()
