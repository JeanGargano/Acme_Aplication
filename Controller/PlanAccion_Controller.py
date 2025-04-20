from fastapi import APIRouter, HTTPException
from Model.PlanAccion_Model import PlanDeAccion
from Service.PlanAccion_ServiceImp import PlanDeAccionService

router = APIRouter()
service = PlanDeAccionService()

@router.post("/crear_plan")
def crear_plan(plan: PlanDeAccion):
    plan_dict = plan.dict(by_alias=True)
    plan_id = service.crear(plan_dict)
    return {"id": plan_id}

@router.get("/listar_planes")
def listar_planes():
    return service.obtener_todos()

@router.get("/listar_plan_por_id/{plan_id}")
def listar_plan_por_id(plan_id: str):
    plan = service.obtener_por_id(plan_id)
    if plan:
        return plan
    raise HTTPException(status_code=404, detail="Plan no encontrado")

