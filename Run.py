#!/usr/bin/env python3
"""
Ejecutor principal de Wikia Cognitiva - VERSIÓN CORREGIDA
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def print_banner():
    """Muestra el banner de inicio"""
    print("\n" + "="*70)
    print("  WIKIA COGNITIVA - Plataforma Educativa de IA")
    print("  Licenciatura en Inteligencia Artificial")
    print("="*70 + "\n")

def check_dependencies():
    """Verifica que las dependencias estén instaladas"""
    print("🔍 Verificando dependencias...")
    
    required = [
        'PyQt6',
        'PyQt6.QtWebEngineWidgets',
    ]
    
    missing = []
    
    for module in required:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        print("\n❌ Faltan dependencias:\n")
        for module in missing:
            print(f"  • {module}")
        
        print("\n💡 Instala con:")
        print("   pip install -r requirements.txt\n")
        
        return False
    
    print("✅ Todas las dependencias instaladas\n")
    return True

def check_data_files():
    """Verifica archivos de datos"""
    print("🔍 Verificando archivos de datos...")
    
    curriculum_path = root_dir / "src" / "data" / "curriculum.json"
    
    if not curriculum_path.exists():
        print(f"\n❌ No se encontró: {curriculum_path}")
        return False
    
    print("✅ Archivos de datos encontrados\n")
    return True

def run_application():
    """Ejecuta la aplicación"""
    print("🚀 Iniciando aplicación...\n")
    
    try:
        # Importar desde src.main
        from src.main import main
        
        return main()
        
    except ImportError as e:
        print(f"\n❌ Error de importación: {e}")
        print("\n💡 Soluciones:")
        print("   1. Verifica que estás en el directorio raíz")
        print("   2. Ejecuta: python Run.py\n")
        return 1
        
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return 1

def main():
    """Función principal"""
    print_banner()
    
    # Verificaciones
    if not check_dependencies():
        print("❌ Instala las dependencias primero")
        input("\nPresiona Enter para salir...")
        sys.exit(1)
    
    if not check_data_files():
        print("❌ Faltan archivos de datos")
        input("\nPresiona Enter para salir...")
        sys.exit(1)
    
    # Ejecutar
    try:
        exit_code = run_application()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n👋 Aplicación cerrada")
        sys.exit(0)

if __name__ == "__main__":
    main()
