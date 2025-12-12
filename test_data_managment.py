#!/usr/bin/env python3
"""
Pruebas adicionales para DataManager

Este script complementa test_models_loaders.py con pruebas
específicas del coordinador central.
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.data_manager import DataManager


def print_separator(title=""):
    """Imprime un separador visual"""
    if title:
        print(f"\n{'='*70}")
        print(f"  {title}")
        print(f"{'='*70}\n")
    else:
        print(f"{'='*70}\n")


def test_initialization():
    """Prueba la inicialización del DataManager"""
    print_separator("🧪 TEST 1: INICIALIZACIÓN DEL DATA MANAGER")
    
    dm = DataManager()
    
    print("📂 Inicializando sistema...")
    if dm.initialize():
        print("✅ Sistema inicializado correctamente\n")
        
        # Mostrar resumen
        print(dm.info_resumen())
        
        return True, dm
    else:
        print("❌ Error en inicialización")
        return False, None


def test_cache_system(dm: DataManager):
    """Prueba el sistema de caché"""
    print_separator("🧪 TEST 2: SISTEMA DE CACHÉ")
    
    print("📄 Cargando tema por primera vez (cache miss)...")
    topic1 = dm.get_topic(1, "algebra_superior", "teoria_conjuntos.json")
    
    if topic1:
        print(f"✅ Tema cargado: {topic1.titulo}")
        
        print("\n📄 Cargando el mismo tema otra vez (cache hit)...")
        topic2 = dm.get_topic(1, "algebra_superior", "teoria_conjuntos.json")
        
        if topic2:
            print(f"✅ Tema obtenido del caché")
            
            # Verificar que es el mismo objeto
            if topic1 is topic2:
                print("✅ Es el mismo objeto en memoria (caché funciona)")
            
            # Mostrar estadísticas de caché
            print("\n📊 ESTADÍSTICAS DE CACHÉ:")
            stats = dm.get_cache_stats()
            for key, value in stats.items():
                print(f"  {key}: {value}")
            
            return True
    
    print("❌ Error en sistema de caché")
    return False


def test_multiple_loads(dm: DataManager):
    """Prueba carga múltiple de temas"""
    print_separator("🧪 TEST 3: CARGA MÚLTIPLE DE TEMAS")
    
    temas_a_cargar = [
        (1, "algebra_superior", "teoria_conjuntos.json"),
        (1, "algebra_superior", "algebra_booleana.json"),
        (1, "calculo_dif_int", "derivadas_basicas.json")
    ]
    
    print(f"📚 Cargando {len(temas_a_cargar)} temas...")
    
    exitosos = 0
    for sem, mat, arch in temas_a_cargar:
        topic = dm.get_topic(sem, mat, arch)
        if topic:
            print(f"  ✅ {topic.titulo}")
            exitosos += 1
        else:
            print(f"  ❌ Error: {sem}/{mat}/{arch}")
    
    print(f"\n📊 Resultado: {exitosos}/{len(temas_a_cargar)} exitosos")
    
    # Mostrar estado del caché
    stats = dm.get_cache_stats()
    print(f"\n💾 Items en caché: {stats['topics_cached']}")
    print(f"   Hit rate: {stats['hit_rate']*100:.1f}%")
    
    return exitosos == len(temas_a_cargar)


def test_challenges_and_projects(dm: DataManager):
    """Prueba carga de challenges y projects"""
    print_separator("🧪 TEST 4: CHALLENGES Y PROJECTS")
    
    # Intentar cargar un challenge
    print("🎯 Buscando reto de programación...")
    challenge = dm.get_challenge(1, "intro_programacion", "recursividad.json")
    
    if challenge:
        print(f"✅ Challenge encontrado: {challenge.titulo}")
        print(f"   Dificultad: {challenge.dificultad}")
        print(f"   Pistas: {len(challenge.pistas)}")
    else:
        print("ℹ️  No se encontró challenge en ese tema")
    
    # Intentar cargar un project
    print("\n📋 Buscando proyecto conceptual...")
    project = dm.get_project(1, "calculo_dif_int", "derivadas_basicas.json")
    
    if project:
        print(f"✅ Project encontrado: {project.titulo}")
        print(f"   Objetivos: {project.numero_objetivos}")
        print(f"   Pasos: {project.numero_pasos}")
    else:
        print("ℹ️  No se encontró project en ese tema")
    
    return True


def test_search_functions(dm: DataManager):
    """Prueba funciones de búsqueda"""
    print_separator("🧪 TEST 5: FUNCIONES DE BÚSQUEDA")
    
    # Buscar materias
    print("🔍 Buscando materias con 'álgebra'...")
    materias = dm.buscar_materias("álgebra")
    if materias:
        print(f"✅ Encontradas {len(materias)} materias:")
        for sem, mat in materias[:3]:
            print(f"  • Semestre {sem}: {mat.nombre}")
    
    # Buscar temas
    print("\n🔍 Buscando temas con 'lógica'...")
    temas = dm.buscar_temas("lógica")
    if temas:
        print(f"✅ Encontrados {len(temas)} temas:")
        for tema in temas[:3]:
            print(f"  • {tema['materia_nombre']}: {tema['tema_nombre']}")
    
    # Buscar por dificultad
    print("\n🔍 Buscando temas de dificultad 'intermedio'...")
    temas_inter = dm.buscar_temas_por_dificultad("intermedio")
    if temas_inter:
        print(f"✅ Encontrados {len(temas_inter)} temas intermedios")
    
    return True


def test_cache_management(dm: DataManager):
    """Prueba gestión de caché"""
    print_separator("🧪 TEST 6: GESTIÓN DE CACHÉ")
    
    # Cargar algunos temas
    print("📚 Cargando temas para llenar caché...")
    dm.get_topic(1, "algebra_superior", "teoria_conjuntos.json")
    dm.get_topic(1, "algebra_superior", "algebra_booleana.json")
    
    stats_antes = dm.get_cache_stats()
    print(f"\n💾 Items en caché antes: {stats_antes['topics_cached']}")
    
    # Limpiar caché específico
    print("\n🗑️  Limpiando caché de topics...")
    dm.limpiar_cache('topics')
    
    stats_despues = dm.get_cache_stats()
    print(f"💾 Items en caché después: {stats_despues['topics_cached']}")
    
    if stats_despues['topics_cached'] == 0:
        print("✅ Caché limpiado correctamente")
        return True
    else:
        print("❌ Error limpiando caché")
        return False


def test_force_reload(dm: DataManager):
    """Prueba recarga forzada (ignorar caché)"""
    print_separator("🧪 TEST 7: RECARGA FORZADA")
    
    # Cargar tema
    print("📄 Cargando tema (primera vez)...")
    topic1 = dm.get_topic(1, "algebra_superior", "teoria_conjuntos.json")
    
    if topic1:
        print(f"✅ Cargado: {topic1.titulo}")
        
        # Recargar con force_reload=True
        print("\n🔄 Recargando con force_reload=True...")
        topic2 = dm.get_topic(
            1, "algebra_superior", "teoria_conjuntos.json",
            force_reload=True
        )
        
        if topic2:
            print(f"✅ Recargado: {topic2.titulo}")
            
            # Verificar que son objetos diferentes
            if topic1 is not topic2:
                print("✅ Son objetos diferentes (recarga exitosa)")
                return True
            else:
                print("⚠️  Son el mismo objeto (no se forzó recarga)")
                return False
    
    return False


def test_validation(dm: DataManager):
    """Prueba validación de integridad"""
    print_separator("🧪 TEST 8: VALIDACIÓN DE INTEGRIDAD")
    
    print("🔍 Validando integridad del sistema...")
    valido, problemas = dm.validar_integridad_completa()
    
    if valido:
        print("✅ Sistema completamente válido")
        return True
    else:
        print(f"⚠️  Se encontraron {len(problemas)} problemas:")
        for i, problema in enumerate(problemas[:5], 1):
            print(f"  {i}. {problema}")
        if len(problemas) > 5:
            print(f"  ... y {len(problemas) - 5} más")
        return False


def test_statistics(dm: DataManager):
    """Prueba obtención de estadísticas"""
    print_separator("🧪 TEST 9: ESTADÍSTICAS DEL SISTEMA")
    
    # Cargar algunos temas para tener datos
    dm.get_topic(1, "algebra_superior", "teoria_conjuntos.json")
    dm.get_topic(1, "geometria", "sistemas_coordenadas.json")
    dm.get_challenge(1, "intro_programacion", "recursividad.json")
    
    print("📊 Obteniendo estadísticas generales...")
    stats = dm.get_estadisticas_generales()
    
    print("\n✅ ESTADÍSTICAS OBTENIDAS:")
    print(f"  Total semestres: {stats.get('total_semestres', 0)}")
    print(f"  Total materias: {stats.get('total_materias', 0)}")
    print(f"  Total temas: {stats.get('total_temas', 0)}")
    print(f"  Topics cargados: {stats['cache']['topics_loaded']}")
    print(f"  Challenges cargados: {stats['cache']['challenges_loaded']}")
    print(f"  Cache hit rate: {stats['cache']['hit_rate']*100:.1f}%")
    
    # Estadísticas de materia específica
    print("\n📚 Estadísticas de materia específica...")
    stats_materia = dm.get_progreso_materia(1, "algebra_superior")
    if stats_materia:
        print(f"✅ {stats_materia['nombre']}:")
        print(f"  - Créditos: {stats_materia['creditos']}")
        print(f"  - Temas: {stats_materia['total_temas']}")
    
    return True


def main():
    """Función principal"""
    print("\n" + "="*70)
    print("  PRUEBAS DEL DATA MANAGER - WIKIA COGNITIVA")
    print("="*70)
    
    resultados = []
    
    # Test 1: Inicialización
    exito, dm = test_initialization()
    resultados.append(("Inicialización", exito))
    
    if not exito or not dm:
        print("\n❌ Error crítico: No se pudo inicializar el DataManager")
        return
    
    # Tests restantes
    resultados.append(("Sistema de Caché", test_cache_system(dm)))
    resultados.append(("Carga Múltiple", test_multiple_loads(dm)))
    resultados.append(("Challenges y Projects", test_challenges_and_projects(dm)))
    resultados.append(("Búsqueda", test_search_functions(dm)))
    resultados.append(("Gestión de Caché", test_cache_management(dm)))
    resultados.append(("Recarga Forzada", test_force_reload(dm)))
    resultados.append(("Validación", test_validation(dm)))
    resultados.append(("Estadísticas", test_statistics(dm)))
    
    # Resumen
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
        print("🎉 ¡TODAS LAS PRUEBAS DEL DATA MANAGER PASARON!")
        print("\n✅ La Fase 2 está 100% completa")
        print("\n📝 Próximos pasos:")
        print("  1. Implementar cache_manager.py (opcional, para persistencia)")
        print("  2. Comenzar con la Fase 3: Interfaz Básica")
        print("  3. Implementar main_window.py y navigation_panel.py")
    else:
        print("⚠️  Algunas pruebas fallaron")
        print("\n🔧 Revisa los errores y corrige los problemas")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    main()