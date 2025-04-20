from fastapi import APIRouter, HTTPException
from Model.AuditorE_Model import AuditorExterno
from Service.AuditorE_ServiceImp import AuditorExternoService

router = APIRouter()
service = AuditorExternoService()

@router.post("/crear_auditor_externo")
def crear_auditor_externo(auditor: AuditorExterno):
    auditor_dict = auditor.dict(by_alias=True)
    auditor_id = service.crear(auditor_dict)
    return {"id": auditor_id}

@router.get("/listar_auditores_externos")
def listar_auditores_externos():
    return service.obtener_todos()

@router.get("/listar_auditor_externo_por_id/{auditor_id}")
def listar_auditor_externo_por_id(auditor_id: str):
    auditor = service.obtener_por_id(auditor_id)
    if auditor:
        return auditor
    raise HTTPException(status_code=404, detail="Auditor no encontrado")


