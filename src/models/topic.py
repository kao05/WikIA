"""
Modelo de datos para un Tema completo

Este módulo define la clase Topic que representa un tema completo
con todas sus 6 secciones obligatorias.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field


@dataclass
class Topic:
    """
    Representa un tema completo con las 6 secciones obligatorias.
    
    Las 6 secciones son:
    1. Conceptos Clave - ¿Qué es esto?
    2. Utilidad Práctica - ¿Para qué sirve?
    3. Relaciones - Conceptos relacionados
    4. Aplicaciones en Industria - ¿Dónde se usa?
    5. Roles Laborales - ¿Qué puestos lo necesitan?
    6. Reto/Proyecto - Desafío práctico
    
    Attributes:
        metadata (Dict): Información general del tema (id, título, materia, semestre)
        conceptos_clave (Dict): Sección 1 - Explicación del concepto
        utilidad_practica (Dict): Sección 2 - Para qué sirve
        relaciones (Dict): Sección 3 - Temas relacionados
        aplicaciones_industria (Dict): Sección 4 - Uso en el mundo real
        roles_laborales (Dict): Sección 5 - Puestos de trabajo
        reto_proyecto (Dict): Sección 6 - Reto o proyecto
        _raw_data (Dict): Datos JSON originales (opcional)
    """
    
    metadata: Dict[str, Any]
    conceptos_clave: Dict[str, Any]
    utilidad_practica: Dict[str, Any]
    relaciones: Dict[str, Any]
    aplicaciones_industria: Dict[str, Any]
    roles_laborales: Dict[str, Any]
    reto_proyecto: Dict[str, Any]
    _raw_data: Dict[str, Any] = field(default_factory=dict, repr=False)
    
    def __init__(self, data: Dict[str, Any]):
        """
        Inicializa un Topic desde un diccionario (típicamente de JSON).
        
        Args:
            data (Dict): Diccionario con todas las secciones del tema
        
        Raises:
            KeyError: Si falta alguna sección obligatoria
            ValueError: Si los datos no son válidos
        """
        # Validar que existan todas las secciones obligatorias
        required_sections = [
            'metadata',
            '1_conceptos_clave',
            '2_utilidad_practica',
            '3_relaciones',
            '4_aplicaciones_industria',
            '5_roles_laborales',
            '6_reto_proyecto'
        ]
        
        for section in required_sections:
            if section not in data:
                raise KeyError(f"Falta sección obligatoria: {section}")
        
        # Asignar secciones
        self.metadata = data.get('metadata', {})
        self.conceptos_clave = data.get('1_conceptos_clave', {})
        self.utilidad_practica = data.get('2_utilidad_practica', {})
        self.relaciones = data.get('3_relaciones', {})
        self.aplicaciones_industria = data.get('4_aplicaciones_industria', {})
        self.roles_laborales = data.get('5_roles_laborales', {})
        self.reto_proyecto = data.get('6_reto_proyecto', {})
        
        # Guardar datos originales
        self._raw_data = data
        
        # Validar metadata básica
        if not self.metadata:
            raise ValueError("metadata no puede estar vacío")
        
        if 'titulo' not in self.metadata:
            raise ValueError("metadata debe contener 'titulo'")
    
    def __repr__(self) -> str:
        """Representación legible del tema"""
        return f"Topic('{self.titulo}', materia='{self.materia}', tipo_reto='{self.tipo_reto}')"
    
    def __str__(self) -> str:
        """Conversión a string para print()"""
        return f"{self.titulo} ({self.materia})"
# ==================== PROPIEDADES DE METADATA ====================
    
    @property
    def id(self) -> str:
        """ID único del tema"""
        return self.metadata.get('id', '')
    
    @property
    def titulo(self) -> str:
        """Título del tema"""
        return self.metadata.get('titulo', 'Sin título')
    
    @property
    def materia(self) -> str:
        """Nombre de la materia a la que pertenece"""
        return self.metadata.get('materia', '')
    
    @property
    def semestre(self) -> int:
        """Número de semestre (1-4)"""
        return self.metadata.get('semestre', 0)
    
    @property
    def dificultad(self) -> str:
        """Nivel de dificultad del tema"""
        return self.metadata.get('dificultad', 'no especificada')
    
    @property
    def tiempo_estudio(self) -> str:
        """Tiempo estimado de estudio"""
        return self.metadata.get('tiempo_estudio', 'no especificado')
    
    # ==================== PROPIEDADES DE RETO/PROYECTO ====================
    
    @property
    def tipo_reto(self) -> str:
        """
        Tipo de reto: 'programacion' o 'conceptual'
        
        Returns:
            str: Tipo del reto
        """
        return self.reto_proyecto.get('tipo', 'conceptual')
    
    @property
    def es_reto_programacion(self) -> bool:
        """True si el reto es de programación"""
        return self.tipo_reto == 'programacion'
    
    @property
    def es_proyecto_conceptual(self) -> bool:
        """True si es un proyecto conceptual"""
        return self.tipo_reto == 'conceptual'
    
    @property
    def titulo_reto(self) -> str:
        """Título del reto o proyecto"""
        return self.reto_proyecto.get('titulo', '')
    
    @property
    def descripcion_reto(self) -> str:
        """Descripción del reto o proyecto"""
        return self.reto_proyecto.get('descripcion', '')
# ==================== MÉTODOS DE ACCESO A CONTENIDO ====================
    
    def get_contenido_conceptos(self) -> str:
        """Obtiene el contenido de la sección Conceptos Clave"""
        return self.conceptos_clave.get('contenido', '')
    
    def get_puntos_clave(self) -> List[str]:
        """Obtiene los puntos clave del tema"""
        return self.conceptos_clave.get('puntos_clave', [])
    
    def get_aplicaciones_practica(self) -> List[str]:
        """Obtiene las aplicaciones prácticas del tema"""
        return self.utilidad_practica.get('aplicaciones', [])
    
    def get_ejemplos_vida_real(self) -> List[str]:
        """Obtiene ejemplos de uso en la vida real"""
        return self.utilidad_practica.get('ejemplos_vida_real', [])
    
    def get_prerequisitos(self) -> List[Dict[str, str]]:
        """Obtiene los temas prerequisitos"""
        return self.relaciones.get('prerequisitos', [])
    
    def get_temas_siguientes(self) -> List[Dict[str, str]]:
        """Obtiene los temas que siguen después de este"""
        return self.relaciones.get('temas_siguientes', [])
    
    def get_sectores_industria(self) -> List[Dict[str, Any]]:
        """Obtiene los sectores de industria donde se aplica"""
        return self.aplicaciones_industria.get('sectores', [])
    
    def get_empresas(self) -> List[str]:
        """Obtiene las empresas que usan este conocimiento"""
        return self.aplicaciones_industria.get('empresas_que_lo_usan', [])
    
    def get_roles(self) -> List[Dict[str, str]]:
        """Obtiene los roles laborales donde este conocimiento es importante"""
        return self.roles_laborales.get('roles', [])
    
    def get_salario_promedio(self) -> str:
        """Obtiene el rango salarial promedio"""
        return self.roles_laborales.get('salario_promedio_mx', 'No especificado')
# ==================== MÉTODOS ESPECÍFICOS PARA RETOS ====================
    
    def get_codigo_inicial(self) -> str:
        """Obtiene el código inicial para retos de programación"""
        if self.es_reto_programacion:
            return self.reto_proyecto.get('codigo_inicial', '')
        return ''
    
    def get_solucion_referencia(self) -> str:
        """Obtiene la solución de referencia para retos de programación"""
        if self.es_reto_programacion:
            return self.reto_proyecto.get('solucion_referencia', '')
        return ''
    
    def get_pistas(self) -> List[str]:
        """Obtiene las pistas para resolver el reto"""
        return self.reto_proyecto.get('pistas', [])
    
    def get_casos_prueba(self) -> List[Dict[str, Any]]:
        """Obtiene los casos de prueba visibles para retos de programación"""
        if self.es_reto_programacion:
            return self.reto_proyecto.get('casos_prueba_visibles', [])
        return []
    
    # ==================== MÉTODOS ESPECÍFICOS PARA PROYECTOS ====================
    
    def get_objetivos_proyecto(self) -> List[str]:
        """Obtiene los objetivos del proyecto conceptual"""
        if self.es_proyecto_conceptual:
            return self.reto_proyecto.get('objetivos', [])
        return []
    
    def get_pasos_proyecto(self) -> List[str]:
        """Obtiene los pasos sugeridos para el proyecto"""
        if self.es_proyecto_conceptual:
            return self.reto_proyecto.get('pasos_sugeridos', [])
        return []
    
    def get_recursos_adicionales(self) -> List[Dict[str, str]]:
        """Obtiene recursos adicionales (videos, artículos, etc.)"""
        return self.reto_proyecto.get('recursos_adicionales', [])
    
    # ==================== MÉTODOS DE UTILIDAD ====================
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el tema a diccionario"""
        if self._raw_data:
            return self._raw_data
        
        return {
            'metadata': self.metadata,
            '1_conceptos_clave': self.conceptos_clave,
            '2_utilidad_practica': self.utilidad_practica,
            '3_relaciones': self.relaciones,
            '4_aplicaciones_industria': self.aplicaciones_industria,
            '5_roles_laborales': self.roles_laborales,
            '6_reto_proyecto': self.reto_proyecto
        }
    
    def info_resumen(self) -> str:
        """Retorna un resumen formateado del tema"""
        lineas = [
            f"\n{'='*70}",
            f"TEMA: {self.titulo}",
            f"{'='*70}",
            f"Materia: {self.materia}",
            f"Semestre: {self.semestre}",
            f"Dificultad: {self.dificultad}",
            f"Tiempo de estudio: {self.tiempo_estudio}",
            f"\n📘 Conceptos Clave:",
            f"  {self.get_contenido_conceptos()[:100]}...",
            f"\n Tipo de Reto: {self.tipo_reto}",
            f"  {self.titulo_reto}",
        ]
        
        return "\n".join(lineas)
    
    def tiene_contenido_completo(self) -> bool:
        """Verifica si el tema tiene contenido en todas las secciones"""
        checks = [
            bool(self.metadata),
            bool(self.conceptos_clave),
            bool(self.utilidad_practica),
            bool(self.relaciones),
            bool(self.aplicaciones_industria),
            bool(self.roles_laborales),
            bool(self.reto_proyecto)
        ]
        return all(checks)
