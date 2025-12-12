"""
Gestor Central de Datos (Data Manager)

Este módulo es el coordinador principal del sistema de datos.
Integra CurriculumLoader y ContentLoader, maneja caché y provee
una interfaz única para acceder a toda la información.
"""

from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
import logging

from ..models.semester import Semester
from ..models.subject import Subject
from ..models.topic import Topic
from ..models.challenge import Challenge
from ..models.project import Project
from .curriculum_loader import CurriculumLoader
from .content_loader import ContentLoader


# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataManager:
    """
    Coordinador central del sistema de datos.
    
    Esta clase:
    - Coordina CurriculumLoader y ContentLoader
    - Maneja caché de temas cargados
    - Provee interfaz unificada para la UI
    - Gestiona el estado de carga
    - Ofrece métodos de búsqueda avanzada
    
    Attributes:
        base_path (Path): Ruta base de datos
        curriculum_loader (CurriculumLoader): Cargador de curriculum
        content_loader (ContentLoader): Cargador de contenido
        semestres (List[Semester]): Semestres cargados
        cache (Dict): Caché de temas y objetos cargados
        inicializado (bool): Estado de inicialización
    
    Example:
        >>> dm = DataManager()
        >>> if dm.initialize():
        ...     topic = dm.get_topic(1, "algebra_superior", "teoria_conjuntos.json")
        ...     print(topic.titulo)
    """
    
    def __init__(self, base_path: Optional[str | Path] = None):
        """
        Inicializa el Data Manager.
        
        Args:
            base_path: Ruta base de datos (default: src/data)
        """
        # Determinar ruta base
        if base_path is None:
            # Asumir estructura: data_manager.py está en src/core/
            self.base_path = Path(__file__).parent.parent / "data"
        else:
            self.base_path = Path(base_path)
        
        logger.info(f"DataManager inicializado con base: {self.base_path}")
        
        # Inicializar loaders
        self.curriculum_loader = CurriculumLoader(
            self.base_path / "curriculum.json"
        )
        self.content_loader = ContentLoader(
            self.base_path / "content"
        )
        
        # Estado
        self.semestres: List[Semester] = []
        self.cache: Dict[str, Any] = {
            'topics': {},      # Cache de Topics completos
            'challenges': {},  # Cache de Challenges
            'projects': {},    # Cache de Projects
            'metadata': {}     # Cache de metadatos
        }
        self.inicializado = False
        
        # Estadísticas de uso
        self._stats = {
            'cache_hits': 0,
            'cache_misses': 0,
            'topics_loaded': 0,
            'challenges_loaded': 0,
            'projects_loaded': 0
        }
    
    # ==================== INICIALIZACIÓN ====================
    
    def initialize(self) -> bool:
        """
        Inicializa el sistema completo cargando el curriculum.
        
        Este método debe llamarse antes de usar cualquier otra funcionalidad.
        
        Returns:
            bool: True si la inicialización fue exitosa
        
        Example:
            >>> dm = DataManager()
            >>> if dm.initialize():
            ...     print("Sistema listo")
        """
        logger.info("🔄 Inicializando DataManager...")
        
        try:
            # Cargar curriculum
            if not self.curriculum_loader.load():
                logger.error("❌ Error cargando curriculum")
                return False
            
            # Obtener semestres
            self.semestres = self.curriculum_loader.get_semestres()
            
            if not self.semestres:
                logger.error("❌ No se cargaron semestres")
                return False
            
            self.inicializado = True
            logger.info(f"✅ DataManager inicializado: {len(self.semestres)} semestres")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error en inicialización: {e}")
            return False
    
    def verificar_inicializacion(self) -> bool:
        """
        Verifica si el DataManager está inicializado.
        
        Returns:
            bool: True si está inicializado
        """
        if not self.inicializado:
            logger.warning("⚠️  DataManager no inicializado. Llama a initialize() primero")
        return self.inicializado
    
    # ==================== ACCESO A ESTRUCTURA ====================
    
    def get_semestres(self) -> List[Semester]:
        """
        Obtiene todos los semestres.
        
        Returns:
            List[Semester]: Lista de semestres
        """
        if not self.verificar_inicializacion():
            return []
        return self.semestres
    
    def get_semestre(self, numero: int) -> Optional[Semester]:
        """
        Obtiene un semestre específico.
        
        Args:
            numero (int): Número del semestre (1-4)
        
        Returns:
            Semester o None
        """
        if not self.verificar_inicializacion():
            return None
        return self.curriculum_loader.get_semestre(numero)
    
    def get_materia(self, semestre_num: int, materia_id: str) -> Optional[Subject]:
        """
        Obtiene una materia específica.
        
        Args:
            semestre_num (int): Número del semestre
            materia_id (str): ID de la materia
        
        Returns:
            Subject o None
        """
        if not self.verificar_inicializacion():
            return None
        return self.curriculum_loader.get_materia(semestre_num, materia_id)
    
    # ==================== CARGA DE CONTENIDO (CON CACHÉ) ====================
    
    def get_topic(
        self,
        semestre_num: int,
        materia_id: str,
        tema_archivo: str,
        force_reload: bool = False
    ) -> Optional[Topic]:
        """
        Obtiene un tema completo (usa caché si existe).
        
        Args:
            semestre_num (int): Número del semestre
            materia_id (str): ID de la materia
            tema_archivo (str): Nombre del archivo JSON
            force_reload (bool): Forzar recarga (ignorar caché)
        
        Returns:
            Topic o None si hay error
        
        Example:
            >>> topic = dm.get_topic(1, "algebra_superior", "teoria_conjuntos.json")
            >>> print(topic.titulo)
        """
        if not self.verificar_inicializacion():
            return None
        
        # Generar clave de caché
        cache_key = self._generar_cache_key(semestre_num, materia_id, tema_archivo)
        
        # Verificar caché (si no se fuerza recarga)
        if not force_reload and cache_key in self.cache['topics']:
            logger.debug(f"✓ Cache hit: {cache_key}")
            self._stats['cache_hits'] += 1
            return self.cache['topics'][cache_key]
        
        # Cache miss - cargar desde disco
        logger.debug(f"⊙ Cache miss: {cache_key}")
        self._stats['cache_misses'] += 1
        
        try:
            topic = self.content_loader.load_topic(
                semestre_num, materia_id, tema_archivo
            )
            
            # Guardar en caché
            self.cache['topics'][cache_key] = topic
            self._stats['topics_loaded'] += 1
            
            return topic
            
        except Exception as e:
            logger.error(f"❌ Error cargando topic: {e}")
            return None
    
    def get_challenge(
        self,
        semestre_num: int,
        materia_id: str,
        tema_archivo: str,
        force_reload: bool = False
    ) -> Optional[Challenge]:
        """
        Obtiene solo el challenge de un tema (usa caché).
        
        Args:
            semestre_num (int): Número del semestre
            materia_id (str): ID de la materia
            tema_archivo (str): Nombre del archivo JSON
            force_reload (bool): Forzar recarga
        
        Returns:
            Challenge o None
        """
        if not self.verificar_inicializacion():
            return None
        
        cache_key = self._generar_cache_key(semestre_num, materia_id, tema_archivo)
        
        # Verificar caché
        if not force_reload and cache_key in self.cache['challenges']:
            logger.debug(f"✓ Cache hit (challenge): {cache_key}")
            self._stats['cache_hits'] += 1
            return self.cache['challenges'][cache_key]
        
        # Cargar desde disco
        try:
            challenge = self.content_loader.load_challenge(
                semestre_num, materia_id, tema_archivo
            )
            
            if challenge:
                self.cache['challenges'][cache_key] = challenge
                self._stats['challenges_loaded'] += 1
            
            return challenge
            
        except Exception as e:
            logger.error(f"❌ Error cargando challenge: {e}")
            return None
    
    def get_project(
        self,
        semestre_num: int,
        materia_id: str,
        tema_archivo: str,
        force_reload: bool = False
    ) -> Optional[Project]:
        """
        Obtiene solo el project de un tema (usa caché).
        
        Args:
            semestre_num (int): Número del semestre
            materia_id (str): ID de la materia
            tema_archivo (str): Nombre del archivo JSON
            force_reload (bool): Forzar recarga
        
        Returns:
            Project o None
        """
        if not self.verificar_inicializacion():
            return None
        
        cache_key = self._generar_cache_key(semestre_num, materia_id, tema_archivo)
        
        # Verificar caché
        if not force_reload and cache_key in self.cache['projects']:
            logger.debug(f"✓ Cache hit (project): {cache_key}")
            self._stats['cache_hits'] += 1
            return self.cache['projects'][cache_key]
        
        # Cargar desde disco
        try:
            project = self.content_loader.load_project(
                semestre_num, materia_id, tema_archivo
            )
            
            if project:
                self.cache['projects'][cache_key] = project
                self._stats['projects_loaded'] += 1
            
            return project
            
        except Exception as e:
            logger.error(f"❌ Error cargando project: {e}")
            return None
    
    def get_metadatos_tema(
        self,
        semestre_num: int,
        materia_id: str,
        tema_archivo: str
    ) -> Optional[Dict[str, Any]]:
        """
        Obtiene solo los metadatos de un tema (ligero, sin cargar todo).
        
        Args:
            semestre_num (int): Número del semestre
            materia_id (str): ID de la materia
            tema_archivo (str): Nombre del archivo
        
        Returns:
            Dict con metadatos o None
        """
        cache_key = f"meta_{self._generar_cache_key(semestre_num, materia_id, tema_archivo)}"
        
        # Verificar caché de metadatos
        if cache_key in self.cache['metadata']:
            return self.cache['metadata'][cache_key]
        
        # Cargar metadatos
        metadatos = self.content_loader.obtener_metadatos(
            semestre_num, materia_id, tema_archivo
        )
        
        if metadatos:
            self.cache['metadata'][cache_key] = metadatos
        
        return metadatos
    
    # ==================== BÚSQUEDA ====================
    
    def buscar_materias(self, query: str) -> List[Tuple[int, Subject]]:
        """
        Busca materias por nombre.
        
        Args:
            query (str): Término de búsqueda
        
        Returns:
            Lista de tuplas (semestre_num, Subject)
        """
        if not self.verificar_inicializacion():
            return []
        return self.curriculum_loader.buscar_materias(query)
    
    def buscar_temas(self, query: str) -> List[Dict[str, Any]]:
        """
        Busca temas en todo el curriculum.
        
        Args:
            query (str): Término de búsqueda
        
        Returns:
            Lista de diccionarios con info de temas encontrados
        """
        if not self.verificar_inicializacion():
            return []
        return self.curriculum_loader.buscar_temas(query)
    
    def buscar_temas_por_dificultad(self, dificultad: str) -> List[Dict[str, Any]]:
        """
        Busca temas por nivel de dificultad.
        
        Args:
            dificultad (str): 'basico', 'intermedio', 'avanzado'
        
        Returns:
            Lista de temas con esa dificultad
        """
        resultados = []
        
        for semestre in self.semestres:
            for materia in semestre.materias:
                for tema_info in materia.temas:
                    metadatos = self.get_metadatos_tema(
                        semestre.numero,
                        materia.id,
                        tema_info['archivo']
                    )
                    
                    if metadatos and metadatos.get('dificultad') == dificultad:
                        resultados.append({
                            'semestre': semestre.numero,
                            'materia': materia.nombre,
                            'materia_id': materia.id,
                            'tema': tema_info['nombre'],
                            'archivo': tema_info['archivo']
                        })
        
        return resultados
    
    def buscar_retos_programacion(self) -> List[Dict[str, Any]]:
        """
        Encuentra todos los retos de programación disponibles.
        
        Returns:
            Lista de retos de programación
        """
        resultados = []
        
        for semestre in self.semestres:
            for materia in semestre.materias:
                for tema_info in materia.temas:
                    try:
                        topic = self.get_topic(
                            semestre.numero,
                            materia.id,
                            tema_info['archivo']
                        )
                        
                        if topic and topic.es_reto_programacion:
                            resultados.append({
                                'semestre': semestre.numero,
                                'materia': materia.nombre,
                                'materia_id': materia.id,
                                'tema': tema_info['nombre'],
                                'archivo': tema_info['archivo'],
                                'titulo_reto': topic.titulo_reto,
                                'dificultad': topic.dificultad
                            })
                    except:
                        continue
        
        return resultados
    
    # ==================== GESTIÓN DE CACHÉ ====================
    
    def limpiar_cache(self, tipo: Optional[str] = None):
        """
        Limpia el caché.
        
        Args:
            tipo (str, optional): Tipo específico ('topics', 'challenges', 'projects', 'metadata')
                                  Si es None, limpia todo el caché
        """
        if tipo:
            if tipo in self.cache:
                size = len(self.cache[tipo])
                self.cache[tipo].clear()
                logger.info(f"🗑️  Cache limpiado: {tipo} ({size} items)")
        else:
            total = sum(len(cache) for cache in self.cache.values())
            for cache_type in self.cache:
                self.cache[cache_type].clear()
            logger.info(f"🗑️  Todo el cache limpiado ({total} items)")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del caché.
        
        Returns:
            Dict con estadísticas
        """
        return {
            'topics_cached': len(self.cache['topics']),
            'challenges_cached': len(self.cache['challenges']),
            'projects_cached': len(self.cache['projects']),
            'metadata_cached': len(self.cache['metadata']),
            'cache_hits': self._stats['cache_hits'],
            'cache_misses': self._stats['cache_misses'],
            'hit_rate': (
                self._stats['cache_hits'] / 
                (self._stats['cache_hits'] + self._stats['cache_misses'])
                if (self._stats['cache_hits'] + self._stats['cache_misses']) > 0
                else 0
            ),
            'topics_loaded': self._stats['topics_loaded'],
            'challenges_loaded': self._stats['challenges_loaded'],
            'projects_loaded': self._stats['projects_loaded']
        }
    
    def _generar_cache_key(self, semestre_num: int, materia_id: str, tema_archivo: str) -> str:
        """
        Genera una clave única para el caché.
        
        Args:
            semestre_num: Número de semestre
            materia_id: ID de materia
            tema_archivo: Nombre de archivo
        
        Returns:
            str: Clave de caché
        """
        return f"{semestre_num}_{materia_id}_{tema_archivo}"
    
    # ==================== ESTADÍSTICAS ====================
    
    def get_estadisticas_generales(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas generales del sistema.
        
        Returns:
            Dict con estadísticas completas
        """
        if not self.verificar_inicializacion():
            return {}
        
        stats_curriculum = self.curriculum_loader.get_estadisticas()
        stats_cache = self.get_cache_stats()
        
        return {
            **stats_curriculum,
            'cache': stats_cache,
            'inicializado': self.inicializado
        }
    
    def get_progreso_materia(self, semestre_num: int, materia_id: str) -> Dict[str, Any]:
        """
        Obtiene estadísticas de una materia específica.
        
        Args:
            semestre_num: Número de semestre
            materia_id: ID de materia
        
        Returns:
            Dict con estadísticas de la materia
        """
        materia = self.get_materia(semestre_num, materia_id)
        if not materia:
            return {}
        
        return {
            'nombre': materia.nombre,
            'creditos': materia.creditos,
            'total_temas': materia.total_temas,
            'temas': materia.temas
        }
    
    # ==================== VALIDACIÓN ====================
    
    def validar_integridad_completa(self) -> Tuple[bool, List[str]]:
        """
        Valida la integridad de todo el sistema.
        
        Returns:
            tuple: (es_valido, lista_problemas)
        """
        if not self.verificar_inicializacion():
            return False, ["Sistema no inicializado"]
        
        problemas = []
        
        # Validar curriculum
        valido_curriculum, probs_curriculum = self.curriculum_loader.validar_integridad()
        if not valido_curriculum:
            problemas.extend(probs_curriculum)
        
        # Validar que existan archivos de contenido
        temas_sin_archivo = 0
        for semestre in self.semestres:
            for materia in semestre.materias:
                for tema_info in materia.temas:
                    if not self.content_loader.existe_archivo(
                        semestre.numero,
                        materia.id,
                        tema_info['archivo']
                    ):
                        temas_sin_archivo += 1
                        problemas.append(
                            f"Archivo no existe: {semestre.numero}/{materia.id}/{tema_info['archivo']}"
                        )
        
        return len(problemas) == 0, problemas
    
    # ==================== UTILIDADES ====================
    
    def info_resumen(self) -> str:
        """
        Genera un resumen completo del sistema.
        
        Returns:
            str: Resumen formateado
        """
        stats = self.get_estadisticas_generales()
        
        lineas = [
            f"\n{'='*70}",
            f"📊 DATA MANAGER - RESUMEN DEL SISTEMA",
            f"{'='*70}",
            f"Estado: {'✅ Inicializado' if self.inicializado else '❌ No inicializado'}",
            f"\n📚 CURRICULUM:",
            f"  - Versión: {stats.get('version', 'N/A')}",
            f"  - Semestres: {stats.get('total_semestres', 0)}",
            f"  - Materias: {stats.get('total_materias', 0)}",
            f"  - Temas: {stats.get('total_temas', 0)}",
            f"  - Créditos totales: {stats.get('total_creditos', 0)}",
            f"\n💾 CACHÉ:",
            f"  - Topics: {stats['cache']['topics_cached']}",
            f"  - Challenges: {stats['cache']['challenges_cached']}",
            f"  - Projects: {stats['cache']['projects_cached']}",
            f"  - Hit rate: {stats['cache']['hit_rate']*100:.1f}%",
            f"\n📈 ESTADÍSTICAS DE USO:",
            f"  - Topics cargados: {stats['cache']['topics_loaded']}",
            f"  - Challenges cargados: {stats['cache']['challenges_loaded']}",
            f"  - Projects cargados: {stats['cache']['projects_loaded']}",
            f"\n{'='*70}\n"
        ]
        
        return "\n".join(lineas)
    
    def __repr__(self) -> str:
        """Representación del DataManager"""
        estado = "✓" if self.inicializado else "✗"
        return f"DataManager({estado}, {len(self.semestres)} semestres, cache: {sum(len(c) for c in self.cache.values())} items)"