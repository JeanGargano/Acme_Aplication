#Endpoints para Respuesta
from fastapi import APIRouter, Depends, HTTPException
from Model.RespuestaModel import RespuestaModel
from Service.RespuestaServiceImp import RespuestaServiceImp

router = APIRouter()

@router.post("/crear_respuesta")
def crear_respuesta(
    respuesta: RespuestaModel,
    service: RespuestaServiceImp = Depends()
):
    try:
        service.crear_respuesta(respuesta)
        return {"mensaje": "Respuestas enviadas con éxito"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error al crear la respuesta.")
