# Controller/RAGController.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from Service.RagServiceImp import RAGService
from pydantic import BaseModel
from Model.PromptModel import PromptDocumento

router = APIRouter()


@router.post("/preguntar-documento")
async def generar_formulario(data: PromptDocumento, service: RAGService = Depends()):
    try:
        respuesta = await service.generarFormulario(data.prompt)
        return {"respuesta": respuesta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/subir-documento")
async def subir_documento(
    file: UploadFile = File(...),
    file_type: str = Form(...),
    service: RAGService = Depends()
):
    try:
        resultado = await service.save_document(file, file_type)
        return {"mensaje": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
