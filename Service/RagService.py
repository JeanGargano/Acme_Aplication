import os
import logging
import fitz  # PyMuPDF
from typing import List, Optional



from Model.DocumentModel import Document
from Repository.GeminiRepository import GeminiRepository
from Model.FormularioModel import FormularioModel
from Service.FormularioServiceImp import FormularioServiceImp
import json
from fastapi import UploadFile, Depends
from datetime import datetime

logger = logging.getLogger(__name__)

class RAGService:
    def __init__(self, repo: GeminiRepository = Depends(), formulario_service: FormularioServiceImp = Depends()):
        self.gemini_repo = repo
        self.formulario_service = formulario_service
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
                        Por favor, genera un formulario en formato JSON válido con base en la norma "{context}". 
                        El formulario debe cubrir exactamente todas las secciones del lineamiento o norma. Las preguntas deben ir 
                        propuestas con el enfoque de poder ser respondidas con cumple, cumple parcialmente o no cumple. Pero no debes agregar algun campo más,
                        solo debes darme las preguntas segun el siguiente formato, y el titulo extraelo del contexto, no le pongas "ejemplo de ...", ni nada parecido, el nombre 
                        de la norma o el lineamiento se saca del contexto y la descripcion tambien, intenta ser conciso y breve con la descripción.
                        Limita las preguntas a un máximo de 10. Que no se repitan las preguntas e intenta cubrir todos Solo aspectos o secciones de la norma o lineamiento.
                        Debe seguir el siguiente formato:
                        {{
                        "nombre": "Nombre de la norma o lineamiento",
                        "descripcion": "Descripción de qué trata la norma o lineamiento",
                        "tipo": "Lineamiento" o "Norma",
                        "preguntas": ["Pregunta 1", "Pregunta 2", ..., "Pregunta 10"]
                        }}

                        Solo responde con el JSON, sin explicaciones ni texto adicional.
                        """
            formulario_generado = self.gemini_repo.generate_form(prompt, context)

            formulario_model = FormularioModel(**formulario_generado)
            self.formulario_service.crear_formulario(formulario_model)

            self._reset_context()

            return {"message": "Formulario generado y guardado exitosamente", "formulario": formulario_generado}

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

    def _reset_context(self) -> None:
        """Borra Data.txt y metadata.json"""
        with open(self.data_file, "w", encoding="utf-8") as f:
            f.write("")
        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump([], f)
