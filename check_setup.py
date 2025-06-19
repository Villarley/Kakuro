#!/usr/bin/env python3
"""
Script de verificación para comprobar que la estructura del proyecto esté correcta
"""

import os
import sys
import json
from pathlib import Path


def check_directory_structure():
    """Verifica que la estructura de directorios esté correcta"""
    print("🔍 Verificando estructura de directorios...")
    
    required_dirs = [
        "data",
        "gui", 
        "logic",
        "utils",
        "docs",
        "tests"
    ]
    
    missing_dirs = []
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"❌ Directorios faltantes: {missing_dirs}")
        return False
    else:
        print("✅ Estructura de directorios correcta")
        return True


def check_required_files():
    """Verifica que los archivos requeridos existan"""
    print("\n📁 Verificando archivos requeridos...")
    
    required_files = [
        "main.py",
        "README.md",
        "requirements.txt",
        ".gitignore",
        "data/kakuro2025_partidas.json",
        "data/kakuro2025_récords.json",
        "data/kakuro2025_configuración.json",
        "data/kakuro2025_juego_actual.json",
        "gui/__init__.py",
        "gui/main_window.py",
        "gui/game_screen.py",
        "gui/components.py",
        "logic/__init__.py",
        "logic/validator.py",
        "logic/game_manager.py",
        "logic/pila_jugadas.py",
        "logic/partida_loader.py",
        "utils/__init__.py",
        "utils/file_manager.py",
        "utils/timer.py",
        "tests/__init__.py",
        "tests/test_validator.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Archivos faltantes: {missing_files}")
        return False
    else:
        print("✅ Todos los archivos requeridos existen")
        return True


def check_json_files():
    """Verifica que los archivos JSON sean válidos"""
    print("\n📄 Verificando archivos JSON...")
    
    json_files = [
        "data/kakuro2025_partidas.json",
        "data/kakuro2025_récords.json",
        "data/kakuro2025_configuración.json",
        "data/kakuro2025_juego_actual.json"
    ]
    
    invalid_files = []
    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            invalid_files.append(f"{file_path}: {e}")
    
    if invalid_files:
        print(f"❌ Archivos JSON inválidos: {invalid_files}")
        return False
    else:
        print("✅ Todos los archivos JSON son válidos")
        return True


def check_python_imports():
    """Verifica que los módulos Python se puedan importar"""
    print("\n🐍 Verificando importaciones de Python...")
    
    # Añadir el directorio actual al path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    modules_to_test = [
        ("gui.main_window", "MainWindow"),
        ("gui.game_screen", "GameScreen"),
        ("gui.components", "NumberPanel"),
        ("logic.validator", "KakuroValidator"),
        ("logic.game_manager", "GameManager"),
        ("logic.pila_jugadas", "PilaJugadas"),
        ("logic.partida_loader", "PartidaLoader"),
        ("utils.file_manager", "FileManager"),
        ("utils.timer", "GameTimer")
    ]
    
    failed_imports = []
    for module_name, class_name in modules_to_test:
        try:
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)
        except (ImportError, AttributeError) as e:
            failed_imports.append(f"{module_name}.{class_name}: {e}")
    
    if failed_imports:
        print(f"❌ Importaciones fallidas: {failed_imports}")
        return False
    else:
        print("✅ Todas las importaciones funcionan correctamente")
        return True


def check_tests():
    """Verifica que las pruebas se puedan ejecutar"""
    print("\n🧪 Verificando pruebas...")
    
    try:
        import unittest
        from tests.test_validator import TestKakuroValidator
        
        # Crear un test suite y ejecutar las pruebas
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(TestKakuroValidator)
        runner = unittest.TextTestRunner(verbosity=0)
        result = runner.run(suite)
        
        if result.wasSuccessful():
            print("✅ Las pruebas se ejecutan correctamente")
            return True
        else:
            print("❌ Algunas pruebas fallaron")
            return False
            
    except Exception as e:
        print(f"❌ Error ejecutando pruebas: {e}")
        return False


def main():
    """Función principal de verificación"""
    print("🚀 Verificando configuración del proyecto Kakuro 2025\n")
    
    checks = [
        check_directory_structure,
        check_required_files,
        check_json_files,
        check_python_imports,
        check_tests
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 ¡Todas las verificaciones pasaron! El proyecto está listo.")
        print("\nPara ejecutar el juego:")
        print("  python3 main.py")
        print("\nPara ejecutar las pruebas:")
        print("  python3 -m unittest tests.test_validator -v")
    else:
        print("❌ Algunas verificaciones fallaron. Revisa los errores arriba.")
        sys.exit(1)


if __name__ == "__main__":
    main() 