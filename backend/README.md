# Sistema Modular de Extracción de PDFs

Sistema completo y modular para extraer texto y metadatos de archivos PDF, con opciones de almacenamiento en JSON y bases de datos (SQLite/PostgreSQL).

## 📁 Estructura del Proyecto

```
pdf_extractor/
├── main.py                    # Script principal con CLI
├── config.py                  # PASO 1: Configuración y variables de entorno
├── models.py                  # PASO 2: Modelos SQLAlchemy (Documento, Página)
├── extractors/
│   ├── __init__.py
│   └── pdf_extractor.py       # PASO 3: Extractor de PDF
├── storage/
│   ├── __init__.py
│   ├── json_storage.py        # PASO 4a: Almacenamiento JSON
│   └── database_storage.py    # PASO 4b: Almacenamiento en BD
├── test/
│   ├── __init__.py
│   └── unit_test.py           # PASO 5: Tests unitarios
├── requirements.txt           # Dependencias
├── .env.example              # Plantilla de configuración
├── ejemplo_uso.py            # Ejemplos prácticos
└── README.md                 # Esta documentación
```

## 🚀 Instalación

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

Copiar `.env.example` a `.env` y ajustar según necesites:

```bash
cp .env.example .env
```

**Para SQLite (por defecto):**
```env
DATABASE_TYPE=sqlite
DATABASE_PATH=./pdf_database.db
PDF_INPUT_DIR=./pdfs
JSON_OUTPUT_DIR=./output_json
```

**Para PostgreSQL:**
```env
DATABASE_TYPE=postgresql
POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu_contraseña
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=pdf_extractor
PDF_INPUT_DIR=./pdfs
JSON_OUTPUT_DIR=./output_json
```

### 3. Crear directorio de PDFs

```bash
mkdir pdfs
# Coloca tus archivos PDF aquí
```

## 📖 Uso

### Ejemplos Básicos

**1. Procesar PDFs y guardar en JSON:**
```bash
python main.py --storage json
```

**2. Procesar PDFs y guardar en base de datos:**
```bash
python main.py --storage database
```

**3. Guardar en ambos formatos:**
```bash
python main.py --storage both
```

**4. Especificar directorio de entrada:**
```bash
python main.py --input ./mis_pdfs --storage json
```

**5. Listar documentos guardados:**
```bash
# Listar JSONs
python main.py --list json

# Listar documentos en BD
python main.py --list database
```

### Ayuda del CLI

```bash
python main.py --help
```

## 🔧 Componentes del Sistema

### PASO 1: Configuración (config.py)

Gestiona variables de entorno y configuración de base de datos.

**Características:**
- Soporte para SQLite y PostgreSQL
- Rutas configurables para entrada/salida
- Generación automática de URLs de conexión

**Uso programático:**
```python
from config import config

# Obtener URL de base de datos
db_url = config.get_database_url()

# Asegurar directorios
config.ensure_directories()
```

### PASO 2: Modelos de Datos (models.py)

Define estructura de datos con SQLAlchemy.

**Modelos:**
- `Documento`: Información del PDF (nombre, autor, título, fechas)
- `Pagina`: Contenido de cada página
- `DatabaseManager`: Gestor de conexión a BD

**Uso programático:**
```python
from models import DatabaseManager, Documento, Pagina

# Crear gestor
db_manager = DatabaseManager('sqlite:///mi_base.db')
db_manager.create_tables()

# Obtener sesión
session = db_manager.get_session()
```

### PASO 3: Extractor de PDF (extractors/pdf_extractor.py)

Extrae texto y metadatos de archivos PDF.

**Características:**
- Extracción de texto por página
- Extracción de metadatos (título, autor, fecha)
- Manejo robusto de errores

**Uso programático:**
```python
from extractors.pdf_extractor import PDFExtractor, extract_pdf
from pathlib import Path

# Método 1: Función auxiliar
data = extract_pdf(Path('documento.pdf'))

# Método 2: Clase completa
extractor = PDFExtractor(Path('documento.pdf'))
metadata = extractor.extract_metadata()
num_pages = extractor.get_num_pages()
all_pages = extractor.extract_all_pages()
```

### PASO 4a: Almacenamiento JSON (storage/json_storage.py)

Guarda documentos en formato JSON estructurado.

**Características:**
- Archivos JSON con timestamp
- Serialización automática de fechas
- Listado de documentos

**Uso programático:**
```python
from storage.json_storage import JSONStorage
from pathlib import Path

storage = JSONStorage(Path('./output'))

# Guardar documento
json_path = storage.save_document(document_data)

# Cargar documento
data = storage.load_document(json_path)

# Listar todos
docs = storage.list_documents()
```

### PASO 4b: Almacenamiento en BD (storage/database_storage.py)

Guarda documentos en base de datos relacional.

**Características:**
- Soporte SQLite y PostgreSQL
- Operaciones CRUD completas
- Búsqueda por nombre de archivo

**Uso programático:**
```python
from storage.database_storage import DatabaseStorage
from models import DatabaseManager

db_manager = DatabaseManager('sqlite:///pdfs.db')
storage = DatabaseStorage(db_manager)

# Guardar documento
doc_id = storage.save_document(document_data)

# Obtener documento
doc = storage.get_document(doc_id)

# Listar todos
docs = storage.list_documents()

# Buscar por nombre
results = storage.search_by_filename('informe')

# Eliminar
storage.delete_document(doc_id)
```

## 🔍 Ejemplos de Uso Completo

### SQLite (Simple)

```bash
# Configurar .env
echo "DATABASE_TYPE=sqlite" > .env
echo "DATABASE_PATH=./documentos.db" >> .env
echo "PDF_INPUT_DIR=./pdfs" >> .env

# Procesar PDFs
python main.py --storage database

# Ver documentos
python main.py --list database
```

### PostgreSQL (Avanzado)

```bash
# 1. Crear base de datos PostgreSQL
createdb pdf_extractor

# 2. Configurar .env
cat > .env << EOF
DATABASE_TYPE=postgresql
POSTGRES_USER=postgres
POSTGRES_PASSWORD=mipass
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=pdf_extractor
PDF_INPUT_DIR=./pdfs
EOF

# 3. Procesar PDFs
python main.py --storage database

# 4. Ver documentos
python main.py --list database
```

### Modo Híbrido (JSON + Base de Datos)

```bash
# Guardar en ambos formatos
python main.py --storage both

# Listar en ambos
python main.py --list json
python main.py --list database
```

## 📊 Formato de Datos

### Estructura JSON de salida:

```json
{
  "nombre_archivo": "documento.pdf",
  "ruta_archivo": "/ruta/completa/documento.pdf",
  "num_paginas": 3,
  "titulo": "Título del documento",
  "autor": "Autor del documento",
  "fecha_creacion": "2024-01-15T10:30:00",
  "fecha_procesamiento": "2026-02-09T14:22:00",
  "paginas": [
    {
      "numero_pagina": 1,
      "contenido": "Texto de la primera página..."
    },
    {
      "numero_pagina": 2,
      "contenido": "Texto de la segunda página..."
    }
  ]
}
```

### Esquema de Base de Datos:

**Tabla: documentos**
- `id`: INTEGER (PK)
- `nombre_archivo`: VARCHAR(255)
- `ruta_archivo`: VARCHAR(500)
- `num_paginas`: INTEGER
- `autor`: VARCHAR(255)
- `titulo`: VARCHAR(500)
- `fecha_creacion`: DATETIME
- `fecha_procesamiento`: DATETIME

**Tabla: paginas**
- `id`: INTEGER (PK)
- `documento_id`: INTEGER (FK → documentos.id)
- `numero_pagina`: INTEGER
- `contenido`: TEXT

## 🛠️ Personalización

### Agregar nuevos extractores:

```python
# extractors/custom_extractor.py
class CustomExtractor:
    def extract(self, file_path):
        # Tu lógica aquí
        pass
```

### Agregar nuevos tipos de almacenamiento:

```python
# storage/mongodb_storage.py
class MongoDBStorage:
    def save_document(self, document_data):
        # Tu lógica aquí
        pass
```

## 📝 Dependencias

- **PyPDF2**: Extracción de texto de PDFs
- **SQLAlchemy**: ORM para bases de datos
- **python-dotenv**: Gestión de variables de entorno
- **psycopg2-binary**: Driver de PostgreSQL

## 🧪 Tests Unitarios (PASO 5)

El sistema incluye tests unitarios completos para verificar el funcionamiento de todos los componentes.

### Ejecutar todos los tests:

```bash
python test/unit_test.py
```

### Tests incluidos:

**TestConfig** - Configuración del sistema:
- ✓ Generación de URLs de base de datos (SQLite y PostgreSQL)
- ✓ Creación automática de directorios

**TestModels** - Modelos de datos:
- ✓ Creación de tablas
- ✓ Creación de documentos y páginas
- ✓ Relaciones entre modelos
- ✓ Conversión a diccionario
- ✓ Eliminación en cascada

**TestJSONStorage** - Almacenamiento JSON:
- ✓ Guardar documentos
- ✓ Cargar documentos
- ✓ Listar documentos
- ✓ Serialización de fechas

**TestDatabaseStorage** - Almacenamiento en BD:
- ✓ Guardar documentos
- ✓ Recuperar documentos por ID
- ✓ Listar todos los documentos
- ✓ Búsqueda por nombre de archivo
- ✓ Eliminar documentos

### Salida esperada:

```
======================================================================
EJECUTANDO TESTS UNITARIOS - Sistema de Extracción de PDFs
======================================================================

test_ensure_directories (test.unit_test.TestConfig) ... ok
test_get_database_url_postgresql (test.unit_test.TestConfig) ... ok
test_get_database_url_sqlite (test.unit_test.TestConfig) ... ok
...
----------------------------------------------------------------------
Ran 20 tests in 0.543s

OK

======================================================================
RESUMEN DE TESTS
======================================================================
Tests ejecutados: 20
Tests exitosos: 20
Tests fallidos: 0
Errores: 0
======================================================================
```

### Ejecutar tests específicos:

```bash
# Solo tests de configuración
python -m unittest test.unit_test.TestConfig

# Solo tests de modelos
python -m unittest test.unit_test.TestModels

# Solo tests de JSON
python -m unittest test.unit_test.TestJSONStorage

# Solo tests de base de datos
python -m unittest test.unit_test.TestDatabaseStorage
```

### Verificar cobertura:

```bash
# Instalar coverage
pip install coverage

# Ejecutar con cobertura
coverage run test/unit_test.py
coverage report
coverage html  # Genera reporte HTML
```

## 🔐 Seguridad

- No incluir archivos `.env` en control de versiones
- Usar contraseñas fuertes para PostgreSQL
- Validar permisos de archivos antes de procesar
- Sanitizar entradas de usuario

## 📚 Fuentes y Referencias

- [PyPDF2 Documentation](https://pypdf2.readthedocs.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)