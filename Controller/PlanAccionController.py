#Endpoints para Plan de Accion
from fastapi import APIRouter, Depends, HTTPException, Query
from Model.PlanAccionModel import PlanDeAccionCreate, Actualizar_estado_comentario, EvidenciaRequest
from Service.PlanAccionServiceImp import PlanDeAccionServiceImp
from typing import List
import logging
router = APIRouter()

# Crear plan de acción
@router.post("/guardar_plan")
def guardar_plan(
    plan: PlanDeAccionCreate,
    service: PlanDeAccionServiceImp = Depends()
):
    try:
        res = service.guardar_plan(plan)
        if res:
            return {"mensaje": "Se ha creado el plan de acción exitosamente"}
        else:
            raise HTTPException(status_code=400, detail="No se ha podido crear el plan de acción")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Error al crear el plan: {str(e)}")
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al crear el plan.")

# Listar planes por auditor interno
@router.get("/listar_plan_por_auditor_interno")
def listar_plan_por_auditor_interno(
    auditorI_id: str = Query(...),
    service: PlanDeAccionServiceImp = Depends()
):
    try:
        return service.listar_plan_por_auditor_interno(auditorI_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Error al traer los planes de acción: {str(e)}")
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al traer los planes")

logger = logging.getLogger(__name__)

#Listar plan por id
@router.get("/listar_plan_por_id")
def listar_plan_por_id(
    plan_id: str = Query(...),
    service: PlanDeAccionServiceImp = Depends()
):
    try:
        return service.listar_plan_por_id(plan_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al buscar el plan por ID")

# Listar planes pendientes por auditor interno
@router.get("/listar_planes_pendientes_auditor_interno")
def listar_planes_pendientes_auditor_interno(
    auditorI_id: str = Query(...),
    service: PlanDeAccionServiceImp = Depends()
):
    try:
        logger.info(f"Buscando planes para auditorI_id: {auditorI_id}")
        result = service.listar_planes_pendientes_por_auditor_interno(auditorI_id)
        logger.info(f"Resultado obtenido: {result}")
        return result
    except ValueError as e:
        logger.error(f"Error de valor: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error al traer los planes pendientes: {str(e)}")
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno al traer los planes pendientes")
    
#Actualizar Comentario y estado
@router.post("/actualizar_comentario_estado")
def actualizar_comentario_estado(
    Data: Actualizar_estado_comentario,
    service: PlanDeAccionServiceImp = Depends()
):
    try:
        actualizado = service.actualizar_estado_comentario(Data)
        if not actualizado:
            raise HTTPException(status_code=404, detail="Plan de acción no encontrado")
        return {"message": "Plan actualizado correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al actualizar el plan")

#Añadir evidencias   
@router.post("/añadir_evidencias")
async def añadir_evidencias(
    data: EvidenciaRequest,
    service: PlanDeAccionServiceImp = Depends()):
    actualizado = service.añadir_evidencias(data.plan_id, data.evidencias)
    if not actualizado:
        raise HTTPException(status_code=404, detail="No se pudo actualizar el plan de acción")
    return {"mensaje": "Evidencias actualizadas correctamente"}

#Enviar Plan de Accion al auditor enterno
@router.post("/enviar_a_auditorExterno")
async def enviar_plan_a_auditorExterno(
    plan_id: str = Query(...),
    service: PlanDeAccionServiceImp = Depends()
):
    planEnviado = service.enviar_plan_a_auditorExterno(plan_id)
    if not planEnviado:
        raise HTTPException(status_code=404, detail="No se pudo enviar el plan de acción al auditor Externo")
    return{"mesagge": "Plan enviado exitosamente"}



