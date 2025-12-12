#!/usr/bin/env python3
"""
Script de prueba para modelos y loaders

Este script prueba toda la Fase 2:
- Modelos (Semester, Subject, Topic, Challenge, Project)
- Loaders (CurriculumLoader, ContentLoader)
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.curriculum_loader import CurriculumLoader
from src.core.content_loader import ContentLoader


def print_separator(title=""):
    """Imprime un separador visual"""
    if title:
        print(f"\n{'='*70}")
        print(f"  {title}")
        print(f"{'='*70}\n")
    else:
        print(f"{'='*70}\n")


def test_curriculum_loader():
    """Prueba el CurriculumLoader"""
    print_separator("🧪 TEST 1: CURRICULUM LOADER")
    
    # Inicializar
    curriculum_path = "src/data/curriculum.json"
    loader = CurriculumLoader(curriculum_path)
    
    # Cargar
    print("📂 Cargando curriculum...")
    if loader.load():
        print("✅ Curriculum cargado exitosamente\n")
        
        # Estadísticas
        stats = loader.get_estadisticas()
        print("📊 ESTADÍSTICAS:")
        print(f"  - Versión: {stats['version']}")
        print(f"  - Última actualización: {stats['ultima_actualizacion']}")
        print(f"  - Total semestres: {stats['total_semestres']}")
        print(f"  - Total materias: {stats['total_materias']}")
        print(f"  - Total créditos: {stats['total_creditos']}")
        print(f"  - Total temas: {stats['total_temas']}")
        
        # Listar semestres
        print("\n📚 SEMESTRES CARGADOS:")
        for semestre in loader.get_semestres():
            print(f"  {semestre}")
        
        # Validar integridad
        print("\n🔍 VALIDANDO INTEGRIDAD...")
        valido, problemas = loader.validar_integridad()
        if valido:
            print("✅ Integridad verificada")
        else:
            print("⚠️  Problemas encontrados:")
            for problema in problemas:
                print(f"    - {problema}")
        
        return True
    else:
        print("❌ Error cargando curriculum")
        return False


def test_semestre_access(loader):
    """Prueba acceso a semestres"""
    print_separator("🧪 TEST 2: ACCESO A SEMESTRES")
    
    # Obtener semestre 1
    print("📖 Obteniendo Semestre 1...")
    semestre = loader.get_semestre(1)
    
    if semestre:
        print(f"✅ {semestre}")
        print(f"   Total materias: {semestre.total_materias}")
        print(f"   Total créditos: {semestre.total_creditos}")
        print(f"   Total temas: {semestre.total_temas}")
        
        print("\n📚 Materias del semestre:")
        for i, materia in enumerate(semestre.materias, 1):
            print(f"  {i}. {materia.nombre} ({materia.creditos} créditos, {materia.total_temas} temas)")
        
        return True
    else:
        print("❌ No se pudo obtener el semestre")
        return False


def test_materia_access(loader):
    """Prueba acceso a materias"""
    print_separator("🧪 TEST 3: ACCESO A MATERIAS")
    
    # Obtener una materia específica
    print("📖 Obteniendo materia 'Álgebra Superior' del Semestre 1...")
    materia = loader.get_materia(1, "algebra_superior")
    
    if materia:
        print(f"✅ {materia}")
        print(f"\n📋 INFORMACIÓN DETALLADA:")
        print(f"  ID: {materia.id}")
        print(f"  Nombre: {materia.nombre}")
        print(f"  Créditos: {materia.creditos}")
        print(f"  Total temas: {materia.total_temas}")
        
        print(f"\n📝 Primeros 5 temas:")
        for i, tema_info in enumerate(materia.temas[:5], 1):
            print(f"  {i}. {tema_info['nombre']}")
            print(f"     ID: {tema_info['id']}")
            print(f"     Archivo: {tema_info['archivo']}")
        
        if len(materia.temas) > 5:
            print(f"  ... y {len(materia.temas) - 5} temas más")
        
        return True
    else:
        print("❌ No se pudo obtener la materia")
        return False


def test_content_loader():
    """Prueba el ContentLoader"""
    print_separator("🧪 TEST 4: CONTENT LOADER")
    
    # Inicializar
    content_path = "src/data/content"
    loader = ContentLoader(content_path)
    
    print(f"📂 ContentLoader inicializado con base: {loader.base_path}\n")
    
    # Listar temas disponibles
    print("📚 Listando temas de 'Álgebra Superior' (Semestre 1)...")
    temas = loader.listar_temas_disponibles(1, "algebra_superior")
    
    if temas:
        print(f"✅ Encontrados {len(temas)} temas:")
        for i, tema in enumerate(temas[:5], 1):
            print(f"  {i}. {tema}")
        if len(temas) > 5:
            print(f"  ... y {len(temas) - 5} temas más")
        return True, loader
    else:
        print("⚠️  No se encontraron temas")
        return False, loader


def test_topic_loading(content_loader):
    """Prueba carga de un tema completo"""
    print_separator("🧪 TEST 5: CARGA DE TEMA COMPLETO")
    
    # Cargar un tema
    print("📄 Cargando tema: 'Teoría de Conjuntos'...")
    
    try:
        topic = content_loader.load_topic(
            semestre_num=1,
            materia_id="algebra_superior",
            tema_archivo="teoria_conjuntos.json"
        )
        
        print(f"✅ Tema cargado: {topic.titulo}\n")
        
        print("📋 METADATOS:")
        print(f"  ID: {topic.id}")
        print(f"  Título: {topic.titulo}")
        print(f"  Materia: {topic.materia}")
        print(f"  Semestre: {topic.semestre}")
        print(f"  Dificultad: {topic.dificultad}")
        print(f"  Tiempo de estudio: {topic.tiempo_estudio}")
        
        print("\n📘 CONCEPTOS CLAVE:")
        contenido = topic.get_contenido_conceptos()
        print(f"  {contenido[:150]}...")
        
        print("\n🎯 PUNTOS CLAVE:")
        for punto in topic.get_puntos_clave()[:3]:
            print(f"  • {punto}")
        
        print("\n🏭 APLICACIONES EN INDUSTRIA:")
        sectores = topic.get_sectores_industria()
        for sector in sectores[:2]:
            print(f"  • {sector.get('nombre', 'N/A')}: {sector.get('descripcion', 'N/A')[:60]}...")
        
        print("\n💼 ROLES LABORALES:")
        roles = topic.get_roles()
        for rol in roles[:3]:
            print(f"  • {rol.get('nombre', 'N/A')} - {rol.get('nivel_importancia', 'N/A')}")
        
        print(f"\n🎮 TIPO DE RETO: {topic.tipo_reto}")
        print(f"  Título: {topic.titulo_reto}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error cargando tema: {e}")
        return False


def test_challenge_loading(content_loader):
    """Prueba carga de un reto de programación"""
    print_separator("🧪 TEST 6: CARGA DE RETO DE PROGRAMACIÓN")
    
    print("🎯 Cargando reto: 'Recursividad'...")
    
    try:
        challenge = content_loader.load_challenge(
            semestre_num=1,
            materia_id="intro_programacion",
            tema_archivo="recursividad.json"
        )
        
        if challenge:
            print(f"✅ Challenge cargado: {challenge.titulo}\n")
            
            print("📋 INFORMACIÓN:")
            print(f"  Tipo: {challenge.tipo}")
            print(f"  Dificultad: {challenge.dificultad}")
            print(f"  Tiene código inicial: {'Sí' if challenge.tiene_codigo_inicial else 'No'}")
            print(f"  Tiene solución: {'Sí' if challenge.tiene_solucion else 'No'}")
            print(f"  Número de pistas: {challenge.numero_pistas}")
            print(f"  Casos de prueba: {challenge.numero_casos_prueba}")
            
            if challenge.tiene_pistas:
                print("\n💡 PISTAS:")
                for i, pista in enumerate(challenge.get_todas_pistas()[:3], 1):
                    print(f"  {i}. {pista}")
            
            if challenge.tiene_codigo_inicial:
                print("\n💻 CÓDIGO INICIAL:")
                codigo = challenge.codigo_inicial.split('\n')[:5]
                for linea in codigo:
                    print(f"  {linea}")
                print("  ...")
            
            return True
        else:
            print("ℹ️  El tema no tiene reto de programación")
            return False
            
    except Exception as e:
        print(f"❌ Error cargando challenge: {e}")
        return False


def test_busqueda(curriculum_loader):
    """Prueba funcionalidades de búsqueda"""
    print_separator("🧪 TEST 7: BÚSQUEDA DE CONTENIDO")
    
    # Buscar materias
    print("🔍 Buscando materias con 'álgebra'...")
    resultados_materias = curriculum_loader.buscar_materias("álgebra")
    
    if resultados_materias:
        print(f"✅ Encontradas {len(resultados_materias)} materias:")
        for sem_num, materia in resultados_materias[:3]:
            print(f"  • Semestre {sem_num}: {materia.nombre}")
    
    # Buscar temas
    print("\n🔍 Buscando temas con 'recursividad'...")
    resultados_temas = curriculum_loader.buscar_temas("recursividad")
    
    if resultados_temas:
        print(f"✅ Encontrados {len(resultados_temas)} temas:")
        for tema in resultados_temas:
            print(f"  • {tema['semestre']}.{tema['materia_nombre']}: {tema['tema_nombre']}")
    
    return True


def test_validacion(content_loader):
    """Prueba validación de temas"""
    print_separator("🧪 TEST 8: VALIDACIÓN DE TEMAS")
    
    print("🔍 Validando tema: 'Teoría de Conjuntos'...")
    
    valido, errores = content_loader.validar_tema(
        semestre_num=1,
        materia_id="algebra_superior",
        tema_archivo="teoria_conjuntos.json"
    )
    
    if valido:
        print("✅ Tema válido")
    else:
        print(f"⚠️  Problemas encontrados ({len(errores)}):")
        for error in errores:
            print(f"  • {error}")
    
    return True


def main():
    """Función principal que ejecuta todas las pruebas"""
    print("\n" + "="*70)
    print("  PRUEBAS DE MODELOS Y LOADERS - WIKIA COGNITIVA")
    print("="*70)
    
    resultados = []
    
    # Test 1: Curriculum Loader
    resultado = test_curriculum_loader()
    resultados.append(("Curriculum Loader", resultado))
    
    if not resultado:
        print("\n❌ Error crítico: No se pudo cargar el curriculum")
        print("   Verifica que exista: src/data/curriculum.json")
        return
    
    # Crear instancia de curriculum loader para otros tests
    curriculum_loader = CurriculumLoader("src/data/curriculum.json")
    curriculum_loader.load()
    
    # Test 2: Acceso a Semestres
    resultado = test_semestre_access(curriculum_loader)
    resultados.append(("Acceso a Semestres", resultado))
    
    # Test 3: Acceso a Materias
    resultado = test_materia_access(curriculum_loader)
    resultados.append(("Acceso a Materias", resultado))
    
    # Test 4: Content Loader
    resultado, content_loader = test_content_loader()
    resultados.append(("Content Loader", resultado))
    
    if not resultado:
        print("\n⚠️  Content Loader no pudo listar temas")
        print("   Verifica que existan archivos en: src/data/content/")
    else:
        # Test 5: Carga de Tema
        resultado = test_topic_loading(content_loader)
        resultados.append(("Carga de Tema", resultado))
        
        # Test 6: Carga de Challenge
        resultado = test_challenge_loading(content_loader)
        resultados.append(("Carga de Challenge", resultado))
        
        # Test 7: Búsqueda
        resultado = test_busqueda(curriculum_loader)
        resultados.append(("Búsqueda", resultado))
        
        # Test 8: Validación
        resultado = test_validacion(content_loader)
        resultados.append(("Validación", resultado))
    
    # Resumen final
    print_separator("📊 RESUMEN DE PRUEBAS")
    
    exitosos = sum(1 for _, r in resultados if r)
    total = len(resultados)
    
    print(f"Tests ejecutados: {total}")
    print(f"Tests exitosos: {exitosos}")
    print(f"Tests fallidos: {total - exitosos}\n")
    
    for nombre, resultado in resultados:
        estado = "✅" if resultado else "❌"
        print(f"  {estado} {nombre}")
    
    print()
    
    if exitosos == total:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("\n✅ La Fase 2 está completa y funcional")
        print("\n📝 Próximos pasos:")
        print("  1. Implementar data_manager.py (coordinador)")
        print("  2. Implementar cache_manager.py")
        print("  3. Comenzar con la interfaz (Fase 3)")
    else:
        print("⚠️  Algunas pruebas fallaron")
        print("\n🔧 Revisa los errores anteriores y corrige los problemas")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()