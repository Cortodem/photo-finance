"""
PASO 1: Configuración del sistema
Gestiona variables de entorno y configuración de base de datos
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Cargar variables de entorno
load_dotenv()


class Config:
    """Configuración centralizada del sistema"""
    
    # Tipo de base de datos
    DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'sqlite')
    
    # SQLite
    DATABASE_PATH = os.getenv('DATABASE_PATH', './pdf_database.db')
    
    # PostgreSQL
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', '')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'pdf_extractor')
    
    # Rutas
    PDF_INPUT_DIR = Path(os.getenv('PDF_INPUT_DIR', './pdfs'))
    JSON_OUTPUT_DIR = Path(os.getenv('JSON_OUTPUT_DIR', './output_json'))
    
    @classmethod
    def get_database_url(cls) -> str:
        """
        Obtiene la URL de conexión según el tipo de base de datos
        
        Returns:
            str: URL de conexión a la base de datos
        """
        if cls.DATABASE_TYPE == 'postgresql':
            return (
                f"postgresql://{cls.POSTGRES_USER}:{cls.POSTGRES_PASSWORD}"
                f"@{cls.POSTGRES_HOST}:{cls.POSTGRES_PORT}/{cls.POSTGRES_DB}"
            )
        else:  # sqlite por defecto
            return f"sqlite:///{cls.DATABASE_PATH}"
    
    @classmethod
    def ensure_directories(cls):
        """Crea los directorios necesarios si no existen"""
        cls.PDF_INPUT_DIR.mkdir(parents=True, exist_ok=True)
        cls.JSON_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# Crear instancia global
config = Config()