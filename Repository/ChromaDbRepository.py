# Repository/ChromaDbRepository.py
import uuid
import logging
from typing import List
from Model.DocumentModel import Document
from Repository.GeminiRepository import GeminiRepository

class ChromaDbRepository:
    def __init__(self, chroma_client, gemini_repository: GeminiRepository, collection_name="documents"):
        self.chroma_client = chroma_client
        self.collection_name = collection_name
        self.embedding_function = gemini_repository

    async def save_documents(self, documents: List[Document]) -> None:
        try:
            collection = self.chroma_client.get_or_create_collection(self.collection_name)
            ids = [str(uuid.uuid4()) for _ in documents]
            embeddings = await self.embedding_function.generate_embeddings_parallel(
                [doc.content for doc in documents]
            )
            metadatas = [{"file_type": doc.file_type, "content": doc.content} for doc in documents]
            collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas)
            logging.info(f"{len(documents)} documentos almacenados exitosamente en ChromaDB.")
        except Exception as e:
            logging.error(f"Error al almacenar documentos en ChromaDB: {e}", exc_info=True)

    async def buscar_documento(self, prompt: str):
        try:
            collection = self.chroma_client.get_or_create_collection(self.collection_name)
            vector = await self.embedding_function.generar_embedding(prompt)
            resultados = collection.query(query_embeddings=[vector], n_results=5)
            contenidos = [match["metadata"]["content"] for match in resultados["documents"][0]]
            return [{"pregunta": prompt, "respuesta": c} for c in contenidos]
        except Exception as e:
            logging.error(f"Error al buscar en ChromaDB: {e}")
            raise
