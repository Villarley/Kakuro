#!/usr/bin/env python3
"""
Script principal del juego Kakuro 2025
Lanza la aplicación principal
"""

import sys
import os

# Añadir el directorio actual al path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow
from logic.game_manager import GameManager
from utils.file_manager import FileManager


def main():
    """Función principal que inicia la aplicación"""
    try:
        # Inicializar componentes del juego
        file_manager = FileManager()
        game_manager = GameManager()
        
        # Crear y ejecutar la ventana principal
        app = MainWindow()
        app.run()
        
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 