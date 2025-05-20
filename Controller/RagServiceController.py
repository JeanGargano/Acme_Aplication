from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from Service.RagService import RAGService
from Model.DocumentModel import PromptDocumento
import logging
import os

router = APIRouter()
logger = logging.getLogger(__name__)

# Asegurar que existe el directorio de datos
os.makedirs("Data", exist_ok=True)

@router.post("/generar_formulario")
async def query_document(
    data: PromptDocumento,
    service: RAGService = Depends()
):
    try:
        response = await service.process_query(data.prompt)
        return {"response": response}
    except Exception as e:
        logger.error(f"Query error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    service: RAGService = Depends()
):
    try:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Solo se admiten archivos PDF")
        
        result = await service.process_upload(file)
        return {"message": result}
    except Exception as e:
        logger.error(f"Upload error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))