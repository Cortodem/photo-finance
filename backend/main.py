"""
PASO 5: Script Principal
Procesamiento de directorio y manejo de argumentos CLI
"""
import argparse
import sys
from pathlib import Path

from config import config
from models import DatabaseManager
from extractors.pdf_extractor import extract_pdf
from storage.json_storage import JSONStorage
from storage.database_storage import DatabaseStorage


def process_pdf_file(pdf_path: Path, storage_type: str, json_storage=None, db_storage=None):
    """
    Procesa un archivo PDF individual
    
    Args:
        pdf_path: Ruta al archivo PDF
        storage_type: Tipo de almacenamiento ('json', 'database', 'both')
        json_storage: Instancia de JSONStorage (opcional)
        db_storage: Instancia de DatabaseStorage (opcional)
    """
    print(f"\n📄 Procesando: {pdf_path.name}")
    
    try:
        # Extraer información del PDF
        document_data = extract_pdf(pdf_path)
        print(f"  ✓ Extraídas {document_data['num_paginas']} páginas")
        
        # Guardar según el tipo de almacenamiento
        if storage_type in ['json', 'both']:
            if json_storage:
                json_storage.save_document(document_data)
        
        if storage_type in ['database', 'both']:
            if db_storage:
                db_storage.save_document(document_data)
        
        print(f"  ✓ Procesamiento completado")
        
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")


def process_directory(input_dir: Path, storage_type: str):
    """
    Procesa todos los PDFs en un directorio
    
    Args:
        input_dir: Directorio con archivos PDF
        storage_type: Tipo de almacenamiento ('json', 'database', 'both')
    """
    # Buscar archivos PDF
    pdf_files = list(input_dir.glob('*.pdf'))
    
    if not pdf_files:
        print(f"⚠ No se encontraron archivos PDF en {input_dir}")
        return
    
    print(f"\n🔍 Encontrados {len(pdf_files)} archivos PDF")
    
    # Inicializar almacenamiento
    json_storage = None
    db_storage = None
    
    if storage_type in ['json', 'both']:
        json_storage = JSONStorage(config.JSON_OUTPUT_DIR)
        print(f"📁 Salida JSON: {config.JSON_OUTPUT_DIR}")
    
    if storage_type in ['database', 'both']:
        db_manager = DatabaseManager(config.get_database_url())
        db_storage = DatabaseStorage(db_manager)
        print(f"💾 Base de datos: {config.DATABASE_TYPE}")
    
    # Procesar cada PDF
    for pdf_file in pdf_files:
        process_pdf_file(pdf_file, storage_type, json_storage, db_storage)
    
    print(f"\n✅ Procesamiento completado: {len(pdf_files)} archivos")


def list_documents(storage_type: str):
    """
    Lista documentos almacenados
    
    Args:
        storage_type: Tipo de almacenamiento ('json', 'database')
    """
    print(f"\n📋 Documentos almacenados ({storage_type}):")
    
    if storage_type == 'json':
        json_storage = JSONStorage(config.JSON_OUTPUT_DIR)
        docs = json_storage.list_documents()
        
        if not docs:
            print("  No hay documentos guardados")
            return
        
        for doc in docs:
            print(f"  - {doc.name}")
    
    elif storage_type == 'database':
        db_manager = DatabaseManager(config.get_database_url())
        db_storage = DatabaseStorage(db_manager)
        docs = db_storage.list_documents()
        
        if not docs:
            print("  No hay documentos guardados")
            return
        
        for doc in docs:
            print(f"  - ID: {doc['id']} | {doc['nombre_archivo']} | {doc['num_paginas']} páginas")


def main():
    """Función principal con argumentos CLI"""
    
    parser = argparse.ArgumentParser(
        description='Sistema modular de extracción de PDFs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  # Procesar PDFs y guardar en JSON
  python main.py --storage json
  
  # Procesar PDFs y guardar en base de datos
  python main.py --storage database
  
  # Procesar PDFs y guardar en ambos formatos
  python main.py --storage both
  
  # Procesar PDFs desde un directorio específico
  python main.py --input ./mis_pdfs --storage json
  
  # Listar documentos guardados
  python main.py --list json
  python main.py --list database
        """
    )
    
    parser.add_argument(
        '--input',
        type=str,
        help=f'Directorio de entrada con PDFs (default: {config.PDF_INPUT_DIR})',
        default=None
    )
    
    parser.add_argument(
        '--storage',
        type=str,
        choices=['json', 'database', 'both'],
        help='Tipo de almacenamiento (default: json)',
        default='json'
    )
    
    parser.add_argument(
        '--list',
        type=str,
        choices=['json', 'database'],
        help='Listar documentos almacenados',
        default=None
    )
    
    args = parser.parse_args()
    
    # Asegurar que existan los directorios
    config.ensure_directories()
    
    # Listar documentos
    if args.list:
        list_documents(args.list)
        return
    
    # Determinar directorio de entrada
    input_dir = Path(args.input) if args.input else config.PDF_INPUT_DIR
    
    if not input_dir.exists():
        print(f"❌ Error: El directorio {input_dir} no existe")
        sys.exit(1)
    
    # Procesar PDFs
    print(f"🚀 Iniciando extracción de PDFs")
    print(f"📂 Directorio de entrada: {input_dir}")
    
    process_directory(input_dir, args.storage)


if __name__ == '__main__':
    main()