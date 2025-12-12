"""
Modelo de datos para una Materia

Este módulo define la clase Subject que representa una materia
completa con todos sus temas.
"""

from typing import List, Optional, Dict
from dataclasses import dataclass, field


@dataclass
class Subject:
    """
    Representa una materia académica.
    
    Attributes:
        id (str): Identificador único de la materia (ej: "algebra_superior")
        nombre (str): Nombre completo de la materia
        creditos (int): Número de créditos de la materia
        temas (List[Dict]): Lista de diccionarios con información básica de temas
                           Cada tema tiene: id, nombre, archivo
    
    Example:
        >>> materia = Subject(
        ...     id="algebra_superior",
        ...     nombre="Álgebra Superior",
        ...     creditos=8,
        ...     temas=[
        ...         {"id": "teoria_conjuntos", "nombre": "Teoría de Conjuntos", "archivo": "teoria_conjuntos.json"}
        ...     ]
        ... )
        >>> print(materia)
        Álgebra Superior (8 créditos, 10 temas)
    """
    
    id: str
    nombre: str
    creditos: int
    temas: List[Dict[str, str]] = field(default_factory=list)
    
    def __post_init__(self):
        """Validación después de la inicialización"""
        if not self.id:
            raise ValueError("El ID de la materia no puede estar vacío")
        
        if not self.nombre:
            raise ValueError("El nombre de la materia no puede estar vacío")
        
        if self.creditos < 0:
            raise ValueError(f"Los créditos no pueden ser negativos: {self.creditos}")
        
        if not isinstance(self.temas, list):
            raise TypeError("temas debe ser una lista")
        
        # Validar estructura de cada tema
        for i, tema in enumerate(self.temas):
            if not isinstance(tema, dict):
                raise TypeError(f"Tema en posición {i} debe ser un diccionario")
            
            required_keys = ['id', 'nombre', 'archivo']
            for key in required_keys:
                if key not in tema:
                    raise ValueError(f"Tema en posición {i} debe tener campo '{key}'")
    
    def __repr__(self) -> str:
        """Representación legible de la materia"""
        return f"{self.nombre} ({self.creditos} créditos, {len(self.temas)} temas)"
    
    def __str__(self) -> str:
        """Conversión a string para print()"""
        return self.__repr__()
    
    @property
    def total_temas(self) -> int:
        """Retorna el número total de temas de la materia"""
        return len(self.temas)
    
    def get_tema_info(self, tema_id: str) -> Optional[Dict[str, str]]:
        """
        Busca la información básica de un tema por su ID.
        
        Args:
            tema_id (str): ID del tema a buscar
        
        Returns:
            Diccionario con info del tema (id, nombre, archivo) o None
        
        Example:
            >>> info = materia.get_tema_info("teoria_conjuntos")
            >>> print(info['nombre'])
            Teoría de Conjuntos
        """
        for tema in self.temas:
            if tema['id'] == tema_id:
                return tema
        return None
    
    def get_tema_by_nombre(self, nombre: str) -> Optional[Dict[str, str]]:
        """
        Busca un tema por su nombre (búsqueda parcial, case-insensitive).
        
        Args:
            nombre (str): Nombre o parte del nombre del tema
        
        Returns:
            Diccionario con info del tema o None
        """
        nombre_lower = nombre.lower()
        for tema in self.temas:
            if nombre_lower in tema['nombre'].lower():
                return tema
        return None
    
    def get_archivo_tema(self, tema_id: str) -> Optional[str]:
        """
        Obtiene el nombre del archivo JSON de un tema específico.
        
        Args:
            tema_id (str): ID del tema
        
        Returns:
            Nombre del archivo (ej: "teoria_conjuntos.json") o None
        
        Example:
            >>> archivo = materia.get_archivo_tema("teoria_conjuntos")
            >>> print(archivo)
            teoria_conjuntos.json
        """
        tema_info = self.get_tema_info(tema_id)
        return tema_info['archivo'] if tema_info else None
    
    def listar_temas(self) -> List[str]:
        """
        Retorna una lista con los nombres de todos los temas.
        
        Returns:
            Lista de strings con los nombres de los temas
        
        Example:
            >>> temas = materia.listar_temas()
            >>> print(temas)
            ['Teoría de Conjuntos', 'Álgebra Booleana', ...]
        """
        return [tema['nombre'] for tema in self.temas]
    
    def listar_ids_temas(self) -> List[str]:
        """
        Retorna una lista con los IDs de todos los temas.
        
        Returns:
            Lista de strings con los IDs de los temas
        """
        return [tema['id'] for tema in self.temas]
    
    def buscar_temas(self, query: str) -> List[Dict[str, str]]:
        """
        Busca temas cuyo nombre contenga la query (case-insensitive).
        
        Args:
            query (str): Término de búsqueda
        
        Returns:
            Lista de diccionarios con los temas que coinciden
        
        Example:
            >>> resultados = materia.buscar_temas("lógica")
            >>> for tema in resultados:
            ...     print(tema['nombre'])
            Lógica Proposicional
            Lógica de Predicados
        """
        query_lower = query.lower()
        return [
            tema for tema in self.temas
            if query_lower in tema['nombre'].lower() or query_lower in tema['id'].lower()
        ]
    
    def to_dict(self) -> dict:
        """
        Convierte la materia a diccionario (útil para serialización).
        
        Returns:
            Diccionario con la información de la materia
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'creditos': self.creditos,
            'total_temas': self.total_temas,
            'temas': self.temas
        }
    
    def info_resumen(self) -> str:
        """
        Retorna un resumen formateado de la materia.
        
        Returns:
            String con información resumida de la materia
        """
        lineas = [
            f"\n{'='*60}",
            f"MATERIA: {self.nombre}",
            f"{'='*60}",
            f"ID: {self.id}",
            f"Créditos: {self.creditos}",
            f"Total de temas: {self.total_temas}",
            f"\nTemas:",
        ]
        
        for i, tema in enumerate(self.temas, 1):
            lineas.append(f"  {i}. {tema['nombre']}")
            lineas.append(f"     ID: {tema['id']}")
            lineas.append(f"     Archivo: {tema['archivo']}")
        
        return "\n".join(lineas)
    
    def validate_tema_exists(self, tema_id: str) -> bool:
        """
        Verifica si un tema existe en esta materia.
        
        Args:
            tema_id (str): ID del tema a verificar
        
        Returns:
            True si el tema existe, False en caso contrario
        """
        return any(tema['id'] == tema_id for tema in self.temas)