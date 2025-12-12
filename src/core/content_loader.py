"""
Cargador de Contenido de Temas

Este módulo implementa carga perezosa (lazy loading) de temas.
Los temas solo se cargan cuando el usuario los solicita,
no todos al inicio de la aplicación.
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any
import logging

from ..models.topic import Topic
from ..models.challenge import Challenge
from ..models.project import Project


# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContentLoader:
    """
    Cargador de contenido de temas con lazy loading.
    
    Esta clase se encarga de:
    - Cargar archivos JSON de temas bajo demanda
    - Validar el contenido cargado
    - Crear objetos Topic, Challenge o Project según corresponda
    - Manejar errores de carga
    
    Attributes:
        base_path (Path): Ruta base donde están las carpetas de semestres
        cache (Dict): Caché opcional de temas cargados (manejado externamente)
    
    Example:
        >>> loader = ContentLoader("src/data/content")
        >>> topic = loader.load_topic(1, "algebra_superior", "teoria_conjuntos.json")
        >>> print(topic.titulo)
    """
    
    def __init__(self, content_base_path: str | Path):
        """
        Inicializa el cargador de contenido.
        
        Args:
            content_base_path: Ruta base del contenido (donde están semestre_1, semestre_2, etc.)
        """
        self.base_path = Path(content_base_path)
        
        # Verificar que la ruta base existe
        if not self.base_path.exists():
            logger.warning(f"⚠️  Ruta base no existe: {self.base_path}")
        
        logger.info(f"ContentLoader inicializado con base: {self.base_path}")
    
    def load_topic(self, semestre_num: int, materia_id: str, tema_archivo: str) -> Topic:
        """
        Carga un tema específico (lazy loading).
        
        Args:
            semestre_num (int): Número de semestre (1-4)
            materia_id (str): ID de la materia (ej: "algebra_superior")
            tema_archivo (str): Nombre del archivo JSON (ej: "teoria_conjuntos.json")
        
        Returns:
            Topic: Objeto Topic con todo el contenido
        
        Raises:
            FileNotFoundError: Si el archivo no existe
            json.JSONDecodeError: Si el JSON es inválido
            KeyError: Si faltan secciones obligatorias
            ValueError: Si los datos no son válidos
        
        Example:
            >>> topic = loader.load_topic(1, "algebra_superior", "teoria_conjuntos.json")
            >>> print(topic.titulo)
            Teoría de Conjuntos y Operaciones Fundamentales
        """
        # Construir ruta completa
        ruta = self._construir_ruta(semestre_num, materia_id, tema_archivo)
        
        logger.info(f"Cargando tema: {ruta}")
        
        # Verificar que el archivo existe
        if not ruta.exists():
            error_msg = f"Archivo no encontrado: {ruta}"
            logger.error(f"❌ {error_msg}")
            raise FileNotFoundError(error_msg)
        
        try:
            # Cargar JSON
            with open(ruta, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validar y crear Topic
            topic = Topic(data)
            
            logger.info(f"✅ Tema cargado: {topic.titulo}")
            return topic
            
        except json.JSONDecodeError as e:
            error_msg = f"Error de sintaxis JSON en {ruta}: {e}"
            logger.error(f"❌ {error_msg}")
            raise
        
        except KeyError as e:
            error_msg = f"Falta sección obligatoria en {ruta}: {e}"
            logger.error(f"❌ {error_msg}")
            raise
        
        except ValueError as e:
            error_msg = f"Datos inválidos en {ruta}: {e}"
            logger.error(f"❌ {error_msg}")
            raise
        
        except Exception as e:
            error_msg = f"Error inesperado cargando {ruta}: {e}"
            logger.error(f"❌ {error_msg}")
            raise
    
    def load_challenge(self, semestre_num: int, materia_id: str, tema_archivo: str) -> Optional[Challenge]:
        """
        Carga solo el reto de programación de un tema.
        
        Args:
            semestre_num (int): Número de semestre
            materia_id (str): ID de la materia
            tema_archivo (str): Nombre del archivo JSON
        
        Returns:
            Challenge o None si el tema no tiene reto de programación
        
        Example:
            >>> challenge = loader.load_challenge(1, "intro_programacion", "recursividad.json")
            >>> if challenge:
            ...     print(challenge.codigo_inicial)
        """
        try:
            # Cargar el tema completo
            topic = self.load_topic(semestre_num, materia_id, tema_archivo)
            
            # Verificar si es un reto de programación
            if topic.es_reto_programacion:
                challenge = Challenge(topic.reto_proyecto)
                logger.info(f"✅ Challenge cargado: {challenge.titulo}")
                return challenge
            else:
                logger.info(f"ℹ️  Tema no tiene reto de programación")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error cargando challenge: {e}")
            raise
    
    def load_project(self, semestre_num: int, materia_id: str, tema_archivo: str) -> Optional[Project]:
        """
        Carga solo el proyecto conceptual de un tema.
        
        Args:
            semestre_num (int): Número de semestre
            materia_id (str): ID de la materia
            tema_archivo (str): Nombre del archivo JSON
        
        Returns:
            Project o None si el tema no tiene proyecto conceptual
        
        Example:
            >>> project = loader.load_project(1, "calculo_dif_int", "derivadas_basicas.json")
            >>> if project:
            ...     print(project.objetivos)
        """
        try:
            # Cargar el tema completo
            topic = self.load_topic(semestre_num, materia_id, tema_archivo)
            
            # Verificar si es un proyecto conceptual
            if topic.es_proyecto_conceptual:
                project = Project(topic.reto_proyecto)
                logger.info(f"✅ Project cargado: {project.titulo}")
                return project
            else:
                logger.info(f"ℹ️  Tema no tiene proyecto conceptual")
                return None
                
        except Exception as e:
            logger.error(f"❌ Error cargando project: {e}")
            raise
    
    def _construir_ruta(self, semestre_num: int, materia_id: str, tema_archivo: str) -> Path:
        """
        Construye la ruta completa a un archivo de tema.
        
        Args:
            semestre_num (int): Número de semestre
            materia_id (str): ID de la materia
            tema_archivo (str): Nombre del archivo
        
        Returns:
            Path: Ruta completa al archivo
        
        Example:
            >>> ruta = loader._construir_ruta(1, "algebra_superior", "teoria_conjuntos.json")
            >>> print(ruta)
            .../src/data/content/semestre_1/algebra_superior/teoria_conjuntos.json
        """
        return self.base_path / f"semestre_{semestre_num}" / materia_id / tema_archivo
    
    def existe_archivo(self, semestre_num: int, materia_id: str, tema_archivo: str) -> bool:
        """
        Verifica si existe un archivo de tema.
        
        Args:
            semestre_num (int): Número de semestre
            materia_id (str): ID de la materia
            tema_archivo (str): Nombre del archivo
        
        Returns:
            bool: True si el archivo existe
        
        Example:
            >>> if loader.existe_archivo(1, "algebra_superior", "teoria_conjuntos.json"):
            ...     topic = loader.load_topic(1, "algebra_superior", "teoria_conjuntos.json")
        """
        ruta = self._construir_ruta(semestre_num, materia_id, tema_archivo)
        return ruta.exists()
    
    def listar_temas_disponibles(self, semestre_num: int, materia_id: str) -> list[str]:
        """
        Lista todos los archivos JSON disponibles en una materia.
        
        Args:
            semestre_num (int): Número de semestre
            materia_id (str): ID de la materia
        
        Returns:
            List[str]: Lista de nombres de archivos JSON
        
        Example:
            >>> temas = loader.listar_temas_disponibles(1, "algebra_superior")
            >>> print(temas)
            ['teoria_conjuntos.json', 'algebra_booleana.json', ...]
        """
        materia_path = self.base_path / f"semestre_{semestre_num}" / materia_id
        
        if not materia_path.exists():
            logger.warning(f"⚠️  Carpeta no existe: {materia_path}")
            return []
        
        # Buscar todos los archivos .json (excepto los que empiezan con _)
        archivos = [
            f.name for f in materia_path.glob("*.json")
            if not f.name.startswith('_')
        ]
        
        return sorted(archivos)
    
    def validar_tema(self, semestre_num: int, materia_id: str, tema_archivo: str) -> tuple[bool, list[str]]:
        """
        Valida un archivo de tema sin cargarlo completamente.
        
        Args:
            semestre_num (int): Número de semestre
            materia_id (str): ID de la materia
            tema_archivo (str): Nombre del archivo
        
        Returns:
            tuple: (es_valido, lista_de_errores)
        
        Example:
            >>> valido, errores = loader.validar_tema(1, "algebra_superior", "teoria_conjuntos.json")
            >>> if not valido:
            ...     for error in errores:
            ...         print(f"Error: {error}")
        """
        errores = []
        
        # Verificar que existe
        if not self.existe_archivo(semestre_num, materia_id, tema_archivo):
            errores.append(f"Archivo no existe: {tema_archivo}")
            return False, errores
        
        try:
            # Intentar cargar el tema
            topic = self.load_topic(semestre_num, materia_id, tema_archivo)
            
            # Verificar que tenga contenido completo
            if not topic.tiene_contenido_completo():
                errores.append("Algunas secciones están vacías")
            
            # Validar metadata
            if not topic.id:
                errores.append("Falta ID en metadata")
            if not topic.titulo:
                errores.append("Falta título en metadata")
            
            # Validar reto/proyecto según tipo
            if topic.es_reto_programacion:
                if not topic.get_codigo_inicial():
                    errores.append("Reto de programación sin código inicial")
                if not topic.get_solucion_referencia():
                    errores.append("Reto de programación sin solución")
            
            elif topic.es_proyecto_conceptual:
                if not topic.get_objetivos_proyecto():
                    errores.append("Proyecto sin objetivos")
            
        except Exception as e:
            errores.append(f"Error al cargar: {str(e)}")
        
        return len(errores) == 0, errores
    
    def obtener_metadatos(self, semestre_num: int, materia_id: str, tema_archivo: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene solo los metadatos de un tema sin cargar todo el contenido.
        
        Útil para mostrar previews o listados sin cargar archivos completos.
        
        Args:
            semestre_num (int): Número de semestre
            materia_id (str): ID de la materia
            tema_archivo (str): Nombre del archivo
        
        Returns:
            Dict con metadatos o None si hay error
        
        Example:
            >>> meta = loader.obtener_metadatos(1, "algebra_superior", "teoria_conjuntos.json")
            >>> print(meta['titulo'])
            >>> print(meta['dificultad'])
        """
        try:
            ruta = self._construir_ruta(semestre_num, materia_id, tema_archivo)
            
            with open(ruta, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Retornar solo metadata
            return data.get('metadata', {})
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo metadatos de {tema_archivo}: {e}")
            return None
    
    def cargar_multiple(self, temas: list[tuple[int, str, str]]) -> Dict[str, Topic]:
        """
        Carga múltiples temas en una sola operación.
        
        Útil para precarga o cuando se necesitan varios temas al mismo tiempo.
        
        Args:
            temas: Lista de tuplas (semestre_num, materia_id, tema_archivo)
        
        Returns:
            Dict con clave "semestre_materia_archivo" y valor Topic
        
        Example:
            >>> temas_a_cargar = [
            ...     (1, "algebra_superior", "teoria_conjuntos.json"),
            ...     (1, "geometria", "sistemas_coordenadas.json")
            ... ]
            >>> topics = loader.cargar_multiple(temas_a_cargar)
            >>> for key, topic in topics.items():
            ...     print(f"{key}: {topic.titulo}")
        """
        resultados = {}
        
        for semestre_num, materia_id, tema_archivo in temas:
            key = f"{semestre_num}_{materia_id}_{tema_archivo}"
            
            try:
                topic = self.load_topic(semestre_num, materia_id, tema_archivo)
                resultados[key] = topic
                logger.debug(f"✓ Cargado: {key}")
            
            except Exception as e:
                logger.error(f"❌ Error cargando {key}: {e}")
                # Continuar con los demás temas
        
        logger.info(f"✅ Carga múltiple completada: {len(resultados)}/{len(temas)} exitosos")
        return resultados
    
    def get_estadisticas_materia(self, semestre_num: int, materia_id: str) -> Dict[str, Any]:
        """
        Obtiene estadísticas de una materia (sin cargar todos los temas).
        
        Args:
            semestre_num (int): Número de semestre
            materia_id (str): ID de la materia
        
        Returns:
            Dict con estadísticas
        """
        archivos = self.listar_temas_disponibles(semestre_num, materia_id)
        
        total_retos_programacion = 0
        total_proyectos = 0
        
        for archivo in archivos:
            meta = self.obtener_metadatos(semestre_num, materia_id, archivo)
            if meta:
                # Aquí necesitaríamos cargar el tema para saber el tipo
                # Por ahora solo contamos archivos
                pass
        
        return {
            'total_temas': len(archivos),
            'temas_disponibles': archivos,
            'retos_programacion': total_retos_programacion,
            'proyectos_conceptuales': total_proyectos
        }