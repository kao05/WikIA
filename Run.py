#!/usr/bin/env python3
"""
Ejecutor principal de Wikia Cognitiva
Maneja errores comunes y proporciona mensajes útiles
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
        ('PyQt6', 'pip install PyQt6'),
        ('PyQt6.QtWebEngineWidgets', 'pip install PyQt6-WebEngine'),
    ]
    
    missing = []
    
    for module, install_cmd in required:
        try:
            __import__(module)
        except ImportError:
            missing.append((module, install_cmd))
    
    if missing:
        print("\n❌ Faltan dependencias:\n")
        for module, cmd in missing:
            print(f"  • {module}")
            print(f"    Instalar: {cmd}\n")
        
        print("💡 Instala todas las dependencias con:")
        print("   pip install -r requirements.txt\n")
        
        return False
    
    print("✅ Todas las dependencias instaladas\n")
    return True

def check_data_files():
    """Verifica que existan los archivos de datos necesarios"""
    print("🔍 Verificando archivos de datos...")
    
    curriculum_path = root_dir / "src" / "data" / "curriculum.json"
    
    if not curriculum_path.exists():
        print(f"\n❌ No se encontró: {curriculum_path}")
        print("\n💡 Asegúrate de que el archivo curriculum.json existe en:")
        print(f"   {curriculum_path.parent}\n")
        return False
    
    print("✅ Archivos de datos encontrados\n")
    return True

def run_application():
    """Ejecuta la aplicación principal"""
    print("🚀 Iniciando aplicación...\n")
    
    try:
        # Importar la función main
        from src.main import main
        
        # Ejecutar la aplicación
        return main()
        
    except ImportError as e:
        print(f"\n❌ Error de importación: {e}")
        print("\n💡 Posibles soluciones:")
        print("   1. Verifica que estás en el directorio raíz del proyecto")
        print("   2. Verifica que todos los archivos .py existen")
        print("   3. Ejecuta: python check_ready.py para diagnóstico completo\n")
        return 1
        
    except FileNotFoundError as e:
        print(f"\n❌ Archivo no encontrado: {e}")
        print("\n💡 Verifica que existen:")
        print("   • src/data/curriculum.json")
        print("   • src/data/content/ (con contenido de semestres)\n")
        return 1
        
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("\n📝 Detalles del error:")
        import traceback
        traceback.print_exc()
        print("\n💡 Si el error persiste:")
        print("   1. Ejecuta: python check_ready.py")
        print("   2. Revisa los logs arriba para más detalles\n")
        return 1

def main():
    """Función principal"""
    print_banner()
    
    # Verificaciones previas
    if not check_dependencies():
        print("❌ Instala las dependencias antes de continuar")
        sys.exit(1)
    
    if not check_data_files():
        print("❌ Corrige los archivos de datos antes de continuar")
        sys.exit(1)
    
    # Ejecutar aplicación
    try:
        exit_code = run_application()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n👋 Aplicación cerrada por el usuario")
        sys.exit(0)

if __name__ == "__main__":
    main()