"""
PASO 4: Almacenamiento - JSON
Clase para guardar datos extraídos en formato JSON
"""
import json
from pathlib import Path
from typing import Dict
from datetime import datetime


class JSONStorage:
    """
    Almacena documentos extraídos en formato JSON
    """
    
    def __init__(self, output_dir: Path):
        """
        Inicializa el almacenamiento JSON
        
        Args:
            output_dir: Directorio donde se guardarán los archivos JSON
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def save_document(self, document_data: Dict) -> Path:
        """
        Guarda un documento en formato JSON
        
        Args:
            document_data: Diccionario con los datos del documento
        
        Returns:
            Path: Ruta al archivo JSON creado
        """
        # Crear nombre de archivo basado en el nombre del PDF
        nombre_base = Path(document_data['nombre_archivo']).stem
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_filename = f"{nombre_base}_{timestamp}.json"
        json_path = self.output_dir / json_filename
        
        # Preparar datos para serialización
        data_to_save = self._prepare_for_json(document_data)
        
        # Guardar archivo JSON
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Documento guardado en JSON: {json_path}")
        return json_path
    
    def _prepare_for_json(self, data: Dict) -> Dict:
        """
        Prepara los datos para serialización JSON
        
        Args:
            data: Datos a preparar
        
        Returns:
            Dict: Datos preparados
        """
        prepared = data.copy()
        
        # Convertir datetime a string
        if prepared.get('fecha_creacion') and isinstance(prepared['fecha_creacion'], datetime):
            prepared['fecha_creacion'] = prepared['fecha_creacion'].isoformat()
        
        # Agregar timestamp de procesamiento
        prepared['fecha_procesamiento'] = datetime.now().isoformat()
        
        return prepared
    
    def load_document(self, json_path: Path) -> Dict:
        """
        Carga un documento desde un archivo JSON
        
        Args:
            json_path: Ruta al archivo JSON
        
        Returns:
            Dict: Datos del documento
        """
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def list_documents(self) -> list:
        """
        Lista todos los documentos JSON almacenados
        
        Returns:
            Lista de rutas a archivos JSON
        """
        return list(self.output_dir.glob('*.json'))