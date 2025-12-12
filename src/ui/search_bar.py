"""
Barra de Búsqueda

Este módulo implementa la barra de búsqueda superior
para buscar temas en todo el curriculum.
"""

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QLineEdit, 
    QPushButton, QLabel
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QIcon
import logging


# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SearchBar(QWidget):
    """
    Barra de búsqueda con campo de texto y botón.
    
    Signals:
        search_triggered: Emitido cuando se inicia una búsqueda (query)
    
    Attributes:
        search_input (QLineEdit): Campo de texto para búsqueda
        search_button (QPushButton): Botón de búsqueda
    """
    
    # Señal emitida cuando se realiza una búsqueda
    search_triggered = pyqtSignal(str)
    
    def __init__(self, parent=None):
        """Inicializa la barra de búsqueda."""
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de la barra."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        # Icono de búsqueda
        icon_label = QLabel("🔍")
        icon_label.setStyleSheet("font-size: 18px; padding: 5px;")
        layout.addWidget(icon_label)
        
        # Campo de búsqueda
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar temas, materias o conceptos...")
        self.search_input.setClearButtonEnabled(True)
        self.search_input.returnPressed.connect(self.on_search)
        self.search_input.setMinimumWidth(400)
        
        # Estilo del campo
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #cbd5e1;
                border-radius: 6px;
                font-size: 13px;
                background-color: #ffffff;
                color: #0f172a;
            }
            QLineEdit:focus {
                border-color: #2563eb;
            }
        """)
        
        layout.addWidget(self.search_input, stretch=1)
        
        # Botón de búsqueda
        self.search_button = QPushButton("Buscar")
        self.search_button.clicked.connect(self.on_search)
        self.search_button.setMinimumWidth(100)
        
        # Estilo del botón
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: #f8fafc;
                border: none;
                padding: 8px 20px;
                border-radius: 6px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:pressed {
                background-color: #1e40af;
            }
        """)
        
        layout.addWidget(self.search_button)
        
        # Botón para limpiar búsqueda
        self.clear_button = QPushButton("Limpiar")
        self.clear_button.clicked.connect(self.clear_search)
        self.clear_button.setMaximumWidth(80)
        
        # Estilo del botón limpiar
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #475569;
                color: #f8fafc;
                border: none;
                padding: 8px 15px;
                border-radius: 6px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #334155;
            }
        """)
        
        layout.addWidget(self.clear_button)
        
        # Agregar stretch al final
        layout.addStretch()
    
    def on_search(self):
        """Maneja el evento de búsqueda."""
        query = self.search_input.text().strip()
        
        if not query:
            logger.warning("Búsqueda vacía")
            return
        
        if len(query) < 2:
            logger.warning("Query muy corto")
            return
        
        logger.info(f"Buscando: {query}")
        self.search_triggered.emit(query)
    
    def clear_search(self):
        """Limpia el campo de búsqueda."""
        self.search_input.clear()
        self.search_input.setFocus()
        logger.info("Búsqueda limpiada")
    
    def set_focus(self):
        """Pone el foco en el campo de búsqueda."""
        self.search_input.setFocus()
    
    def get_query(self) -> str:
        """
        Obtiene el texto actual del campo de búsqueda.
        
        Returns:
            str: Texto de búsqueda
        """
        return self.search_input.text().strip()
