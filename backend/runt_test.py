#!/usr/bin/env python3
"""
Script auxiliar para ejecutar tests unitarios
"""
import sys
import subprocess
from pathlib import Path


def run_all_tests():
    """Ejecuta todos los tests"""
    print("🧪 Ejecutando todos los tests...\n")
    result = subprocess.run([sys.executable, 'test/unit_test.py'])
    return result.returncode


def run_specific_test(test_class):
    """Ejecuta una clase de test específica"""
    test_classes = {
        'config': 'test.unit_test.TestConfig',
        'models': 'test.unit_test.TestModels',
        'json': 'test.unit_test.TestJSONStorage',
        'database': 'test.unit_test.TestDatabaseStorage',
    }
    
    if test_class not in test_classes:
        print(f"❌ Clase de test '{test_class}' no encontrada")
        print(f"Opciones disponibles: {', '.join(test_classes.keys())}")
        return 1
    
    print(f"🧪 Ejecutando tests de {test_class}...\n")
    result = subprocess.run([
        sys.executable, '-m', 'unittest', test_classes[test_class], '-v'
    ])
    return result.returncode


def show_help():
    """Muestra ayuda"""
    print("""
🧪 Script de Tests - Sistema de Extracción de PDFs

Uso:
    python run_tests.py [opción]

Opciones:
    (sin argumentos)  Ejecuta todos los tests
    config           Ejecuta solo tests de configuración
    models           Ejecuta solo tests de modelos
    json             Ejecuta solo tests de JSON
    database         Ejecuta solo tests de base de datos
    help             Muestra esta ayuda

Ejemplos:
    python run_tests.py              # Todos los tests
    python run_tests.py config       # Solo configuración
    python run_tests.py database     # Solo base de datos
    """)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        # Sin argumentos, ejecutar todos
        sys.exit(run_all_tests())
    
    elif len(sys.argv) == 2:
        arg = sys.argv[1].lower()
        
        if arg in ['help', '-h', '--help']:
            show_help()
            sys.exit(0)
        else:
            # Ejecutar test específico
            sys.exit(run_specific_test(arg))
    
    else:
        print("❌ Demasiados argumentos")
        show_help()
        sys.exit(1)