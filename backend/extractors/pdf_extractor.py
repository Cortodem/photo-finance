"""
PASO 3: Extractor de PDF
Clase para extraer texto y metadatos de archivos PDF
"""
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import PyPDF2


class PDFExtractor:
    """
    Extractor de contenido y metadatos de archivos PDF
    """
    
    def __init__(self, pdf_path: Path):
        """
        Inicializa el extractor con la ruta del PDF
        
        Args:
            pdf_path: Ruta al archivo PDF
        """
        self.pdf_path = Path(pdf_path)
        self.reader = None
        self._load_pdf()
    
    def _load_pdf(self):
        """Carga el archivo PDF"""
        try:
            with open(self.pdf_path, 'rb') as file:
                self.reader = PyPDF2.PdfReader(file)
                # Forzar la carga completa
                _ = len(self.reader.pages)
        except Exception as e:
            raise ValueError(f"Error al cargar el PDF '{self.pdf_path}': {str(e)}")
    
    def extract_metadata(self) -> Dict[str, Optional[str]]:
        """
        Extrae metadatos del PDF
        
        Returns:
            Dict con metadatos (titulo, autor, fecha_creacion)
        """
        metadata = {
            'titulo': None,
            'autor': None,
            'fecha_creacion': None
        }
        
        try:
            if self.reader.metadata:
                # Título
                if self.reader.metadata.title:
                    metadata['titulo'] = self.reader.metadata.title
                
                # Autor
                if self.reader.metadata.author:
                    metadata['autor'] = self.reader.metadata.author
                
                # Fecha de creación
                if self.reader.metadata.creation_date:
                    try:
                        metadata['fecha_creacion'] = self.reader.metadata.creation_date
                    except:
                        metadata['fecha_creacion'] = None
        except Exception as e:
            print(f"Advertencia: Error al extraer metadatos: {str(e)}")
        
        return metadata
    
    def get_num_pages(self) -> int:
        """
        Obtiene el número de páginas del PDF
        
        Returns:
            int: Número de páginas
        """
        return len(self.reader.pages)
    
    def extract_text_from_page(self, page_num: int) -> str:
        """
        Extrae el texto de una página específica
        
        Args:
            page_num: Número de página (0-indexed)
        
        Returns:
            str: Texto extraído de la página
        """
        try:
            page = self.reader.pages[page_num]
            text = page.extract_text()
            return text.strip() if text else ""
        except Exception as e:
            print(f"Error al extraer texto de página {page_num + 1}: {str(e)}")
            return ""
    
    def extract_all_pages(self) -> List[Dict[str, any]]:
        """
        Extrae el texto de todas las páginas
        
        Returns:
            Lista de diccionarios con número de página y contenido
        """
        pages = []
        num_pages = self.get_num_pages()
        
        for page_num in range(num_pages):
            content = self.extract_text_from_page(page_num)
            pages.append({
                'numero_pagina': page_num + 1,  # 1-indexed para el usuario
                'contenido': content
            })
        
        return pages
    
    def extract_full_document(self) -> Dict:
        """
        Extrae toda la información del documento
        
        Returns:
            Dict con toda la información del documento
        """
        metadata = self.extract_metadata()
        pages = self.extract_all_pages()
        
        return {
            'nombre_archivo': self.pdf_path.name,
            'ruta_archivo': str(self.pdf_path.absolute()),
            'num_paginas': self.get_num_pages(),
            'titulo': metadata['titulo'],
            'autor': metadata['autor'],
            'fecha_creacion': metadata['fecha_creacion'],
            'paginas': pages
        }


def extract_pdf(pdf_path: Path) -> Dict:
    """
    Función auxiliar para extraer un PDF
    
    Args:
        pdf_path: Ruta al archivo PDF
    
    Returns:
        Dict con la información extraída
    """
    extractor = PDFExtractor(pdf_path)
    return extractor.extract_full_document()