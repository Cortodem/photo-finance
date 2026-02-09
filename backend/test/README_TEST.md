# Guía de Tests Unitarios

## 🧪 Descripción

Los tests unitarios verifican el correcto funcionamiento de todos los componentes del sistema de extracción de PDFs.

## 📋 Tests Disponibles

### 1. TestConfig (5 tests)
Verifica la configuración del sistema:
- Generación correcta de URLs para SQLite
- Generación correcta de URLs para PostgreSQL
- Creación automática de directorios necesarios

### 2. TestModels (6 tests)
Verifica los modelos de base de datos:
- Creación correcta de tablas
- Creación de documentos
- Creación de páginas
- Relaciones entre documentos y páginas
- Conversión de objetos a diccionarios
- Eliminación en cascada (al borrar documento se borran páginas)

### 3. TestJSONStorage (4 tests)
Verifica el almacenamiento en JSON:
- Guardar documentos en formato JSON
- Cargar documentos desde archivos JSON
- Listar todos los documentos guardados
- Serialización correcta de fechas

### 4. TestDatabaseStorage (6 tests)
Verifica el almacenamiento en base de datos:
- Guardar documentos en BD
- Recuperar documentos por ID
- Listar todos los documentos
- Búsqueda por nombre de archivo
- Eliminar documentos
- Intentar eliminar documentos inexistentes

## 🚀 Ejecución

### Método 1: Ejecutar todos los tests

```bash
python test/unit_test.py
```

### Método 2: Script auxiliar

```bash
# Todos los tests
python run_tests.py

# Tests específicos
python run_tests.py config
python run_tests.py models
python run_tests.py json
python run_tests.py database
```

### Método 3: Usando unittest directamente

```bash
# Todos los tests
python -m unittest discover -s test -v

# Test específico
python -m unittest test.unit_test.TestConfig -v
python -m unittest test.unit_test.TestModels -v
python -m unittest test.unit_test.TestJSONStorage -v
python -m unittest test.unit_test.TestDatabaseStorage -v

# Test individual
python -m unittest test.unit_test.TestConfig.test_get_database_url_sqlite -v
```

## 📊 Salida Esperada

```
======================================================================
EJECUTANDO TESTS UNITARIOS - Sistema de Extracción de PDFs
======================================================================

test_ensure_directories (test.unit_test.TestConfig)
Verifica que se crean los directorios necesarios ... ok
test_get_database_url_postgresql (test.unit_test.TestConfig)
Verifica que se genera correctamente la URL de PostgreSQL ... ok
test_get_database_url_sqlite (test.unit_test.TestConfig)
Verifica que se genera correctamente la URL de SQLite ... ok

[... más tests ...]

----------------------------------------------------------------------
Ran 21 tests in 0.543s

OK

======================================================================
RESUMEN DE TESTS
======================================================================
Tests ejecutados: 21
Tests exitosos: 21
Tests fallidos: 0
Errores: 0
======================================================================
```

## 🔍 Análisis de Cobertura

Para verificar qué porcentaje del código está cubierto por tests:

```bash
# Instalar coverage
pip install coverage

# Ejecutar tests con análisis de cobertura
coverage run test/unit_test.py

# Ver reporte en consola
coverage report

# Generar reporte HTML detallado
coverage html

# Abrir reporte (se genera en htmlcov/index.html)
```

## ⚙️ Características de los Tests

### Tests aislados
Cada test es independiente y no afecta a otros tests:
- Usan bases de datos temporales en memoria
- Crean directorios temporales que se limpian automáticamente
- No modifican archivos del sistema

### Setup y Teardown
- `setUp()`: Prepara el entorno antes de cada test
- `tearDown()`: Limpia el entorno después de cada test

### Aserciones utilizadas
- `assertEqual(a, b)`: Verifica que a == b
- `assertIsNotNone(x)`: Verifica que x no es None
- `assertTrue(x)`: Verifica que x es True
- `assertFalse(x)`: Verifica que x es False
- `assertIn(x, lista)`: Verifica que x está en lista
- `assertIsInstance(x, tipo)`: Verifica el tipo de x

## 🐛 Depuración

Si un test falla:

1. **Ver detalles del error**:
   ```bash
   python -m unittest test.unit_test.TestConfig -v
   ```

2. **Agregar prints temporales**:
   ```python
   def test_algo(self):
       print(f"Debug: valor = {valor}")
       self.assertEqual(valor, esperado)
   ```

3. **Usar pdb (Python Debugger)**:
   ```python
   import pdb
   
   def test_algo(self):
       pdb.set_trace()  # Pausa ejecución aquí
       # código a depurar
   ```

## 📝 Agregar Nuevos Tests

Para agregar un nuevo test:

```python
def test_nueva_funcionalidad(self):
    """Descripción del test"""
    # 1. Preparar datos
    datos = {...}
    
    # 2. Ejecutar acción
    resultado = funcion_a_probar(datos)
    
    # 3. Verificar resultado
    self.assertEqual(resultado, esperado)
    self.assertTrue(condicion)
```

## ✅ Mejores Prácticas

1. **Nombres descriptivos**: El nombre del test debe explicar qué verifica
2. **Un concepto por test**: Cada test verifica una cosa específica
3. **Tests independientes**: No dependen del orden de ejecución
4. **Datos de prueba claros**: Usar datos que hagan obvio qué se prueba
5. **Mensajes de error útiles**: Agregar mensajes en las aserciones cuando ayude

## 🔗 Referencias

- [unittest Documentation](https://docs.python.org/3/library/unittest.html)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)