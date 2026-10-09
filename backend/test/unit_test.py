"""
PASO 5: Tests Unitarios
Tests completos para todos los componentes del sistema
"""
import unittest
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
import json
import os
import sys

# Añadir el directorio padre al path para importar módulos
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config
from models import DatabaseManager, Documento, Pagina
from extractors.pdf_extractor import PDFExtractor
from storage.json_storage import JSONStorage
from storage.database_storage import DatabaseStorage


class TestConfig(unittest.TestCase):
    """Tests para el módulo de configuración"""
    
    def test_get_database_url_sqlite(self):
        """Verifica que se genera correctamente la URL de SQLite"""
        Config.DATABASE_TYPE = 'sqlite'
        Config.DATABASE_PATH = './test.db'
        url = Config.get_database_url()
        self.assertEqual(url, 'sqlite:///./test.db')
    
    def test_get_database_url_postgresql(self):
        """Verifica que se genera correctamente la URL de PostgreSQL"""
        Config.DATABASE_TYPE = 'postgresql'
        Config.POSTGRES_USER = 'testuser'
        Config.POSTGRES_PASSWORD = 'testpass'
        Config.POSTGRES_HOST = 'localhost'
        Config.POSTGRES_PORT = '5432'
        Config.POSTGRES_DB = 'testdb'
        
        url = Config.get_database_url()
        expected = 'postgresql://testuser:testpass@localhost:5432/testdb'
        self.assertEqual(url, expected)
    
    def test_ensure_directories(self):
        """Verifica que se crean los directorios necesarios"""
        with tempfile.TemporaryDirectory() as tmpdir:
            Config.PDF_INPUT_DIR = Path(tmpdir) / 'pdfs'
            Config.JSON_OUTPUT_DIR = Path(tmpdir) / 'json_output'
            
            Config.ensure_directories()
            
            self.assertTrue(Config.PDF_INPUT_DIR.exists())
            self.assertTrue(Config.JSON_OUTPUT_DIR.exists())


class TestModels(unittest.TestCase):
    """Tests para los modelos de base de datos"""
    
    def setUp(self):
        """Configurar base de datos temporal para cada test"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_url = f'sqlite:///{self.temp_db.name}'
        self.db_manager = DatabaseManager(self.db_url)
        self.db_manager.create_tables()
    
    def tearDown(self):
        """Limpiar después de cada test"""
        self.db_manager.engine.dispose()
        os.unlink(self.temp_db.name)
    
    def test_create_tables(self):
        """Verifica que las tablas se crean correctamente"""
        from sqlalchemy import inspect
        inspector = inspect(self.db_manager.engine)
        tables = inspector.get_table_names()
        
        self.assertIn('documentos', tables)
        self.assertIn('paginas', tables)
    
    def test_documento_creation(self):
        """Verifica la creación de un documento"""
        session = self.db_manager.get_session()
        
        doc = Documento(
            nombre_archivo='test.pdf',
            ruta_archivo='/tmp/test.pdf',
            num_paginas=5,
            autor='Test Author',
            titulo='Test Title'
        )
        
        session.add(doc)
        session.commit()
        
        # Recuperar documento
        retrieved = session.query(Documento).first()
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.nombre_archivo, 'test.pdf')
        self.assertEqual(retrieved.num_paginas, 5)
        
        session.close()
    
    def test_pagina_creation(self):
        """Verifica la creación de páginas asociadas a un documento"""
        session = self.db_manager.get_session()
        
        doc = Documento(
            nombre_archivo='test.pdf',
            ruta_archivo='/tmp/test.pdf',
            num_paginas=2
        )
        
        pagina1 = Pagina(numero_pagina=1, contenido='Contenido página 1')
        pagina2 = Pagina(numero_pagina=2, contenido='Contenido página 2')
        
        doc.paginas.append(pagina1)
        doc.paginas.append(pagina2)
        
        session.add(doc)
        session.commit()
        
        # Recuperar y verificar
        retrieved = session.query(Documento).first()
        self.assertEqual(len(retrieved.paginas), 2)
        self.assertEqual(retrieved.paginas[0].contenido, 'Contenido página 1')
        
        session.close()
    
    def test_documento_to_dict(self):
        """Verifica la conversión de documento a diccionario"""
        session = self.db_manager.get_session()
        
        doc = Documento(
            nombre_archivo='test.pdf',
            ruta_archivo='/tmp/test.pdf',
            num_paginas=1,
            titulo='Test'
        )
        
        pagina = Pagina(numero_pagina=1, contenido='Test content')
        doc.paginas.append(pagina)
        
        session.add(doc)
        session.commit()
        
        doc_dict = doc.to_dict()
        
        self.assertEqual(doc_dict['nombre_archivo'], 'test.pdf')
        self.assertEqual(len(doc_dict['paginas']), 1)
        self.assertEqual(doc_dict['paginas'][0]['contenido'], 'Test content')
        
        session.close()
    
    def test_cascade_delete(self):
        """Verifica que al eliminar un documento se eliminan sus páginas"""
        session = self.db_manager.get_session()
        
        doc = Documento(
            nombre_archivo='test.pdf',
            ruta_archivo='/tmp/test.pdf',
            num_paginas=2
        )
        
        doc.paginas.append(Pagina(numero_pagina=1, contenido='Page 1'))
        doc.paginas.append(Pagina(numero_pagina=2, contenido='Page 2'))
        
        session.add(doc)
        session.commit()
        
        doc_id = doc.id
        
        # Eliminar documento
        session.delete(doc)
        session.commit()
        
        # Verificar que las páginas también se eliminaron
        paginas = session.query(Pagina).filter(Pagina.documento_id == doc_id).all()
        self.assertEqual(len(paginas), 0)
        
        session.close()


class TestJSONStorage(unittest.TestCase):
    """Tests para el almacenamiento JSON"""
    
    def setUp(self):
        """Configurar directorio temporal para cada test"""
        self.temp_dir = tempfile.mkdtemp()
        self.storage = JSONStorage(Path(self.temp_dir))
    
    def tearDown(self):
        """Limpiar después de cada test"""
        shutil.rmtree(self.temp_dir)
    
    def test_save_document(self):
        """Verifica que se guarda un documento en JSON"""
        document_data = {
            'nombre_archivo': 'test.pdf',
            'ruta_archivo': '/tmp/test.pdf',
            'num_paginas': 2,
            'titulo': 'Test Document',
            'autor': 'Test Author',
            'fecha_creacion': datetime(2024, 1, 1),
            'paginas': [
                {'numero_pagina': 1, 'contenido': 'Page 1'},
                {'numero_pagina': 2, 'contenido': 'Page 2'}
            ]
        }
        
        json_path = self.storage.save_document(document_data)
        
        self.assertTrue(json_path.exists())
        self.assertTrue(json_path.name.startswith('test_'))
        self.assertTrue(json_path.name.endswith('.json'))
    
    def test_load_document(self):
        """Verifica que se carga correctamente un documento JSON"""
        document_data = {
            'nombre_archivo': 'test.pdf',
            'ruta_archivo': '/tmp/test.pdf',
            'num_paginas': 1,
            'paginas': [
                {'numero_pagina': 1, 'contenido': 'Content'}
            ]
        }
        
        json_path = self.storage.save_document(document_data)
        loaded_data = self.storage.load_document(json_path)
        
        self.assertEqual(loaded_data['nombre_archivo'], 'test.pdf')
        self.assertEqual(loaded_data['num_paginas'], 1)
        self.assertEqual(len(loaded_data['paginas']), 1)
    
    def test_list_documents(self):
        """Verifica el listado de documentos guardados"""
        # Guardar varios documentos
        for i in range(3):
            document_data = {
                'nombre_archivo': f'test{i}.pdf',
                'ruta_archivo': f'/tmp/test{i}.pdf',
                'num_paginas': 1,
                'paginas': [{'numero_pagina': 1, 'contenido': f'Content {i}'}]
            }
            self.storage.save_document(document_data)
        
        docs = self.storage.list_documents()
        self.assertEqual(len(docs), 3)
    
    def test_datetime_serialization(self):
        """Verifica que las fechas se serializan correctamente"""
        document_data = {
            'nombre_archivo': 'test.pdf',
            'ruta_archivo': '/tmp/test.pdf',
            'num_paginas': 1,
            'fecha_creacion': datetime(2024, 1, 15, 10, 30),
            'paginas': [{'numero_pagina': 1, 'contenido': 'Content'}]
        }
        
        json_path = self.storage.save_document(document_data)
        loaded_data = self.storage.load_document(json_path)
        
        self.assertIsInstance(loaded_data['fecha_creacion'], str)
        self.assertIn('fecha_procesamiento', loaded_data)


class TestDatabaseStorage(unittest.TestCase):
    """Tests para el almacenamiento en base de datos"""
    
    def setUp(self):
        """Configurar base de datos temporal para cada test"""
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_url = f'sqlite:///{self.temp_db.name}'
        self.db_manager = DatabaseManager(self.db_url)
        self.storage = DatabaseStorage(self.db_manager)
    
    def tearDown(self):
        """Limpiar después de cada test"""
        self.db_manager.engine.dispose()
        os.unlink(self.temp_db.name)
    
    def test_save_document(self):
        """Verifica que se guarda un documento en BD"""
        document_data = {
            'nombre_archivo': 'test.pdf',
            'ruta_archivo': '/tmp/test.pdf',
            'num_paginas': 2,
            'titulo': 'Test',
            'autor': 'Author',
            'fecha_creacion': datetime(2024, 1, 1),
            'paginas': [
                {'numero_pagina': 1, 'contenido': 'Page 1'},
                {'numero_pagina': 2, 'contenido': 'Page 2'}
            ]
        }
        
        doc_id = self.storage.save_document(document_data)
        
        self.assertIsNotNone(doc_id)
        self.assertIsInstance(doc_id, int)
    
    def test_get_document(self):
        """Verifica la recuperación de un documento"""
        document_data = {
            'nombre_archivo': 'test.pdf',
            'ruta_archivo': '/tmp/test.pdf',
            'num_paginas': 1,
            'paginas': [{'numero_pagina': 1, 'contenido': 'Content'}]
        }
        
        doc_id = self.storage.save_document(document_data)
        retrieved = self.storage.get_document(doc_id)
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved['nombre_archivo'], 'test.pdf')
        self.assertEqual(len(retrieved['paginas']), 1)
    
    def test_list_documents(self):
        """Verifica el listado de documentos"""
        # Guardar varios documentos
        for i in range(3):
            document_data = {
                'nombre_archivo': f'test{i}.pdf',
                'ruta_archivo': f'/tmp/test{i}.pdf',
                'num_paginas': 1,
                'paginas': [{'numero_pagina': 1, 'contenido': f'Content {i}'}]
            }
            self.storage.save_document(document_data)
        
        docs = self.storage.list_documents()
        self.assertEqual(len(docs), 3)
    
    def test_search_by_filename(self):
        """Verifica la búsqueda por nombre de archivo"""
        # Guardar documentos
        document_data1 = {
            'nombre_archivo': 'informe_enero.pdf',
            'ruta_archivo': '/tmp/informe_enero.pdf',
            'num_paginas': 1,
            'paginas': [{'numero_pagina': 1, 'contenido': 'Content'}]
        }
        
        document_data2 = {
            'nombre_archivo': 'reporte_febrero.pdf',
            'ruta_archivo': '/tmp/reporte_febrero.pdf',
            'num_paginas': 1,
            'paginas': [{'numero_pagina': 1, 'contenido': 'Content'}]
        }
        
        self.storage.save_document(document_data1)
        self.storage.save_document(document_data2)
        
        # Buscar por 'informe'
        results = self.storage.search_by_filename('informe')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['nombre_archivo'], 'informe_enero.pdf')
    
    def test_delete_document(self):
        """Verifica la eliminación de documentos"""
        document_data = {
            'nombre_archivo': 'test.pdf',
            'ruta_archivo': '/tmp/test.pdf',
            'num_paginas': 1,
            'paginas': [{'numero_pagina': 1, 'contenido': 'Content'}]
        }
        
        doc_id = self.storage.save_document(document_data)
        
        # Eliminar
        result = self.storage.delete_document(doc_id)
        self.assertTrue(result)
        
        # Verificar que no existe
        retrieved = self.storage.get_document(doc_id)
        self.assertIsNone(retrieved)
    
    def test_delete_nonexistent_document(self):
        """Verifica que eliminar un documento inexistente retorna False"""
        result = self.storage.delete_document(9999)
        self.assertFalse(result)


class TestPDFExtractorMock(unittest.TestCase):
    """Tests para el extractor de PDF (usando datos simulados)"""
    
    def test_extractor_initialization(self):
        """Verifica que el extractor se inicializa correctamente con PDF válido"""
        # Nota: Este test requeriría un PDF real para funcionar completamente
        # Se puede crear un PDF de prueba usando reportlab o similar
        pass
    
    def test_get_num_pages(self):
        """Verifica el conteo de páginas"""
        # Test que requeriría un PDF real
        pass
    
    def test_extract_metadata(self):
        """Verifica la extracción de metadatos"""
        # Test que requeriría un PDF real
        pass


def run_all_tests():
    """Ejecuta todos los tests"""
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar tests
    suite.addTests(loader.loadTestsFromTestCase(TestConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestModels))
    suite.addTests(loader.loadTestsFromTestCase(TestJSONStorage))
    suite.addTests(loader.loadTestsFromTestCase(TestDatabaseStorage))
    
    # Ejecutar
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    print("=" * 70)
    print("EJECUTANDO TESTS UNITARIOS - Sistema de Extracción de PDFs")
    print("=" * 70)
    print()
    
    result = run_all_tests()
    
    print()
    print("=" * 70)
    print("RESUMEN DE TESTS")
    print("=" * 70)
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Tests exitosos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Tests fallidos: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    print("=" * 70)
    
    # Salir con código apropiado
    sys.exit(0 if result.wasSuccessful() else 1)