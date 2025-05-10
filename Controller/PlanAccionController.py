#Endpoints para Plan de Accion
from fastapi import APIRouter, Depends, HTTPException, Query
from Model.PlanAccionModel import PlanDeAccionModel, Actualizar_plan
from Service.PlanAccionServiceImp import PlanDeAccionServiceImp
from typing import List

router = APIRouter()

# Crear plan de acción
@router.post("/guardar_plan")
def guardar_plan(
    plan: PlanDeAccionModel,
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
    
#Actualizar estado
@router.post("/actualizar_plan")
def actualizar_plan(
    Data: Actualizar_plan,
    service: PlanDeAccionServiceImp = Depends()
):
    try:
        actualizado = service.actualizar_plan(Data)
        if not actualizado:
            raise HTTPException(status_code=404, detail="Plan de acción no encontrado")
        return {"message": "Plan actualizado correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al actualizar el plan")