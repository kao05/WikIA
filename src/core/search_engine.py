"""
Motor de Búsqueda para Wikia Cognitiva

Implementa búsqueda avanzada de temas, materias y contenido
con soporte para búsqueda difusa y filtros múltiples.
"""

from typing import List, Dict, Any, Optional
import logging
from difflib import SequenceMatcher

from ..core.data_manager import DataManager


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SearchEngine:
    """
    Motor de búsqueda para el contenido de Wikia Cognitiva.
    
    Características:
    - Búsqueda en títulos, descripciones y contenido
    - Búsqueda difusa (tolerante a errores tipográficos)
    - Filtros por semestre, materia, dificultad
    - Ranking de resultados por relevancia
    
    Attributes:
        data_manager: Instancia del DataManager
        min_similarity: Umbral mínimo de similitud (0.0 - 1.0)
    """
    
    def __init__(self, data_manager: DataManager, min_similarity: float = 0.6):
        """
        Inicializa el motor de búsqueda.
        
        Args:
            data_manager: DataManager con datos cargados
            min_similarity: Umbral mínimo de similitud para búsqueda difusa
        """
        self.dm = data_manager
        self.min_similarity = min_similarity
        logger.info("SearchEngine inicializado")
    
    def search(
        self,
        query: str,
        semestre: Optional[int] = None,
        materia_id: Optional[str] = None,
        dificultad: Optional[str] = None,
        tipo_reto: Optional[str] = None,
        max_results: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Busca temas en todo el curriculum.
        
        Args:
            query: Término de búsqueda
            semestre: Filtrar por semestre (1-4)
            materia_id: Filtrar por ID de materia
            dificultad: Filtrar por dificultad ('basico', 'intermedio', 'avanzado')
            tipo_reto: Filtrar por tipo ('programacion' o 'conceptual')
            max_results: Número máximo de resultados
        
        Returns:
            Lista de diccionarios con resultados ordenados por relevancia
        """
        if not query or len(query.strip()) < 2:
            logger.warning("Query muy corto o vacío")
            return []
        
        query = query.lower().strip()
        logger.info(f"Buscando: '{query}'")
        
        resultados = []
        
        # Iterar por todos los semestres
        for sem in self.dm.get_semestres():
            # Aplicar filtro de semestre
            if semestre and sem.numero != semestre:
                continue
            
            # Iterar por todas las materias
            for materia in sem.materias:
                # Aplicar filtro de materia
                if materia_id and materia.id != materia_id:
                    continue
                
                # Iterar por todos los temas
                for tema_info in materia.temas:
                    try:
                        # Calcular relevancia del tema
                        relevancia = self._calcular_relevancia(
                            query,
                            tema_info,
                            materia.nombre
                        )
                        
                        if relevancia > 0:
                            # Cargar metadatos para filtros adicionales
                            metadatos = self.dm.get_metadatos_tema(
                                sem.numero,
                                materia.id,
                                tema_info['archivo']
                            )
                            
                            # Aplicar filtros adicionales
                            if dificultad and metadatos:
                                if metadatos.get('dificultad') != dificultad:
                                    continue
                            
                            # Agregar resultado
                            resultado = {
                                'relevancia': relevancia,
                                'semestre': sem.numero,
                                'semestre_nombre': sem.nombre,
                                'materia_id': materia.id,
                                'materia_nombre': materia.nombre,
                                'tema_id': tema_info['id'],
                                'tema_nombre': tema_info['nombre'],
                                'archivo': tema_info['archivo'],
                                'dificultad': metadatos.get('dificultad', 'no especificada') if metadatos else 'desconocida'
                            }
                            
                            # Filtro de tipo de reto (requiere cargar tema completo)
                            if tipo_reto:
                                topic = self.dm.get_topic(
                                    sem.numero,
                                    materia.id,
                                    tema_info['archivo']
                                )
                                if topic and topic.tipo_reto != tipo_reto:
                                    continue
                                resultado['tipo_reto'] = topic.tipo_reto if topic else 'desconocido'
                            
                            resultados.append(resultado)
                    
                    except Exception as e:
                        logger.error(f"Error procesando tema {tema_info.get('id')}: {e}")
                        continue
        
        # Ordenar por relevancia (mayor primero)
        resultados.sort(key=lambda x: x['relevancia'], reverse=True)
        
        # Limitar resultados
        resultados = resultados[:max_results]
        
        logger.info(f"Encontrados {len(resultados)} resultados para '{query}'")
        
        return resultados
    
    def _calcular_relevancia(
        self,
        query: str,
        tema_info: Dict[str, str],
        materia_nombre: str
    ) -> float:
        """
        Calcula la relevancia de un tema para una query.
        
        Args:
            query: Término de búsqueda (ya en minúsculas)
            tema_info: Diccionario con info del tema
            materia_nombre: Nombre de la materia
        
        Returns:
            float: Score de relevancia (0.0 - 10.0)
        """
        score = 0.0
        
        tema_nombre = tema_info['nombre'].lower()
        tema_id = tema_info['id'].lower()
        materia_lower = materia_nombre.lower()
        
        # 1. Coincidencia exacta en nombre del tema (peso alto)
        if query in tema_nombre:
            score += 10.0
            # Bonus si es al inicio
            if tema_nombre.startswith(query):
                score += 2.0
        
        # 2. Coincidencia exacta en ID del tema
        if query in tema_id:
            score += 8.0
        
        # 3. Coincidencia en nombre de materia
        if query in materia_lower:
            score += 5.0
        
        # 4. Búsqueda difusa (similitud de strings)
        similarity_nombre = self._similarity(query, tema_nombre)
        if similarity_nombre >= self.min_similarity:
            score += similarity_nombre * 7.0
        
        similarity_id = self._similarity(query, tema_id)
        if similarity_id >= self.min_similarity:
            score += similarity_id * 5.0
        
        # 5. Coincidencia de palabras individuales
        query_words = query.split()
        tema_words = tema_nombre.split()
        
        for q_word in query_words:
            if len(q_word) < 3:  # Ignorar palabras muy cortas
                continue
            for t_word in tema_words:
                if q_word in t_word or t_word in q_word:
                    score += 3.0
                    break
        
        return score
    
    def _similarity(self, a: str, b: str) -> float:
        """
        Calcula similitud entre dos strings.
        
        Args:
            a: String 1
            b: String 2
        
        Returns:
            float: Similitud (0.0 - 1.0)
        """
        return SequenceMatcher(None, a, b).ratio()
    
    def search_by_keywords(
        self,
        keywords: List[str],
        operator: str = 'OR'
    ) -> List[Dict[str, Any]]:
        """
        Busca temas que coincidan con múltiples keywords.
        
        Args:
            keywords: Lista de términos a buscar
            operator: 'OR' (cualquier keyword) o 'AND' (todas las keywords)
        
        Returns:
            Lista de resultados
        """
        if not keywords:
            return []
        
        if operator == 'OR':
            # Buscar con cada keyword y combinar resultados
            all_results = {}
            
            for keyword in keywords:
                results = self.search(keyword)
                for result in results:
                    key = f"{result['semestre']}_{result['materia_id']}_{result['archivo']}"
                    if key in all_results:
                        # Combinar relevancia
                        all_results[key]['relevancia'] += result['relevancia']
                    else:
                        all_results[key] = result
            
            # Convertir a lista y ordenar
            final_results = list(all_results.values())
            final_results.sort(key=lambda x: x['relevancia'], reverse=True)
            
            return final_results
        
        elif operator == 'AND':
            # Buscar con primera keyword
            results = self.search(keywords[0])
            
            # Filtrar que contengan todas las demás keywords
            for keyword in keywords[1:]:
                results = [
                    r for r in results
                    if keyword.lower() in r['tema_nombre'].lower() or
                       keyword.lower() in r['materia_nombre'].lower()
                ]
            
            return results
        
        else:
            logger.error(f"Operador desconocido: {operator}")
            return []
    
    def get_suggestions(self, partial_query: str, max_suggestions: int = 5) -> List[str]:
        """
        Obtiene sugerencias de autocompletado.
        
        Args:
            partial_query: Query parcial
            max_suggestions: Número máximo de sugerencias
        
        Returns:
            Lista de sugerencias
        """
        if len(partial_query) < 2:
            return []
        
        partial_lower = partial_query.lower()
        suggestions = set()
        
        for sem in self.dm.get_semestres():
            for materia in sem.materias:
                # Sugerir nombre de materia
                if partial_lower in materia.nombre.lower():
                    suggestions.add(materia.nombre)
                
                # Sugerir nombres de temas
                for tema_info in materia.temas:
                    if partial_lower in tema_info['nombre'].lower():
                        suggestions.add(tema_info['nombre'])
                    
                    if len(suggestions) >= max_suggestions * 2:
                        break
                
                if len(suggestions) >= max_suggestions * 2:
                    break
        
        # Convertir a lista y ordenar por similitud
        suggestions_list = list(suggestions)
        suggestions_list.sort(
            key=lambda x: self._similarity(partial_lower, x.lower()),
            reverse=True
        )
        
        return suggestions_list[:max_suggestions]
    
    def search_by_difficulty(self, dificultad: str) -> List[Dict[str, Any]]:
        """
        Busca todos los temas de una dificultad específica.
        
        Args:
            dificultad: 'basico', 'intermedio', o 'avanzado'
        
        Returns:
            Lista de temas con esa dificultad
        """
        return self.dm.buscar_temas_por_dificultad(dificultad)
    
    def search_challenges(self) -> List[Dict[str, Any]]:
        """
        Encuentra todos los retos de programación.
        
        Returns:
            Lista de retos de programación
        """
        return self.dm.buscar_retos_programacion()
    
    def get_related_topics(
        self,
        semestre_num: int,
        materia_id: str,
        tema_archivo: str
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Obtiene temas relacionados (prerequisitos y siguientes).
        
        Args:
            semestre_num: Número de semestre
            materia_id: ID de materia
            tema_archivo: Archivo del tema
        
        Returns:
            Dict con 'prerequisitos' y 'siguientes'
        """
        try:
            topic = self.dm.get_topic(semestre_num, materia_id, tema_archivo)
            
            if not topic:
                return {'prerequisitos': [], 'siguientes': []}
            
            prerequisitos = topic.get_prerequisitos()
            siguientes = topic.get_temas_siguientes()
            
            return {
                'prerequisitos': prerequisitos,
                'siguientes': siguientes
            }
        
        except Exception as e:
            logger.error(f"Error obteniendo temas relacionados: {e}")
            return {'prerequisitos': [], 'siguientes': []}
