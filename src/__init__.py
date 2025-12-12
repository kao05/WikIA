import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

# Importar ventana principal
from ui.main_window import MainWindow


def setup_application():
    """
    Configura la aplicación Qt con estilos y fuentes.
    
    Returns:
        QApplication: Instancia de la aplicación
    """
    app = QApplication(sys.argv)
    
    # Configurar nombre y versión
    app.setApplicationName("Wikia Cognitiva")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Wikia Cognitiva")
    
    # Configurar estilo
    app.setStyle('Fusion')
    
    # Configurar fuente por defecto
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Habilitar high DPI scaling
    app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
    
    return app


def load_stylesheet(app: QApplication):
    """
    Carga la hoja de estilos principal.
    
    Args:
        app: Instancia de QApplication
    """
    try:
        # Ruta al archivo de estilos
        style_path = Path(__file__).parent / "ui" / "styles" / "main.qss"
        
        if style_path.exists():
            with open(style_path, 'r', encoding='utf-8') as f:
                app.setStyleSheet(f.read())
            print(" Estilos cargados")
        else:
            print(" Archivo de estilos no encontrado, usando estilos por defecto")
    
    except Exception as e:
        print(f" Error cargando estilos: {e}")


def show_error_dialog(title: str, message: str):
    """
    Muestra un diálogo de error.
    
    Args:
        title: Título del diálogo
        message: Mensaje de error
    """
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Icon.Critical)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg_box.exec()


def main():
    """
    Función principal que inicia la aplicación.
    """
    print("\n" + "="*70)
    print("  WIKIA COGNITIVA - Plataforma Educativa de IA")
    print("="*70 + "\n")
    
    try:
        # Crear aplicación Qt
        print(" Inicializando aplicación...")
        app = setup_application()
        
        # Cargar estilos
        print(" Cargando estilos...")
        load_stylesheet(app)
        
        # Crear ventana principal
        print("  Creando ventana principal...")
        window = MainWindow()
        
        # Verificar que la ventana se inicializó correctamente
        if not window.is_initialized():
            show_error_dialog(
                "Error de Inicialización",
                "No se pudo inicializar la aplicación.\n\n"
                "Por favor verifica que:\n"
                "1. El archivo curriculum.json existe en src/data/\n"
                "2. Los archivos de contenido existen en src/data/content/"
            )
            return 1
        
        # Mostrar ventana
        print(" Mostrando ventana principal...")
        window.show()
        
        print("\n ¡Aplicación iniciada correctamente!")
        print("="*70 + "\n")
        
        # Ejecutar loop de eventos
        return app.exec()
    
    except Exception as e:
        print(f"\n Error fatal al iniciar la aplicación:")
        print(f"   {str(e)}")
        print("\n" + "="*70 + "\n")
        
        # Mostrar diálogo de error si es posible
        try:
            show_error_dialog(
                "Error Fatal",
                f"No se pudo iniciar la aplicación:\n\n{str(e)}"
            )
        except:
            pass
        
        return 1


if __name__ == "__main__":
    sys.exit(main())
