#!/usr/bin/env python3
"""
Script simplificado para crear el ejecutable de Wikia Cognitiva
"""

import PyInstaller.__main__
import sys
from pathlib import Path

def build_exe():
    """Construye el ejecutable usando PyInstaller"""
    
    print("\n" + "="*70)
    print("  CONSTRUYENDO WIKIA COGNITIVA EJECUTABLE")
    print("="*70 + "\n")
    
    # Configuración básica de PyInstaller
    args = [
        'src/main.py',  # Script principal
        '--name=WikiaCognitiva',  # Nombre del ejecutable
        '--onefile',  # Un solo archivo ejecutable
        '--windowed',  # Sin consola (solo ventana)
        '--icon=NONE',  # Sin icono por ahora
        
        # Incluir datos necesarios
        '--add-data=src/data;data',  # Incluir carpeta de datos
        '--add-data=src/ui/styles;ui/styles',  # Incluir estilos
        
        # Opciones de limpieza
        '--clean',  # Limpiar archivos temporales
        '--noconfirm',  # No pedir confirmación
        
        # Directorio de salida
        '--distpath=dist',
        '--workpath=build',
        '--specpath=build',
    ]
    
    print("📦 Iniciando construcción...")
    print(f"   Archivo principal: src/main.py")
    print(f"   Nombre: WikiaCognitiva.exe")
    print(f"   Modo: Ventana (sin consola)\n")
    
    try:
        # Ejecutar PyInstaller
        PyInstaller.__main__.run(args)
        
        print("\n" + "="*70)
        print("✅ CONSTRUCCIÓN EXITOSA")
        print("="*70)
        print(f"\n📁 El ejecutable está en: dist/WikiaCognitiva.exe")
        print(f"\n💡 Para distribuir:")
        print(f"   1. Copia dist/WikiaCognitiva.exe")
        print(f"   2. Asegúrate de incluir la carpeta 'src/data' junto al .exe")
        print("\n" + "="*70 + "\n")
        
    except Exception as e:
        print("\n" + "="*70)
        print("❌ ERROR EN LA CONSTRUCCIÓN")
        print("="*70)
        print(f"\nError: {e}")
        print("\n💡 Solución:")
        print("   1. Verifica que PyInstaller esté instalado: pip install pyinstaller")
        print("   2. Ejecuta desde el directorio raíz del proyecto")
        print("\n" + "="*70 + "\n")
        sys.exit(1)

if __name__ == "__main__":
    build_exe()
