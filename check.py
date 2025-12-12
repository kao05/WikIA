#!/usr/bin/env python3
"""
Script de verificación rápida para Wikia Cognitiva
Verifica que todo esté listo para la presentación
"""

import sys
from pathlib import Path
import json

def print_header(text):
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70)

def check_file(path, required=True):
    """Verifica si un archivo existe"""
    p = Path(path)
    exists = p.exists()
    
    status = "✅" if exists else ("❌" if required else "⚠️")
    req_text = "REQUERIDO" if required else "Opcional"
    
    print(f"{status} {path:50} [{req_text}]")
    
    return exists

def check_directory(path, required=True):
    """Verifica si un directorio existe"""
    p = Path(path)
    exists = p.exists() and p.is_dir()
    
    status = "✅" if exists else ("❌" if required else "⚠️")
    req_text = "REQUERIDO" if required else "Opcional"
    
    print(f"{status} {path:50} [{req_text}]")
    
    return exists

def check_dependencies():
    """Verifica las dependencias de Python"""
    print_header("📦 VERIFICANDO DEPENDENCIAS")
    
    required = {
        'PyQt6': 'pyqt6',
        'PyQt6.QtWebEngine': 'pyqt6-webengine',
        'markdown': 'markdown',
        'pygments': 'pygments'
    }
    
    optional = {
        'PyInstaller': 'pyinstaller'
    }
    
    all_good = True
    
    print("\n🔍 Dependencias Requeridas:")
    for module, package in required.items():
        try:
            __import__(module)
            print(f"  ✅ {module:30} instalado")
        except ImportError:
            print(f"  ❌ {module:30} FALTA - instalar con: pip install {package}")
            all_good = False
    
    print("\n🔍 Dependencias Opcionales:")
    for module, package in optional.items():
        try:
            __import__(module)
            print(f"  ✅ {module:30} instalado")
        except ImportError:
            print(f"  ⚠️  {module:30} no instalado (solo para .exe)")
    
    return all_good

def check_structure():
    """Verifica la estructura de archivos"""
    print_header("📁 VERIFICANDO ESTRUCTURA DE ARCHIVOS")
    
    print("\n🔍 Archivos Python Críticos:")
    critical_files = [
        "src/main.py",
        "src/__init__.py",
        "src/core/data_manager.py",
        "src/core/curriculum_loader.py",
        "src/core/content_loader.py",
        "src/models/semester.py",
        "src/models/subject.py",
        "src/models/topic.py",
        "src/models/challenge.py",
        "src/models/project.py",
        "src/ui/main_window.py",
        "src/ui/navigation_panel.py",
        "src/ui/content_viewer.py",
        "src/ui/search_bar.py",
    ]
    
    all_good = True
    for file in critical_files:
        if not check_file(file, required=True):
            all_good = False
    
    print("\n🔍 Directorios Necesarios:")
    critical_dirs = [
        "src/data",
        "src/data/content",
        "src/ui",
        "src/core",
        "src/models",
    ]
    
    for dir in critical_dirs:
        if not check_directory(dir, required=True):
            all_good = False
    
    return all_good

def check_data_files():
    """Verifica archivos de datos"""
    print_header("📚 VERIFICANDO ARCHIVOS DE DATOS")
    
    print("\n🔍 Archivo de Curriculum:")
    curriculum_exists = check_file("src/data/curriculum.json", required=True)
    
    if curriculum_exists:
        try:
            with open("src/data/curriculum.json", 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            semestres = data.get('semestres', [])
            print(f"  ✅ curriculum.json válido")
            print(f"     - {len(semestres)} semestres definidos")
            
            total_materias = sum(len(s.get('materias', [])) for s in semestres)
            print(f"     - {total_materias} materias en total")
            
        except json.JSONDecodeError:
            print(f"  ❌ curriculum.json tiene errores de formato")
            return False
        except Exception as e:
            print(f"  ❌ Error leyendo curriculum.json: {e}")
            return False
    else:
        return False
    
    print("\n🔍 Contenido de Semestres:")
    content_found = False
    for i in range(1, 5):
        sem_dir = f"src/data/content/semestre_{i}"
        if check_directory(sem_dir, required=False):
            content_found = True
            # Contar archivos JSON
            json_files = list(Path(sem_dir).rglob("*.json"))
            if json_files:
                print(f"     └─ {len(json_files)} archivos de contenido")
    
    if not content_found:
        print("  ⚠️  No se encontró contenido de semestres (solo afecta navegación)")
    
    return curriculum_exists

def check_imports():
    """Verifica que los imports estén correctos"""
    print_header("🔍 VERIFICANDO IMPORTS")
    
    main_py_path = Path("src/main.py")
    
    if not main_py_path.exists():
        print("❌ src/main.py no existe")
        return False
    
    content = main_py_path.read_text(encoding='utf-8')
    
    # Buscar imports problemáticos
    problematic = [
        ("from ui.main_window", "from src.ui.main_window"),
        ("from core.", "from src.core."),
        ("from models.", "from src.models."),
    ]
    
    issues_found = False
    
    for wrong, correct in problematic:
        if wrong in content:
            print(f"❌ Import incorrecto encontrado:")
            print(f"   Cambiar: {wrong}")
            print(f"   Por:     {correct}")
            issues_found = True
    
    if not issues_found:
        print("✅ Los imports parecen correctos")
    
    return not issues_found

def test_basic_import():
    """Intenta importar los módulos básicos"""
    print_header("🧪 PROBANDO IMPORTS BÁSICOS")
    
    try:
        print("  Importando DataManager...")
        from src.core.data_manager import DataManager
        print("  ✅ DataManager importado correctamente")
        
        print("  Importando modelos...")
        from src.models.semester import Semester
        from src.models.subject import Subject
        from src.models.topic import Topic
        print("  ✅ Modelos importados correctamente")
        
        print("  Importando UI...")
        from src.ui.main_window import MainWindow
        print("  ✅ UI importada correctamente")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Error de import: {e}")
        print("\n  💡 Posibles soluciones:")
        print("     1. Verifica que estás en el directorio raíz del proyecto")
        print("     2. Verifica que los __init__.py existan")
        print("     3. Ejecuta: python -m src.main")
        return False
    except Exception as e:
        print(f"  ❌ Error inesperado: {e}")
        return False

def main():
    """Función principal"""
    print("\n" + "="*70)
    print("  WIKIA COGNITIVA - VERIFICADOR DE SISTEMA")
    print("  Preparación para presentación")
    print("="*70)
    
    checks = []
    
    # Verificar cada aspecto
    checks.append(("Dependencias", check_dependencies()))
    checks.append(("Estructura", check_structure()))
    checks.append(("Datos", check_data_files()))
    checks.append(("Imports", check_imports()))
    checks.append(("Imports básicos", test_basic_import()))
    
    # Resumen
    print_header("📊 RESUMEN")
    
    passed = sum(1 for _, result in checks if result)
    total = len(checks)
    
    print(f"\nVerificaciones pasadas: {passed}/{total}\n")
    
    for name, result in checks:
        status = "✅" if result else "❌"
        print(f"  {status} {name}")
    
    print("\n" + "="*70)
    
    if passed == total:
        print("\n🎉 ¡SISTEMA LISTO PARA LA PRESENTACIÓN!")
        print("\n✅ Puedes ejecutar:")
        print("   python src/main.py")
        print("\n✅ O crear el ejecutable:")
        print("   python build_exe_simple.py")
    elif passed >= total - 1:
        print("\n⚠️  CASI LISTO - Hay un problema menor")
        print("\n💡 Revisa los errores arriba y corrígelos")
        print("   La mayoría está bien, solo falta un detalle")
    else:
        print("\n❌ REQUIERE ATENCIÓN")
        print("\n🔧 Pasos recomendados:")
        print("   1. Instala dependencias faltantes")
        print("   2. Verifica estructura de archivos")
        print("   3. Ejecuta este script nuevamente")
    
    print("\n" + "="*70 + "\n")
    
    sys.exit(0 if passed == total else 1)

if __name__ == "__main__":
    main()