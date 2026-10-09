"""
PASO 4: Almacenamiento - Base de Datos
Clase para guardar datos extraídos en base de datos usando SQLAlchemy
"""
from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from models import Documento, Pagina, DatabaseManager


class DatabaseStorage:
    """
    Almacena documentos extraídos en base de datos
    """
    
    def __init__(self, database_manager: DatabaseManager):
        """
        Inicializa el almacenamiento en base de datos
        
        Args:
            database_manager: Gestor de base de datos
        """
        self.db_manager = database_manager
        self.db_manager.create_tables()
    
    def save_document(self, document_data: Dict) -> int:
        """
        Guarda un documento en la base de datos
        
        Args:
            document_data: Diccionario con los datos del documento
        
        Returns:
            int: ID del documento guardado
        """
        session = self.db_manager.get_session()
        
        try:
            # Crear documento
            documento = Documento(
                nombre_archivo=document_data['nombre_archivo'],
                ruta_archivo=document_data['ruta_archivo'],
                num_paginas=document_data['num_paginas'],
                autor=document_data.get('autor'),
                titulo=document_data.get('titulo'),
                fecha_creacion=document_data.get('fecha_creacion'),
                fecha_procesamiento=datetime.utcnow()
            )
            
            # Agregar páginas
            for page_data in document_data['paginas']:
                pagina = Pagina(
                    numero_pagina=page_data['numero_pagina'],
                    contenido=page_data['contenido']
                )
                documento.paginas.append(pagina)
            
            # Guardar en base de datos
            session.add(documento)
            session.commit()
            
            doc_id = documento.id
            print(f"✓ Documento guardado en BD con ID: {doc_id}")
            
            return doc_id
        
        except Exception as e:
            session.rollback()
            raise Exception(f"Error al guardar documento: {str(e)}")
        
        finally:
            session.close()
    
    def get_document(self, doc_id: int) -> Optional[Dict]:
        """
        Obtiene un documento por su ID
        
        Args:
            doc_id: ID del documento
        
        Returns:
            Dict con los datos del documento o None si no existe
        """
        session = self.db_manager.get_session()
        
        try:
            documento = session.query(Documento).filter(Documento.id == doc_id).first()
            
            if documento:
                return documento.to_dict()
            return None
        
        finally:
            session.close()
    
    def list_documents(self) -> List[Dict]:
        """
        Lista todos los documentos almacenados
        
        Returns:
            Lista de diccionarios con información básica de documentos
        """
        session = self.db_manager.get_session()
        
        try:
            documentos = session.query(Documento).all()
            
            return [{
                'id': doc.id,
                'nombre_archivo': doc.nombre_archivo,
                'num_paginas': doc.num_paginas,
                'titulo': doc.titulo,
                'autor': doc.autor,
                'fecha_procesamiento': doc.fecha_procesamiento.isoformat()
            } for doc in documentos]
        
        finally:
            session.close()
    
    def search_by_filename(self, filename: str) -> List[Dict]:
        """
        Busca documentos por nombre de archivo
        
        Args:
            filename: Nombre del archivo a buscar
        
        Returns:
            Lista de documentos encontrados
        """
        session = self.db_manager.get_session()
        
        try:
            documentos = session.query(Documento).filter(
                Documento.nombre_archivo.like(f'%{filename}%')
            ).all()
            
            return [doc.to_dict() for doc in documentos]
        
        finally:
            session.close()
    
    def delete_document(self, doc_id: int) -> bool:
        """
        Elimina un documento y sus páginas
        
        Args:
            doc_id: ID del documento
        
        Returns:
            bool: True si se eliminó, False si no existía
        """
        session = self.db_manager.get_session()
        
        try:
            documento = session.query(Documento).filter(Documento.id == doc_id).first()
            
            if documento:
                session.delete(documento)
                session.commit()
                print(f"✓ Documento {doc_id} eliminado")
                return True
            
            return False
        
        except Exception as e:
            session.rollback()
            raise Exception(f"Error al eliminar documento: {str(e)}")
        
        finally:
            session.close()