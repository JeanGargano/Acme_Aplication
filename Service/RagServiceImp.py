# Service/RAGService.py
import logging
import uuid
from typing import List
from Repository.ChromaDbRepository import ChromaDbRepository
from Repository.GeminiRepository import GeminiRepository
from Model.DocumentModel import Document
from Model.PromptModel import PromptModel  # Asegúrate de tener esto
import fitz  # PyMuPDF

class RAGService:
    def __init__(self, chroma_repo: ChromaDbRepository, gemini_repo: GeminiRepository):
        self.chroma_repo = chroma_repo
        self.gemini_repo = gemini_repo

    def chunk_content(self, content: str, chunk_size: int = 512) -> List[str]:
        return [content[i : i + chunk_size] for i in range(0, len(content), chunk_size)]

    def prepare_documents(self, content: str, file_type: str, chunk_size: int = 1024) -> List[Document]:
        chunks = self.chunk_content(content, chunk_size)
        return [Document(content=chunk, file_type=file_type) for chunk in chunks]

    def save_document(self, file, file_type: str) -> str:
        try:
            if file_type != "pdf":
                raise ValueError("Solo se permiten archivos PDF.")
            content = self._extract_pdf_text(file.read())
            documents = self.prepare_documents(content, file_type)
            self.chroma_repo.save_documents(documents)
            return "Documento PDF procesado y vectores guardados."
        except Exception as e:
            logging.error(f"Error en save_document: {e}")
            return f"Error: {e}"

    def _extract_pdf_text(self, file_bytes: bytes) -> str:
        text = ""
        with fitz.open("pdf", file_bytes) as doc:
            for page in doc:
                text += page.get_text()
        return text

    def generarFormulario(self, prompt: str):
        try:
            results = self.chroma_repo.buscar_documento(prompt)
            prompt_model = PromptModel(prompt=results)
            return self.gemini_repo.generar_reporte(prompt_model)
        except Exception as e:
            logging.error(f"Error en re(): {e}")
            raise
