"""
Cargador de Curriculum

Este módulo se encarga de cargar y parsear el archivo curriculum.json
que contiene la estructura completa de semestres, materias y temas.
"""

import json
from pathlib import Path
from typing import List, Optional, Dict, Any
import logging

from ..models.semester import Semester
from ..models.subject import Subject


# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CurriculumLoader:
    """
    Cargador del curriculum académico.
    
    Esta clase se encarga de:
    - Cargar el archivo curriculum.json
    - Validar su estructura
    - Convertir los datos a objetos Semester y Subject
    - Proveer métodos de búsqueda y acceso
    
    Attributes:
        curriculum_path (Path): Ruta al archivo curriculum.json
        data (Dict): Datos JSON cargados
        semestres (List[Semester]): Lista de semestres parseados
        version (str): Versión del curriculum
        ultima_actualizacion (str): Fecha de última actualización
    
    Example:
        >>> loader = CurriculumLoader("src/data/curriculum.json")
        >>> if loader.load():
        ...     semestres = loader.get_semestres()
        ...     print(f"Cargados {len(semestres)} semestres")
    """
    
    def __init__(self, curriculum_path: str | Path):
        """
        Inicializa el cargador.
        
        Args:
            curriculum_path: Ruta al archivo curriculum.json
        """
        self.curriculum_path = Path(curriculum_path)
        self.data: Optional[Dict[str, Any]] = None
        self.semestres: List[Semester] = []
        self.version: str = ""
        self.ultima_actualizacion: str = ""
        
        logger.info(f"CurriculumLoader inicializado con ruta: {self.curriculum_path}")
    
    def load(self) -> bool:
        """
        Carga y parsea el archivo curriculum.json.
        
        Returns:
            bool: True si la carga fue exitosa, False en caso contrario
        
        Raises:
            FileNotFoundError: Si el archivo no existe
            json.JSONDecodeError: Si el archivo no es JSON válido
        """
        try:
            # Verificar que el archivo existe
            if not self.curriculum_path.exists():
                logger.error(f"Archivo no encontrado: {self.curriculum_path}")
                raise FileNotFoundError(f"No se encontró el archivo: {self.curriculum_path}")
            
            # Cargar JSON
            logger.info(f"Cargando curriculum desde: {self.curriculum_path}")
            with open(self.curriculum_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            
            # Validar estructura básica
            if not self._validar_estructura():
                return False
            
            # Extraer metadata
            self.version = self.data.get('version', 'desconocida')
            self.ultima_actualizacion = self.data.get('ultima_actualizacion', 'desconocida')
            
            logger.info(f"Curriculum v{self.version} cargado (actualización: {self.ultima_actualizacion})")
            
            # Parsear semestres
            self._parse_semestres()
            
            logger.info(f"✅ Curriculum cargado exitosamente: {len(self.semestres)} semestres")
            return True
            
        except FileNotFoundError as e:
            logger.error(f"❌ Error: {e}")
            raise
        
        except json.JSONDecodeError as e:
            logger.error(f"❌ Error al decodificar JSON: {e}")
            raise
        
        except Exception as e:
            logger.error(f"❌ Error inesperado al cargar curriculum: {e}")
            return False
    
    def _validar_estructura(self) -> bool:
        """
        Valida que el JSON tenga la estructura esperada.
        
        Returns:
            bool: True si la estructura es válida
        """
        if not self.data:
            logger.error("Datos vacíos")
            return False
        
        # Verificar campos requeridos
        if 'semestres' not in self.data:
            logger.error("Falta campo 'semestres' en curriculum.json")
            return False
        
        if not isinstance(self.data['semestres'], list):
            logger.error("'semestres' debe ser una lista")
            return False
        
        if len(self.data['semestres']) == 0:
            logger.warning("⚠️  No hay semestres definidos")
            return False
        
        logger.debug("✓ Estructura básica válida")
        return True
    
    def _parse_semestres(self):
        """
        Convierte los datos JSON en objetos Semester.
        """
        self.semestres = []
        
        for sem_data in self.data['semestres']:
            try:
                # Parsear materias del semestre
                materias = self._parse_materias(sem_data.get('materias', []))
                
                # Crear objeto Semester
                semestre = Semester(
                    numero=sem_data['numero'],
                    nombre=sem_data['nombre'],
                    materias=materias
                )
                
                self.semestres.append(semestre)
                logger.debug(f"✓ Semestre {semestre.numero} parseado: {len(materias)} materias")
                
            except KeyError as e:
                logger.error(f"❌ Error parseando semestre: falta campo {e}")
                raise
            
            except Exception as e:
                logger.error(f"❌ Error parseando semestre {sem_data.get('numero', '?')}: {e}")
                raise
    
    def _parse_materias(self, materias_data: List[Dict]) -> List[Subject]:
        """
        Convierte los datos de materias en objetos Subject.
        
        Args:
            materias_data: Lista de diccionarios con datos de materias
        
        Returns:
            List[Subject]: Lista de objetos Subject
        """
        materias = []
        
        for mat_data in materias_data:
            try:
                # Crear objeto Subject
                materia = Subject(
                    id=mat_data['id'],
                    nombre=mat_data['nombre'],
                    creditos=mat_data.get('creditos', 0),
                    temas=mat_data.get('temas', [])
                )
                
                materias.append(materia)
                logger.debug(f"  ✓ Materia '{materia.nombre}' parseada: {len(materia.temas)} temas")
                
            except KeyError as e:
                logger.error(f"❌ Error parseando materia: falta campo {e}")
                raise
            
            except Exception as e:
                logger.error(f"❌ Error parseando materia '{mat_data.get('nombre', '?')}': {e}")
                raise
        
        return materias
    
    # ==================== MÉTODOS DE ACCESO ====================
    
    def get_semestres(self) -> List[Semester]:
        """
        Obtiene la lista completa de semestres.
        
        Returns:
            List[Semester]: Lista de todos los semestres
        """
        return self.semestres
    
    def get_semestre(self, numero: int) -> Optional[Semester]:
        """
        Obtiene un semestre específico por número.
        
        Args:
            numero (int): Número del semestre (1-4)
        
        Returns:
            Semester o None si no se encuentra
        
        Example:
            >>> semestre = loader.get_semestre(1)
            >>> print(semestre.nombre)
            Primer Semestre
        """
        for semestre in self.semestres:
            if semestre.numero == numero:
                return semestre
        
        logger.warning(f"⚠️  Semestre {numero} no encontrado")
        return None
    
    def get_materia(self, semestre_num: int, materia_id: str) -> Optional[Subject]:
        """
        Obtiene una materia específica.
        
        Args:
            semestre_num (int): Número del semestre
            materia_id (str): ID de la materia
        
        Returns:
            Subject o None si no se encuentra
        
        Example:
            >>> materia = loader.get_materia(1, "algebra_superior")
            >>> print(materia.nombre)
            Álgebra Superior
        """
        semestre = self.get_semestre(semestre_num)
        if semestre:
            return semestre.get_materia_by_id(materia_id)
        return None
    
    def get_tema_info(self, semestre_num: int, materia_id: str, tema_id: str) -> Optional[Dict]:
        """
        Obtiene la información básica de un tema.
        
        Args:
            semestre_num (int): Número del semestre
            materia_id (str): ID de la materia
            tema_id (str): ID del tema
        
        Returns:
            Dict con info del tema (id, nombre, archivo) o None
        """
        materia = self.get_materia(semestre_num, materia_id)
        if materia:
            return materia.get_tema_info(tema_id)
        return None
    
    # ==================== MÉTODOS DE BÚSQUEDA ====================
    
    def buscar_materias(self, query: str) -> List[tuple[int, Subject]]:
        """
        Busca materias por nombre (búsqueda parcial).
        
        Args:
            query (str): Término de búsqueda
        
        Returns:
            List de tuplas (semestre_numero, Subject)
        
        Example:
            >>> resultados = loader.buscar_materias("álgebra")
            >>> for sem_num, materia in resultados:
            ...     print(f"Sem {sem_num}: {materia.nombre}")
        """
        resultados = []
        query_lower = query.lower()
        
        for semestre in self.semestres:
            for materia in semestre.materias:
                if query_lower in materia.nombre.lower() or query_lower in materia.id.lower():
                    resultados.append((semestre.numero, materia))
        
        return resultados
    
    def buscar_temas(self, query: str) -> List[Dict[str, Any]]:
        """
        Busca temas en todo el curriculum.
        
        Args:
            query (str): Término de búsqueda
        
        Returns:
            List de diccionarios con info del tema y su ubicación
        
        Example:
            >>> resultados = loader.buscar_temas("recursividad")
            >>> for tema in resultados:
            ...     print(f"{tema['semestre']}.{tema['materia']}: {tema['nombre']}")
        """
        resultados = []
        query_lower = query.lower()
        
        for semestre in self.semestres:
            for materia in semestre.materias:
                temas_encontrados = materia.buscar_temas(query)
                
                for tema in temas_encontrados:
                    resultados.append({
                        'semestre': semestre.numero,
                        'semestre_nombre': semestre.nombre,
                        'materia_id': materia.id,
                        'materia_nombre': materia.nombre,
                        'tema_id': tema['id'],
                        'tema_nombre': tema['nombre'],
                        'archivo': tema['archivo']
                    })
        
        return resultados
    
    # ==================== MÉTODOS DE ESTADÍSTICAS ====================
    
    def get_estadisticas(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas generales del curriculum.
        
        Returns:
            Dict con estadísticas
        """
        total_materias = sum(sem.total_materias for sem in self.semestres)
        total_creditos = sum(sem.total_creditos for sem in self.semestres)
        total_temas = sum(sem.total_temas for sem in self.semestres)
        
        return {
            'version': self.version,
            'ultima_actualizacion': self.ultima_actualizacion,
            'total_semestres': len(self.semestres),
            'total_materias': total_materias,
            'total_creditos': total_creditos,
            'total_temas': total_temas,
            'promedio_materias_por_semestre': total_materias / len(self.semestres) if self.semestres else 0,
            'promedio_temas_por_materia': total_temas / total_materias if total_materias else 0
        }
    
    def info_resumen(self) -> str:
        """
        Genera un resumen completo del curriculum.
        
        Returns:
            str: Resumen formateado
        """
        stats = self.get_estadisticas()
        
        lineas = [
            f"\n{'='*70}",
            f"CURRICULUM - LICENCIATURA EN INTELIGENCIA ARTIFICIAL",
            f"{'='*70}",
            f"Versión: {stats['version']}",
            f"Última actualización: {stats['ultima_actualizacion']}",
            f"\n📊 ESTADÍSTICAS GENERALES:",
            f"  - Total de semestres: {stats['total_semestres']}",
            f"  - Total de materias: {stats['total_materias']}",
            f"  - Total de créditos: {stats['total_creditos']}",
            f"  - Total de temas: {stats['total_temas']}",
            f"  - Promedio materias/semestre: {stats['promedio_materias_por_semestre']:.1f}",
            f"  - Promedio temas/materia: {stats['promedio_temas_por_materia']:.1f}",
            f"\n📚 DESGLOSE POR SEMESTRE:",
        ]
        
        for semestre in self.semestres:
            lineas.append(f"\n  {semestre.nombre}:")
            lineas.append(f"    Materias: {semestre.total_materias}")
            lineas.append(f"    Créditos: {semestre.total_creditos}")
            lineas.append(f"    Temas: {semestre.total_temas}")
        
        lineas.append(f"\n{'='*70}\n")
        
        return "\n".join(lineas)
    
    # ==================== MÉTODOS DE VALIDACIÓN ====================
    
    def validar_integridad(self) -> tuple[bool, List[str]]:
        """
        Valida la integridad de los datos cargados.
        
        Returns:
            tuple: (es_valido, lista_de_problemas)
        """
        problemas = []
        
        # Verificar que hay semestres
        if not self.semestres:
            problemas.append("No hay semestres cargados")
            return False, problemas
        
        # Verificar cada semestre
        for semestre in self.semestres:
            if semestre.total_materias == 0:
                problemas.append(f"Semestre {semestre.numero} no tiene materias")
            
            # Verificar cada materia
            for materia in semestre.materias:
                if materia.total_temas == 0:
                    problemas.append(f"Materia '{materia.nombre}' (Sem {semestre.numero}) no tiene temas")
        
        return len(problemas) == 0, problemas