"""
Modelo de datos para Proyectos Conceptuales

Este módulo define la clase Project que representa un proyecto
conceptual sin código, enfocado en análisis y reflexión.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class Project:
    """
    Representa un proyecto conceptual (sin código).
    
    Un proyecto conceptual incluye:
    - Descripción del proyecto
    - Objetivos de aprendizaje
    - Pasos sugeridos para completarlo
    - Recursos adicionales
    - Campo opcional para respuestas del estudiante
    
    Attributes:
        tipo (str): Debe ser "conceptual"
        titulo (str): Título del proyecto
        descripcion (str): Descripción detallada
        objetivos (List[str]): Objetivos de aprendizaje
        pasos_sugeridos (List[str]): Pasos para completar el proyecto
        tiempo_estimado (str): Tiempo estimado de realización
        recursos_adicionales (List[Dict]): Links y materiales de apoyo
        campo_respuesta (bool): Si permite al usuario escribir respuestas
    
    Example:
        >>> project = Project(proyecto_data)
        >>> print(project.titulo)
        Análisis de Gradiente Descendente
        >>> for objetivo in project.objetivos:
        ...     print(f"- {objetivo}")
    """
    
    tipo: str
    titulo: str
    descripcion: str
    objetivos: List[str] = field(default_factory=list)
    pasos_sugeridos: List[str] = field(default_factory=list)
    tiempo_estimado: str = "No especificado"
    recursos_adicionales: List[Dict[str, str]] = field(default_factory=list)
    campo_respuesta: bool = False
    _raw_data: Dict[str, Any] = field(default_factory=dict, repr=False)
    
    def __init__(self, data: Dict[str, Any]):
        """
        Inicializa un Project desde un diccionario.
        
        Args:
            data (Dict): Diccionario con la información del proyecto
        
        Raises:
            ValueError: Si el tipo no es 'conceptual' o faltan campos obligatorios
        """
        # Validar tipo
        if data.get('tipo') != 'conceptual':
            raise ValueError(f"Project requiere tipo='conceptual', recibido: {data.get('tipo')}")
        
        # Validar campos obligatorios
        required_fields = ['tipo', 'titulo', 'descripcion']
        for field_name in required_fields:
            if field_name not in data:
                raise ValueError(f"Project requiere campo '{field_name}'")
        
        # Asignar campos
        self.tipo = data['tipo']
        self.titulo = data['titulo']
        self.descripcion = data['descripcion']
        self.objetivos = data.get('objetivos', [])
        self.pasos_sugeridos = data.get('pasos_sugeridos', [])
        self.tiempo_estimado = data.get('tiempo_estimado', 'No especificado')
        self.recursos_adicionales = data.get('recursos_adicionales', [])
        self.campo_respuesta = data.get('campo_respuesta', False)
        self._raw_data = data
        
        # Advertencias si faltan campos importantes
        if not self.objetivos:
            print(f"⚠️  Warning: Project '{self.titulo}' sin objetivos definidos")
        
        if not self.pasos_sugeridos:
            print(f"⚠️  Warning: Project '{self.titulo}' sin pasos sugeridos")
    
    def __repr__(self) -> str:
        """Representación legible del proyecto"""
        return f"Project('{self.titulo}', {len(self.objetivos)} objetivos)"
    
    def __str__(self) -> str:
        """Conversión a string para print()"""
        return f"📋 {self.titulo}"
    
    # ==================== PROPIEDADES ====================
    
    @property
    def tiene_objetivos(self) -> bool:
        """True si tiene objetivos definidos"""
        return len(self.objetivos) > 0
    
    @property
    def numero_objetivos(self) -> int:
        """Número de objetivos del proyecto"""
        return len(self.objetivos)
    
    @property
    def tiene_pasos(self) -> bool:
        """True si tiene pasos sugeridos"""
        return len(self.pasos_sugeridos) > 0
    
    @property
    def numero_pasos(self) -> int:
        """Número de pasos sugeridos"""
        return len(self.pasos_sugeridos)
    
    @property
    def tiene_recursos(self) -> bool:
        """True si tiene recursos adicionales"""
        return len(self.recursos_adicionales) > 0
    
    @property
    def numero_recursos(self) -> int:
        """Número de recursos adicionales"""
        return len(self.recursos_adicionales)
    
    @property
    def permite_respuesta(self) -> bool:
        """True si permite al usuario escribir respuestas"""
        return self.campo_respuesta
    
    # ==================== MÉTODOS DE ACCESO ====================
    
    def get_objetivo(self, indice: int) -> Optional[str]:
        """
        Obtiene un objetivo específico por índice.
        
        Args:
            indice (int): Índice del objetivo (0-based)
        
        Returns:
            str o None si el índice no existe
        """
        if 0 <= indice < len(self.objetivos):
            return self.objetivos[indice]
        return None
    
    def get_todos_objetivos(self) -> List[str]:
        """
        Obtiene todos los objetivos.
        
        Returns:
            List[str]: Lista completa de objetivos
        """
        return self.objetivos.copy()
    
    def get_paso(self, indice: int) -> Optional[str]:
        """
        Obtiene un paso específico por índice.
        
        Args:
            indice (int): Índice del paso (0-based)
        
        Returns:
            str o None si el índice no existe
        """
        if 0 <= indice < len(self.pasos_sugeridos):
            return self.pasos_sugeridos[indice]
        return None
    
    def get_todos_pasos(self) -> List[str]:
        """
        Obtiene todos los pasos sugeridos.
        
        Returns:
            List[str]: Lista completa de pasos
        """
        return self.pasos_sugeridos.copy()
    
    def get_recursos(self, tipo: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Obtiene recursos adicionales, opcionalmente filtrados por tipo.
        
        Args:
            tipo (str, optional): Tipo de recurso ('video', 'articulo', 'libro', etc.)
        
        Returns:
            List[Dict]: Lista de recursos
        
        Example:
            >>> videos = project.get_recursos('video')
            >>> for video in videos:
            ...     print(video['titulo'], video['url'])
        """
        if tipo:
            return [r for r in self.recursos_adicionales if r.get('tipo') == tipo]
        return self.recursos_adicionales.copy()
    
    def get_videos(self) -> List[Dict[str, str]]:
        """
        Obtiene solo los recursos de tipo video.
        
        Returns:
            List[Dict]: Lista de videos
        """
        return self.get_recursos('video')
    
    def get_articulos(self) -> List[Dict[str, str]]:
        """
        Obtiene solo los recursos de tipo artículo.
        
        Returns:
            List[Dict]: Lista de artículos
        """
        return self.get_recursos('articulo')
    
    def get_libros(self) -> List[Dict[str, str]]:
        """
        Obtiene solo los recursos de tipo libro.
        
        Returns:
            List[Dict]: Lista de libros
        """
        return self.get_recursos('libro')
    
    # ==================== MÉTODOS DE ANÁLISIS ====================
    
    def estimar_complejidad(self) -> str:
        """
        Estima la complejidad del proyecto basándose en objetivos y pasos.
        
        Returns:
            str: 'simple', 'moderado' o 'complejo'
        """
        total_items = self.numero_objetivos + self.numero_pasos
        
        if total_items <= 5:
            return 'simple'
        elif total_items <= 10:
            return 'moderado'
        else:
            return 'complejo'
    
    def calcular_completitud(self) -> float:
        """
        Calcula qué tan completo está el proyecto (0.0 a 1.0).
        
        Considera:
        - Si tiene objetivos
        - Si tiene pasos
        - Si tiene recursos
        - Si tiene tiempo estimado
        
        Returns:
            float: Porcentaje de completitud (0.0 a 1.0)
        """
        puntos = 0
        total = 4
        
        if self.tiene_objetivos:
            puntos += 1
        if self.tiene_pasos:
            puntos += 1
        if self.tiene_recursos:
            puntos += 1
        if self.tiempo_estimado != "No especificado":
            puntos += 1
        
        return puntos / total
    
    # ==================== MÉTODOS DE UTILIDAD ====================
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el proyecto a diccionario.
        
        Returns:
            Dict: Representación en diccionario
        """
        if self._raw_data:
            return self._raw_data
        
        return {
            'tipo': self.tipo,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'objetivos': self.objetivos,
            'pasos_sugeridos': self.pasos_sugeridos,
            'tiempo_estimado': self.tiempo_estimado,
            'recursos_adicionales': self.recursos_adicionales,
            'campo_respuesta': self.campo_respuesta
        }
    
    def info_resumen(self) -> str:
        """
        Retorna un resumen formateado del proyecto.
        
        Returns:
            str: Resumen del proyecto
        """
        complejidad = self.estimar_complejidad()
        completitud = self.calcular_completitud() * 100
        
        lineas = [
            f"\n{'='*70}",
            f"📋 PROYECTO CONCEPTUAL: {self.titulo}",
            f"{'='*70}",
            f"Tiempo estimado: {self.tiempo_estimado}",
            f"Complejidad: {complejidad}",
            f"Completitud: {completitud:.0f}%",
            f"\nDescripción:",
            f"  {self.descripcion}",
            f"\nEstadísticas:",
            f"  - Objetivos: {self.numero_objetivos}",
            f"  - Pasos sugeridos: {self.numero_pasos}",
            f"  - Recursos adicionales: {self.numero_recursos}",
            f"  - Permite respuesta del usuario: {'Sí' if self.permite_respuesta else 'No'}",
        ]
        
        if self.tiene_objetivos:
            lineas.append(f"\n🎯 Objetivos:")
            for i, objetivo in enumerate(self.objetivos[:3], 1):
                lineas.append(f"  {i}. {objetivo}")
            if len(self.objetivos) > 3:
                lineas.append(f"  ... y {len(self.objetivos) - 3} más")
        
        if self.tiene_pasos:
            lineas.append(f"\n📝 Primeros pasos:")
            for i, paso in enumerate(self.pasos_sugeridos[:3], 1):
                lineas.append(f"  {i}. {paso}")
            if len(self.pasos_sugeridos) > 3:
                lineas.append(f"  ... y {len(self.pasos_sugeridos) - 3} más")
        
        if self.tiene_recursos:
            lineas.append(f"\n📚 Recursos disponibles:")
            tipos_recursos = {}
            for recurso in self.recursos_adicionales:
                tipo = recurso.get('tipo', 'otro')
                tipos_recursos[tipo] = tipos_recursos.get(tipo, 0) + 1
            
            for tipo, cantidad in tipos_recursos.items():
                lineas.append(f"  - {cantidad} {tipo}(s)")
        
        return "\n".join(lineas)
    
    def es_valido(self) -> tuple[bool, List[str]]:
        """
        Verifica si el proyecto tiene toda la información necesaria.
        
        Returns:
            tuple: (es_valido, lista_de_problemas)
        """
        problemas = []
        
        if not self.tiene_objetivos:
            problemas.append("No hay objetivos definidos")
        
        if not self.tiene_pasos:
            problemas.append("No hay pasos sugeridos")
        
        if self.tiempo_estimado == "No especificado":
            problemas.append("Tiempo estimado no especificado")
        
        # Advertencia suave para recursos (no crítico)
        if not self.tiene_recursos:
            problemas.append("⚠️  No hay recursos adicionales (recomendado)")
        
        # Filtrar advertencias de problemas críticos
        problemas_criticos = [p for p in problemas if not p.startswith('⚠️')]
        
        return len(problemas_criticos) == 0, problemas
    
    def generar_checklist(self) -> str:
        """
        Genera un checklist formateado para el estudiante.
        
        Returns:
            str: Checklist en formato markdown
        """
        lineas = [
            f"# {self.titulo}\n",
            f"**Tiempo estimado:** {self.tiempo_estimado}\n",
            f"## Descripción\n",
            f"{self.descripcion}\n",
        ]
        
        if self.tiene_objetivos:
            lineas.append("## Objetivos de Aprendizaje\n")
            for objetivo in self.objetivos:
                lineas.append(f"- [ ] {objetivo}")
            lineas.append("")
        
        if self.tiene_pasos:
            lineas.append("## Pasos a Seguir\n")
            for i, paso in enumerate(self.pasos_sugeridos, 1):
                lineas.append(f"{i}. [ ] {paso}")
            lineas.append("")
        
        if self.tiene_recursos:
            lineas.append("## Recursos Adicionales\n")
            for recurso in self.recursos_adicionales:
                tipo = recurso.get('tipo', 'recurso')
                titulo = recurso.get('titulo', 'Sin título')
                url = recurso.get('url', '#')
                lineas.append(f"- [{tipo.upper()}] [{titulo}]({url})")
        
        return "\n".join(lineas)