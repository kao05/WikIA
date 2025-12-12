"""
Modelo para representar retos de programación en Wikia Cognitiva.
Maneja desafíos de código con casos de prueba, pistas y soluciones.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class TestCase:
    """Representa un caso de prueba para validar el código del estudiante."""
    entrada: Dict[str, Any]
    salida_esperada: Any
    explicacion: str
    es_visible: bool = True  # Algunos casos pueden estar ocultos
    
    def __repr__(self) -> str:
        return f"TestCase(entrada={self.entrada}, esperado={self.salida_esperada})"


@dataclass
class Challenge:
    """
    Modelo principal para retos de programación.
    
    Attributes:
        tipo: Tipo de reto (siempre 'programacion' para esta clase)
        titulo: Título descriptivo del reto
        descripcion: Descripción detallada del problema a resolver
        dificultad: Nivel de dificultad ('basico', 'intermedio', 'avanzado')
        codigo_inicial: Código plantilla con el que el estudiante inicia
        solucion: Código de solución de referencia (no visible por defecto)
        pistas: Lista de pistas graduales para ayudar al estudiante
        casos_prueba: Casos de prueba para validar la solución
        recursos_adicionales: Enlaces, videos o material de apoyo
        lenguaje: Lenguaje de programación ('python', 'javascript', etc.)
        tiempo_estimado: Tiempo estimado de resolución
    """
    
    tipo: str = "programacion"
    titulo: str = ""
    descripcion: str = ""
    dificultad: str = "intermedio"
    codigo_inicial: str = ""
    solucion: str = ""
    pistas: List[str] = field(default_factory=list)
    casos_prueba_visibles: List[TestCase] = field(default_factory=list)
    casos_prueba_ocultos: List[TestCase] = field(default_factory=list)
    recursos_adicionales: List[Dict[str, str]] = field(default_factory=list)
    lenguaje: str = "python"
    tiempo_estimado: str = "30-45 minutos"
    
    def __init__(self, data: Dict[str, Any]):
        """
        Inicializa un Challenge desde un diccionario JSON.
        
        Args:
            data: Diccionario con los datos del reto desde el JSON
        """
        self.tipo = data.get('tipo', 'programacion')
        self.titulo = data.get('titulo', 'Reto sin título')
        self.descripcion = data.get('descripcion', '')
        self.dificultad = data.get('dificultad', 'intermedio')
        self.codigo_inicial = data.get('codigo_inicial', '')
        self.solucion = data.get('solucion_referencia', '')
        self.pistas = data.get('pistas', [])
        self.recursos_adicionales = data.get('recursos_adicionales', [])
        self.lenguaje = data.get('lenguaje', 'python')
        self.tiempo_estimado = data.get('tiempo_estimado', '30-45 minutos')
        
        # Parsear casos de prueba visibles
        self.casos_prueba_visibles = []
        for caso in data.get('casos_prueba_visibles', []):
            test_case = TestCase(
                entrada=caso.get('entrada', {}),
                salida_esperada=caso.get('salida_esperada'),
                explicacion=caso.get('explicacion', ''),
                es_visible=True
            )
            self.casos_prueba_visibles.append(test_case)
        
        # Parsear casos de prueba ocultos (si existen)
        self.casos_prueba_ocultos = []
        for caso in data.get('casos_prueba_ocultos', []):
            test_case = TestCase(
                entrada=caso.get('entrada', {}),
                salida_esperada=caso.get('salida_esperada'),
                explicacion=caso.get('explicacion', ''),
                es_visible=False
            )
            self.casos_prueba_ocultos.append(test_case)
    
    @property
    def total_casos_prueba(self) -> int:
        """Retorna el número total de casos de prueba."""
        return len(self.casos_prueba_visibles) + len(self.casos_prueba_ocultos)
    
    @property
    def tiene_solucion(self) -> bool:
        """Verifica si el reto tiene una solución de referencia."""
        return bool(self.solucion and self.solucion.strip())
    
    @property
    def tiene_pistas(self) -> bool:
        """Verifica si el reto tiene pistas disponibles."""
        return len(self.pistas) > 0
    
    def get_pista(self, nivel: int) -> Optional[str]:
        """
        Obtiene una pista específica por nivel.
        
        Args:
            nivel: Nivel de la pista (0-indexed)
            
        Returns:
            La pista solicitada o None si el nivel no existe
        """
        if 0 <= nivel < len(self.pistas):
            return self.pistas[nivel]
        return None
    
    def get_casos_visibles(self) -> List[TestCase]:
        """Retorna solo los casos de prueba visibles al estudiante."""
        return self.casos_prueba_visibles
    
    def get_todos_los_casos(self) -> List[TestCase]:
        """Retorna todos los casos de prueba (visibles + ocultos)."""
        return self.casos_prueba_visibles + self.casos_prueba_ocultos
    
    def validar_codigo(self, codigo_estudiante: str) -> Dict[str, Any]:
        """
        Valida el código del estudiante contra todos los casos de prueba.
        
        Args:
            codigo_estudiante: Código Python a validar
            
        Returns:
            Diccionario con resultados de la validación
        """
        resultados = {
            'exito': False,
            'casos_pasados': 0,
            'casos_totales': self.total_casos_prueba,
            'detalles': [],
            'errores': []
        }
        
        try:
            # Crear un namespace limpio para ejecutar el código
            namespace = {}
            exec(codigo_estudiante, namespace)
            
            # Validar contra todos los casos
            for i, caso in enumerate(self.get_todos_los_casos()):
                try:
                    # Buscar la función principal (asumimos que es la primera función definida)
                    funciones = [v for v in namespace.values() if callable(v)]
                    if not funciones:
                        resultados['errores'].append("No se encontró ninguna función en el código")
                        break
                    
                    funcion_principal = funciones[0]
                    
                    # Ejecutar con los parámetros del caso de prueba
                    resultado = funcion_principal(**caso.entrada)
                    
                    # Comparar resultado
                    paso = resultado == caso.salida_esperada
                    
                    if paso:
                        resultados['casos_pasados'] += 1
                    
                    resultados['detalles'].append({
                        'caso': i + 1,
                        'paso': paso,
                        'entrada': caso.entrada,
                        'esperado': caso.salida_esperada,
                        'obtenido': resultado,
                        'visible': caso.es_visible,
                        'explicacion': caso.explicacion
                    })
                    
                except Exception as e:
                    resultados['detalles'].append({
                        'caso': i + 1,
                        'paso': False,
                        'error': str(e),
                        'visible': caso.es_visible
                    })
            
            # Determinar si pasó todos los casos
            resultados['exito'] = resultados['casos_pasados'] == resultados['casos_totales']
            
        except Exception as e:
            resultados['errores'].append(f"Error al ejecutar el código: {str(e)}")
        
        return resultados
    
    def get_dificultad_emoji(self) -> str:
        """Retorna un emoji representativo de la dificultad."""
        emojis = {
            'basico': '🟢',
            'intermedio': '🟡',
            'avanzado': '🔴',
            'experto': '🔥'
        }
        return emojis.get(self.dificultad.lower(), '⚪')
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte el Challenge a un diccionario para serialización."""
        return {
            'tipo': self.tipo,
            'titulo': self.titulo,
            'descripcion': self.descripcion,
            'dificultad': self.dificultad,
            'codigo_inicial': self.codigo_inicial,
            'solucion': self.solucion,
            'pistas': self.pistas,
            'casos_prueba_visibles': [
                {
                    'entrada': caso.entrada,
                    'salida_esperada': caso.salida_esperada,
                    'explicacion': caso.explicacion
                }
                for caso in self.casos_prueba_visibles
            ],
            'recursos_adicionales': self.recursos_adicionales,
            'lenguaje': self.lenguaje,
            'tiempo_estimado': self.tiempo_estimado
        }
    
    def __repr__(self) -> str:
        return (f"Challenge(titulo='{self.titulo}', "
                f"dificultad='{self.dificultad}', "
                f"casos={self.total_casos_prueba})")
    
    def __str__(self) -> str:
        return (f"{self.get_dificultad_emoji()} {self.titulo}\n"
                f"Dificultad: {self.dificultad}\n"
                f"Casos de prueba: {self.total_casos_prueba}\n"
                f"Pistas disponibles: {len(self.pistas)}")