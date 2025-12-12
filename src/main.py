#!/usr/bin/env python3
"""
Punto de entrada principal de Wikia Cognitiva
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

# IMPORTANTE: Agregar directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

# Ahora importar con rutas correctas
from src.ui.main_window import MainWindow


def setup_application():
    """Configura la aplicación Qt"""
    app = QApplication(sys.argv)
    
    app.setApplicationName("Wikia Cognitiva")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Wikia Cognitiva")
    
    app.setStyle('Fusion')
    
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    return app


def show_error_dialog(title: str, message: str):
    """Muestra un diálogo de error"""
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Critical)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg_box.exec()


def main():
    """Función principal"""
    print("\n" + "="*70)
    print("  WIKIA COGNITIVA - Plataforma Educativa de IA")
    print("="*70 + "\n")
    
    try:
        print("✓ Inicializando aplicación...")
        app = setup_application()
        
        print("✓ Creando ventana principal...")
        window = MainWindow()
        
        if not window.is_initialized():
            show_error_dialog(
                "Error de Inicialización",
                "No se pudo inicializar la aplicación.\n\n"
                "Verifica que:\n"
                "1. El archivo curriculum.json existe en src/data/\n"
                "2. Los archivos de contenido existen en src/data/content/"
            )
            return 1
        
        print("✓ Mostrando ventana...")
        window.show()
        
        print("\n✅ ¡Aplicación iniciada correctamente!")
        print("="*70 + "\n")
        
        return app.exec()
    
    except Exception as e:
        print(f"\n❌ Error fatal: {str(e)}")
        import traceback
        traceback.print_exc()
        
        try:
            show_error_dialog("Error Fatal", f"No se pudo iniciar:\n\n{str(e)}")
        except:
            pass
        
        return 1


if __name__ == "__main__":
    sys.exit(main())
