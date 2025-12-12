"""
Visor de Contenido

Este módulo implementa el panel derecho que muestra el contenido
completo de un tema con sus 6 secciones obligatorias.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QLabel, 
    QFrame, QHBoxLayout, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import logging

from ..models.topic import Topic


# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContentViewer(QWidget):
    """
    Visor de contenido de temas.
    
    Muestra las 6 secciones obligatorias de cada tema:
    1. Conceptos Clave
    2. Utilidad Práctica
    3. Relaciones
    4. Aplicaciones en Industria
    5. Roles Laborales
    6. Reto/Proyecto
    
    Attributes:
        scroll_area (QScrollArea): Área scrolleable para el contenido
        content_widget (QWidget): Widget que contiene el contenido
        content_layout (QVBoxLayout): Layout del contenido
        current_topic (Topic): Tema actualmente mostrado
    """
    
    def __init__(self, parent=None):
        """Inicializa el visor de contenido."""
        super().__init__(parent)
        self.current_topic = None
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz del visor."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # === ÁREA SCROLLEABLE ===
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        
        # Widget contenedor del contenido
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(20)
        
        self.scroll_area.setWidget(self.content_widget)
        layout.addWidget(self.scroll_area)
        
        # Mostrar mensaje inicial
        self.show_welcome_message()
    
    def show_welcome_message(self):
        """Muestra un mensaje de bienvenida cuando no hay tema seleccionado."""
        self.clear_content()
        
        welcome_label = QLabel(
            "👋 Bienvenido a Wikia Cognitiva\n\n"
            "Selecciona un tema del panel izquierdo\n"
            "para comenzar a explorar el contenido."
        )
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("""
            QLabel {
                color: #666;
                font-size: 16px;
                padding: 50px;
            }
        """)
        
        self.content_layout.addStretch()
        self.content_layout.addWidget(welcome_label)
        self.content_layout.addStretch()
    
    def display_topic(self, topic: Topic):
        """
        Muestra un tema completo con todas sus secciones.
        
        Args:
            topic: Objeto Topic a mostrar
        """
        try:
            logger.info(f"Mostrando tema: {topic.titulo}")
            
            self.current_topic = topic
            self.clear_content()
            
            # === ENCABEZADO DEL TEMA ===
            self.add_header(topic)
            
            # === METADATA ===
            self.add_metadata(topic)
            
            # === SECCIÓN 1: CONCEPTOS CLAVE ===
            self.add_section_1_conceptos_clave(topic)
            
            # === SECCIÓN 2: UTILIDAD PRÁCTICA ===
            self.add_section_2_utilidad_practica(topic)
            
            # === SECCIÓN 3: RELACIONES ===
            self.add_section_3_relaciones(topic)
            
            # === SECCIÓN 4: APLICACIONES EN INDUSTRIA ===
            self.add_section_4_aplicaciones_industria(topic)
            
            # === SECCIÓN 5: ROLES LABORALES ===
            self.add_section_5_roles_laborales(topic)
            
            # === SECCIÓN 6: RETO/PROYECTO ===
            self.add_section_6_reto_proyecto(topic)
            
            # Agregar espacio al final
            self.content_layout.addStretch()
            
            # Scroll al inicio
            self.scroll_area.verticalScrollBar().setValue(0)
            
            logger.info("✅ Tema mostrado correctamente")
            
        except Exception as e:
            logger.error(f"❌ Error mostrando tema: {e}")
            self.show_error_message(str(e))
    
    def clear_content(self):
        """Limpia todo el contenido actual."""
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def add_header(self, topic: Topic):
        """Agrega el encabezado con título y materia."""
        # Título
        title_label = QLabel(topic.titulo)
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setWordWrap(True)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 5px;")
        self.content_layout.addWidget(title_label)
        
        # Materia
        materia_label = QLabel(f"📚 {topic.materia} • Semestre {topic.semestre}")
        materia_label.setStyleSheet("color: #7f8c8d; font-size: 14px; margin-bottom: 10px;")
        self.content_layout.addWidget(materia_label)
        
        # Línea separadora
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("background-color: #bdc3c7;")
        self.content_layout.addWidget(line)
    
    def add_metadata(self, topic: Topic):
        """Agrega metadata del tema (dificultad, tiempo)."""
        meta_layout = QHBoxLayout()
        
        # Dificultad
        dif_label = QLabel(f"🎯 Dificultad: {topic.dificultad.title()}")
        dif_label.setStyleSheet("color: #34495e; padding: 5px; font-size: 12px;")
        meta_layout.addWidget(dif_label)
        
        # Tiempo estimado
        tiempo_label = QLabel(f"⏱️ Tiempo: {topic.tiempo_estudio}")
        tiempo_label.setStyleSheet("color: #34495e; padding: 5px; font-size: 12px;")
        meta_layout.addWidget(tiempo_label)
        
        meta_layout.addStretch()
        
        self.content_layout.addLayout(meta_layout)
    
    def add_section_1_conceptos_clave(self, topic: Topic):
        """Agrega la sección de Conceptos Clave."""
        section_widget = self.create_section_widget(
            "📘 1. Conceptos Clave",
            "#3498db"
        )
        
        # Contenido
        contenido = topic.get_contenido_conceptos()
        if contenido:
            content_label = QLabel(contenido)
            content_label.setWordWrap(True)
            content_label.setStyleSheet("padding: 10px; line-height: 1.6;")
            section_widget.layout().addWidget(content_label)
        
        # Puntos clave
        puntos = topic.get_puntos_clave()
        if puntos:
            puntos_label = QLabel("<b>Puntos Clave:</b>")
            puntos_label.setStyleSheet("margin-top: 10px; padding: 10px;")
            section_widget.layout().addWidget(puntos_label)
            
            for punto in puntos:
                punto_label = QLabel(f"• {punto}")
                punto_label.setWordWrap(True)
                punto_label.setStyleSheet("padding-left: 20px; padding-right: 10px;")
                section_widget.layout().addWidget(punto_label)
        
        self.content_layout.addWidget(section_widget)
    
    def add_section_2_utilidad_practica(self, topic: Topic):
        """Agrega la sección de Utilidad Práctica."""
        section_widget = self.create_section_widget(
            "🔧 2. Utilidad Práctica",
            "#27ae60"
        )
        
        # Contenido
        contenido = topic.utilidad_practica.get('contenido', '')
        if contenido:
            content_label = QLabel(contenido)
            content_label.setWordWrap(True)
            content_label.setStyleSheet("padding: 10px; line-height: 1.6;")
            section_widget.layout().addWidget(content_label)
        
        # Aplicaciones
        aplicaciones = topic.get_aplicaciones_practica()
        if aplicaciones:
            app_label = QLabel("<b>Aplicaciones Comunes:</b>")
            app_label.setStyleSheet("margin-top: 10px; padding: 10px;")
            section_widget.layout().addWidget(app_label)
            
            for app in aplicaciones:
                app_item = QLabel(f"✓ {app}")
                app_item.setWordWrap(True)
                app_item.setStyleSheet("padding-left: 20px; padding-right: 10px;")
                section_widget.layout().addWidget(app_item)
        
        # Ejemplos vida real
        ejemplos = topic.get_ejemplos_vida_real()
        if ejemplos:
            ej_label = QLabel("<b>Ejemplos en la Vida Real:</b>")
            ej_label.setStyleSheet("margin-top: 10px; padding: 10px;")
            section_widget.layout().addWidget(ej_label)
            
            for ejemplo in ejemplos:
                ej_item = QLabel(f"💡 {ejemplo}")
                ej_item.setWordWrap(True)
                ej_item.setStyleSheet("padding-left: 20px; padding-right: 10px;")
                section_widget.layout().addWidget(ej_item)
        
        self.content_layout.addWidget(section_widget)
    
    def add_section_3_relaciones(self, topic: Topic):
        """Agrega la sección de Relaciones."""
        section_widget = self.create_section_widget(
            "🔗 3. Relaciones con Otros Temas",
            "#9b59b6"
        )
        
        # Prerequisitos
        prereqs = topic.get_prerequisitos()
        if prereqs:
            prereq_label = QLabel("<b>Prerequisitos:</b>")
            prereq_label.setStyleSheet("padding: 10px;")
            section_widget.layout().addWidget(prereq_label)
            
            for prereq in prereqs:
                prereq_item = QLabel(f"← {prereq.get('nombre', 'N/A')}")
                prereq_item.setWordWrap(True)
                prereq_item.setStyleSheet("padding-left: 20px; padding-right: 10px; color: #7f8c8d;")
                if 'razon' in prereq:
                    prereq_item.setToolTip(prereq['razon'])
                section_widget.layout().addWidget(prereq_item)
        
        # Temas siguientes
        siguientes = topic.get_temas_siguientes()
        if siguientes:
            sig_label = QLabel("<b>Temas Siguientes:</b>")
            sig_label.setStyleSheet("margin-top: 10px; padding: 10px;")
            section_widget.layout().addWidget(sig_label)
            
            for siguiente in siguientes:
                sig_item = QLabel(f"→ {siguiente.get('nombre', 'N/A')}")
                sig_item.setWordWrap(True)
                sig_item.setStyleSheet("padding-left: 20px; padding-right: 10px; color: #7f8c8d;")
                section_widget.layout().addWidget(sig_item)
        
        self.content_layout.addWidget(section_widget)
    
    def add_section_4_aplicaciones_industria(self, topic: Topic):
        """Agrega la sección de Aplicaciones en Industria."""
        section_widget = self.create_section_widget(
            "🏭 4. Aplicaciones en la Industria",
            "#e67e22"
        )
        
        # Sectores
        sectores = topic.get_sectores_industria()
        if sectores:
            for sector in sectores:
                sector_name = QLabel(f"<b>{sector.get('nombre', 'N/A')}</b>")
                sector_name.setStyleSheet("padding: 10px; margin-top: 5px;")
                section_widget.layout().addWidget(sector_name)
                
                descripcion = sector.get('descripcion', '')
                if descripcion:
                    desc_label = QLabel(descripcion)
                    desc_label.setWordWrap(True)
                    desc_label.setStyleSheet("padding-left: 20px; padding-right: 10px; color: #555;")
                    section_widget.layout().addWidget(desc_label)
                
                ejemplos = sector.get('ejemplos', [])
                if ejemplos:
                    ej_text = ", ".join(ejemplos)
                    ej_label = QLabel(f"Ejemplos: {ej_text}")
                    ej_label.setWordWrap(True)
                    ej_label.setStyleSheet("padding-left: 20px; padding-right: 10px; font-size: 11px; color: #7f8c8d;")
                    section_widget.layout().addWidget(ej_label)
        
        # Empresas
        empresas = topic.get_empresas()
        if empresas:
            emp_label = QLabel("<b>Empresas que lo usan:</b>")
            emp_label.setStyleSheet("margin-top: 15px; padding: 10px;")
            section_widget.layout().addWidget(emp_label)
            
            empresas_text = ", ".join(empresas)
            empresas_widget = QLabel(empresas_text)
            empresas_widget.setWordWrap(True)
            empresas_widget.setStyleSheet("padding-left: 20px; padding-right: 10px;")
            section_widget.layout().addWidget(empresas_widget)
        
        self.content_layout.addWidget(section_widget)
    
    def add_section_5_roles_laborales(self, topic: Topic):
        """Agrega la sección de Roles Laborales."""
        section_widget = self.create_section_widget(
            "💼 5. Roles Laborales",
            "#e74c3c"
        )
        
        # Roles
        roles = topic.get_roles()
        if roles:
            for rol in roles:
                rol_name = QLabel(f"<b>{rol.get('nombre', 'N/A')}</b>")
                rol_name.setStyleSheet("padding: 10px; margin-top: 5px;")
                section_widget.layout().addWidget(rol_name)
                
                importancia = rol.get('nivel_importancia', '')
                uso = rol.get('uso_especifico', '')
                
                if importancia or uso:
                    info_text = []
                    if importancia:
                        info_text.append(f"Importancia: {importancia}")
                    if uso:
                        info_text.append(f"Uso: {uso}")
                    
                    info_label = QLabel(" | ".join(info_text))
                    info_label.setWordWrap(True)
                    info_label.setStyleSheet("padding-left: 20px; padding-right: 10px; color: #555; font-size: 11px;")
                    section_widget.layout().addWidget(info_label)
        
        # Salario promedio
        salario = topic.get_salario_promedio()
        if salario and salario != "No especificado":
            sal_label = QLabel(f"<b>💰 Rango Salarial en México:</b> {salario}")
            sal_label.setStyleSheet("margin-top: 15px; padding: 10px; background-color: #ecf0f1; border-radius: 5px;")
            section_widget.layout().addWidget(sal_label)
        
        self.content_layout.addWidget(section_widget)
    
    def add_section_6_reto_proyecto(self, topic: Topic):
        """Agrega la sección de Reto/Proyecto."""
        tipo = topic.tipo_reto
        
        if tipo == 'programacion':
            icono = "💻"
            color = "#16a085"
            tipo_texto = "Reto de Programación"
        else:
            icono = "📋"
            color = "#8e44ad"
            tipo_texto = "Proyecto Conceptual"
        
        section_widget = self.create_section_widget(
            f"{icono} 6. {tipo_texto}",
            color
        )
        
        # Título del reto
        titulo_reto = topic.titulo_reto
        if titulo_reto:
            titulo_label = QLabel(f"<b>{titulo_reto}</b>")
            titulo_label.setStyleSheet("font-size: 14px; padding: 10px;")
            section_widget.layout().addWidget(titulo_label)
        
        # Descripción
        descripcion = topic.descripcion_reto
        if descripcion:
            desc_label = QLabel(descripcion)
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("padding: 10px; line-height: 1.6;")
            section_widget.layout().addWidget(desc_label)
        
        if tipo == 'programacion':
            self.add_challenge_info(section_widget, topic)
        else:
            self.add_project_info(section_widget, topic)
        
        self.content_layout.addWidget(section_widget)
    
    def add_challenge_info(self, parent_widget: QWidget, topic: Topic):
        """Agrega información específica de un reto de programación."""
        # Código inicial (preview)
        codigo = topic.get_codigo_inicial()
        if codigo:
            code_label = QLabel("<b>Código Inicial:</b>")
            code_label.setStyleSheet("margin-top: 10px; padding: 10px;")
            parent_widget.layout().addWidget(code_label)
            
            # Mostrar primeras líneas
            lineas = codigo.split('\n')[:8]
            preview = '\n'.join(lineas)
            if len(codigo.split('\n')) > 8:
                preview += '\n...'
            
            code_preview = QLabel(f"<pre style='background: #2c3e50; color: #ecf0f1; padding: 10px; border-radius: 5px;'>{preview}</pre>")
            parent_widget.layout().addWidget(code_preview)
        
        # Pistas disponibles
        pistas = topic.get_pistas()
        if pistas:
            pistas_label = QLabel(f"<b>💡 {len(pistas)} Pistas Disponibles</b>")
            pistas_label.setStyleSheet("margin-top: 10px; padding: 10px;")
            parent_widget.layout().addWidget(pistas_label)
        
        # Nota sobre el editor
        nota = QLabel("ℹ️ El editor de código interactivo estará disponible próximamente")
        nota.setStyleSheet("margin-top: 10px; padding: 10px; color: #7f8c8d; font-style: italic;")
        parent_widget.layout().addWidget(nota)
    
    def add_project_info(self, parent_widget: QWidget, topic: Topic):
        """Agrega información específica de un proyecto conceptual."""
        # Objetivos
        objetivos = topic.get_objetivos_proyecto()
        if objetivos:
            obj_label = QLabel("<b>🎯 Objetivos:</b>")
            obj_label.setStyleSheet("margin-top: 10px; padding: 10px;")
            parent_widget.layout().addWidget(obj_label)
            
            for objetivo in objetivos:
                obj_item = QLabel(f"• {objetivo}")
                obj_item.setWordWrap(True)
                obj_item.setStyleSheet("padding-left: 20px; padding-right: 10px;")
                parent_widget.layout().addWidget(obj_item)
        
        # Pasos sugeridos
        pasos = topic.get_pasos_proyecto()
        if pasos:
            pasos_label = QLabel("<b>📝 Pasos Sugeridos:</b>")
            pasos_label.setStyleSheet("margin-top: 10px; padding: 10px;")
            parent_widget.layout().addWidget(pasos_label)
            
            for i, paso in enumerate(pasos, 1):
                paso_item = QLabel(f"{i}. {paso}")
                paso_item.setWordWrap(True)
                paso_item.setStyleSheet("padding-left: 20px; padding-right: 10px;")
                parent_widget.layout().addWidget(paso_item)
    
    def create_section_widget(self, title: str, color: str) -> QWidget:
        """
        Crea un widget de sección con título y estilo.
        
        Args:
            title: Título de la sección
            color: Color del borde izquierdo
        
        Returns:
            QWidget configurado como sección
        """
        section = QFrame()
        section.setFrameShape(QFrame.Shape.StyledPanel)
        section.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-left: 4px solid {color};
                border-radius: 5px;
                padding: 10px;
            }}
        """)
        
        section_layout = QVBoxLayout(section)
        section_layout.setContentsMargins(15, 15, 15, 15)
        section_layout.setSpacing(10)
        
        # Título de la sección
        title_label = QLabel(title)
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet(f"color: {color}; margin-bottom: 10px;")
        section_layout.addWidget(title_label)
        
        return section
    
    def show_error_message(self, error: str):
        """Muestra un mensaje de error."""
        self.clear_content()
        
        error_label = QLabel(f"❌ Error al cargar el tema:\n\n{error}")
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_label.setStyleSheet("color: #e74c3c; padding: 20px;")
        error_label.setWordWrap(True)
        
        self.content_layout.addStretch()
        self.content_layout.addWidget(error_label)
        self.content_layout.addStretch()
