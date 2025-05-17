#Endpoints para Gemini
from fastapi import APIRouter, Depends, HTTPException
from Service.GeminiServiceImp import GeminiServiceImp
from Model.PromptModel import PromptModel, PromptDocumento

router = APIRouter()

@router.post("/generar_reporte")
def generar_reporte(prompt: PromptModel, service: GeminiServiceImp = Depends()):
    try:
        return service.generar_reporte(prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

