"""
PASO 2: Modelos de Datos
Define la estructura de datos para documentos y paginas
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Documento(Base):
    """
    Modelo para almacenar informacion de documentos PDF
    """
    __tablename__ = 'documentos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_archivo = Column(String(255), nullable=False)
    ruta_archivo = Column(String(500), nullable=False)
    num_paginas = Column(Integer, nullable=False)
    autor = Column(String(255), nullable=True)
    titulo = Column(String(500), nullable=True)
    fecha_creacion = Column(DateTime, nullable=True)
    fecha_procesamiento = Column(DateTime, default=datetime.utcnow)

    # Relacion con paginas
    paginas = relationship("Pagina", back_populates="documento", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Documento(id={self.id}, nombre='{self.nombre_archivo}', paginas={self.num_paginas})>"

    def to_dict(self):
        """Convierte el documento a diccionario"""
        return {
            'id': self.id,
            'nombre_archivo': self.nombre_archivo,
            'ruta_archivo': self.ruta_archivo,
            'num_paginas': self.num_paginas,
            'autor': self.autor,
            'titulo': self.titulo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_procesamiento': self.fecha_procesamiento.isoformat(),
            'paginas': [pagina.to_dict() for pagina in self.paginas]
        }


class Pagina(Base):
    """
    Modelo para almacenar el contenido de cada pagina del PDF
    """
    __tablename__ = 'paginas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    documento_id = Column(Integer, ForeignKey('documentos.id'), nullable=False)
    numero_pagina = Column(Integer, nullable=False)
    contenido = Column(Text, nullable=False)

    # Relacion con documento
    documento = relationship("Documento", back_populates="paginas")

    def __repr__(self):
        return f"<Pagina(id={self.id}, doc_id={self.documento_id}, num={self.numero_pagina})>"

    def to_dict(self):
        """Convierte la pagina a diccionario"""
        return {
            'id': self.id,
            'numero_pagina': self.numero_pagina,
            'contenido': self.contenido
        }


class DatabaseManager:
    """
    Gestor de la base de datos
    """

    def __init__(self, database_url: str):
        """
        Inicializa el gestor de base de datos

        Args:
            database_url: URL de conexion a la base de datos
        """
        self.engine = create_engine(database_url, echo=False)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        """Crea todas las tablas en la base de datos"""
        Base.metadata.create_all(self.engine)

    def get_session(self):
        """
        Obtiene una nueva sesion de base de datos

        Returns:
            Session: Sesion de SQLAlchemy
        """
        return self.Session()

    def drop_tables(self):
        """Elimina todas las tablas (usar con precaucion)"""
        Base.metadata.drop_all(self.engine)
"""
PASO 2: Modelos de Datos
Define la estructura de datos para documentos y páginas
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Documento(Base):
    """
    Modelo para almacenar información de documentos PDF
    """
    __tablename__ = 'documentos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_archivo = Column(String(255), nullable=False)
    ruta_archivo = Column(String(500), nullable=False)
    num_paginas = Column(Integer, nullable=False)
    autor = Column(String(255), nullable=True)
    titulo = Column(String(500), nullable=True)
    fecha_creacion = Column(DateTime, nullable=True)
    fecha_procesamiento = Column(DateTime, default=datetime.utcnow)
    
    # Relación con páginas
    paginas = relationship("Pagina", back_populates="documento", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Documento(id={self.id}, nombre='{self.nombre_archivo}', paginas={self.num_paginas})>"
    
    def to_dict(self):
        """Convierte el documento a diccionario"""
        return {
            'id': self.id,
            'nombre_archivo': self.nombre_archivo,
            'ruta_archivo': self.ruta_archivo,
            'num_paginas': self.num_paginas,
            'autor': self.autor,
            'titulo': self.titulo,
            'fecha_creacion': self.fecha_creacion.isoformat() if self.fecha_creacion else None,
            'fecha_procesamiento': self.fecha_procesamiento.isoformat(),
            'paginas': [pagina.to_dict() for pagina in self.paginas]
        }


class Pagina(Base):
    """
    Modelo para almacenar el contenido de cada página del PDF
    """
    __tablename__ = 'paginas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    documento_id = Column(Integer, ForeignKey('documentos.id'), nullable=False)
    numero_pagina = Column(Integer, nullable=False)
    contenido = Column(Text, nullable=False)
    
    # Relación con documento
    documento = relationship("Documento", back_populates="paginas")
    
    def __repr__(self):
        return f"<Pagina(id={self.id}, doc_id={self.documento_id}, num={self.numero_pagina})>"
    
    def to_dict(self):
        """Convierte la página a diccionario"""
        return {
            'id': self.id,
            'numero_pagina': self.numero_pagina,
            'contenido': self.contenido
        }


class DatabaseManager:
    """
    Gestor de la base de datos
    """
    
    def __init__(self, database_url: str):
        """
        Inicializa el gestor de base de datos
        
        Args:
            database_url: URL de conexión a la base de datos
        """
        self.engine = create_engine(database_url, echo=False)
        self.Session = sessionmaker(bind=self.engine)
    
    def create_tables(self):
        """Crea todas las tablas en la base de datos"""
        Base.metadata.create_all(self.engine)
    
    def get_session(self):
        """
        Obtiene una nueva sesión de base de datos
        
        Returns:
            Session: Sesión de SQLAlchemy
        """
        return self.Session()
    
    def drop_tables(self):
        """Elimina todas las tablas (usar con precaución)"""
        Base.metadata.drop_all(self.engine)