import os
import logging
import fitz  # PyMuPDF
from typing import List, Optional
from Model.DocumentModel import Document
from Repository.GeminiRepository import GeminiRepository
import json
from fastapi import UploadFile, Depends
from datetime import datetime

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self, repo: GeminiRepository = Depends()):
        self.gemini_repo = repo
        self.data_file = "Data/Data.txt"
        self.metadata_file = "Data/metadata.json"
        
        # Inicializar archivos si no existen
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w", encoding="utf-8") as f:
                f.write("")
        if not os.path.exists(self.metadata_file):
            with open(self.metadata_file, "w", encoding="utf-8") as f:
                json.dump([], f)

    async def process_query(self, prompt: str) -> dict:
        """Procesa una consulta usando el contexto del archivo Data.txt"""
        try:
            context = self._load_context()
            prompt = f"""
                        Por favor, genera un formulario en formato JSON válido con base en la norma "{prompt}". 
                        El formulario debe tener exactamente 10 preguntas.
                        Debe seguir el siguiente formato:
                        {{
                        "nombre": "Nombre de la norma",
                        "descripcion": "Descripción de qué trata la norma",
                        "tipo": "lineamiento" o "norma",
                        "preguntas": ["Pregunta 1", "Pregunta 2", ..., "Pregunta 10"]
                        }}

                        Solo responde con el JSON, sin explicaciones ni texto adicional.
                        """
            return self.gemini_repo.generate_form(prompt, context)
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            raise

    async def process_upload(self, file: UploadFile) -> str:
        """Procesa y almacena un archivo PDF en Data.txt"""
        try:
            content = await self._extract_text(file)
            self._save_to_data_file(content, file.filename)
            return f"Documento {file.filename} procesado y almacenado correctamente"
        except Exception as e:
            logger.error(f"Error processing upload: {str(e)}")
            raise

    def _load_context(self) -> str:
        """Carga el contexto desde Data.txt"""
        with open(self.data_file, "r", encoding="utf-8") as f:
            return f.read()

    def _save_to_data_file(self, content: str, filename: str) -> None:
        """Guarda el contenido en Data.txt y actualiza metadatos"""
        with open(self.data_file, "a", encoding="utf-8") as f:
            f.write(f"\n\n--- Documento: {filename} ---\n{content}")
        
        # Actualizar metadatos
        with open(self.metadata_file, "r+", encoding="utf-8") as f:
            metadata = json.load(f)
            metadata.append({
                "filename": filename,
                "length": len(content),
                "timestamp": datetime.now().isoformat()
            })
            f.seek(0)
            json.dump(metadata, f, indent=2)

    async def _extract_text(self, file: UploadFile) -> str:
        """Extrae texto de un PDF"""
        content = await file.read()
        with fitz.open(stream=content, filetype="pdf") as doc:
            return "\n".join([page.get_text() for page in doc])