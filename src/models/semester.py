
"""
Modelo de datos para un Semestre académico

Este módulo define la clase Semester que representa un semestre
completo de la licenciatura con todas sus materias.
"""

from typing import List, Optional
from dataclasses import dataclass


@dataclass
class Semester:
    """
    Representa un semestre académico completo.
    
    Attributes:
        numero (int): Número del semestre (1-4)
        nombre (str): Nombre descriptivo del semestre (ej: "Primer Semestre")
        materias (List[Subject]): Lista de materias del semestre
    
    Example:
        >>> semestre = Semester(
        ...     numero=1,
        ...     nombre="Primer Semestre",
        ...     materias=[materia1, materia2]
        ... )
        >>> print(semestre)
        Semestre 1: Primer Semestre (6 materias)
    """
    
    numero: int
    nombre: str
    materias: List['Subject']  # Forward reference para Subject
    
    def __post_init__(self):
        """Validación después de la inicialización"""
        if not 1 <= self.numero <= 4:
            raise ValueError(f"Número de semestre debe estar entre 1 y 4, recibido: {self.numero}")
        
        if not self.nombre:
            raise ValueError("El nombre del semestre no puede estar vacío")
        
        if not isinstance(self.materias, list):
            raise TypeError("materias debe ser una lista")
    
    def __repr__(self) -> str:
        """Representación legible del semestre"""
        return f"Semestre {self.numero}: {self.nombre} ({len(self.materias)} materias)"
    
    def __str__(self) -> str:
        """Conversión a string para print()"""
        return self.__repr__()
    
    @property
    def total_materias(self) -> int:
        """Retorna el número total de materias en el semestre"""
        return len(self.materias)
    
    @property
    def total_creditos(self) -> int:
        """Calcula el total de créditos del semestre"""
        return sum(materia.creditos for materia in self.materias)
    
    @property
    def total_temas(self) -> int:
        """Calcula el total de temas en todas las materias del semestre"""
        return sum(materia.total_temas for materia in self.materias)
    
    def get_materia_by_id(self, materia_id: str) -> Optional['Subject']:
        """
        Busca una materia por su ID.
        
        Args:
            materia_id (str): ID de la materia a buscar
        
        Returns:
            Subject o None si no se encuentra
        
        Example:
            >>> materia = semestre.get_materia_by_id("algebra_superior")
            >>> print(materia.nombre)
            Álgebra Superior
        """
        for materia in self.materias:
            if materia.id == materia_id:
                return materia
        return None
    
    def get_materia_by_nombre(self, nombre: str) -> Optional['Subject']:
        """
        Busca una materia por su nombre (búsqueda parcial, case-insensitive).
        
        Args:
            nombre (str): Nombre o parte del nombre de la materia
        
        Returns:
            Subject o None si no se encuentra
        
        Example:
            >>> materia = semestre.get_materia_by_nombre("álgebra")
            >>> print(materia.nombre)
            Álgebra Superior
        """
        nombre_lower = nombre.lower()
        for materia in self.materias:
            if nombre_lower in materia.nombre.lower():
                return materia
        return None
    
    def listar_materias(self) -> List[str]:
        """
        Retorna una lista con los nombres de todas las materias.
        
        Returns:
            Lista de strings con los nombres de las materias
        
        Example:
            >>> materias = semestre.listar_materias()
            >>> print(materias)
            ['Álgebra Superior', 'Geometría', 'Cálculo', ...]
        """
        return [materia.nombre for materia in self.materias]
    
    def to_dict(self) -> dict:
        """
        Convierte el semestre a diccionario (útil para serialización).
        
        Returns:
            Diccionario con la información del semestre
        """
        return {
            'numero': self.numero,
            'nombre': self.nombre,
            'total_materias': self.total_materias,
            'total_creditos': self.total_creditos,
            'total_temas': self.total_temas,
            'materias': [materia.to_dict() for materia in self.materias]
        }
    
    def info_resumen(self) -> str:
        """
        Retorna un resumen formateado del semestre.
        
        Returns:
            String con información resumida del semestre
        """
        lineas = [
            f"{'='*60}",
            f"SEMESTRE {self.numero}: {self.nombre}",
            f"{'='*60}",
            f"Total de materias: {self.total_materias}",
            f"Total de créditos: {self.total_creditos}",
            f"Total de temas: {self.total_temas}",
            f"\nMaterias:",
        ]
        
        for i, materia in enumerate(self.materias, 1):
            lineas.append(f"  {i}. {materia.nombre} ({materia.creditos} créditos, {materia.total_temas} temas)")
        
        return "\n".join(lineas)


# Evitar importación circular
from .subject import Subject