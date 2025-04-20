from fastapi import APIRouter, HTTPException
from Model.AuditorI_Model import AuditorInterno
from Service.AuditorIServiceImp import AuditorInternoService

router = APIRouter()
service = AuditorInternoService()

@router.post("/crear_auditor_interno")
def crear_auditor_interno(auditor: AuditorInterno):
    auditor_dict = auditor.dict(by_alias=True)
    auditor_id = service.crear(auditor_dict)
    return {"id": auditor_id}

@router.get("/listar_auditores_internos")
def listar_auditores_internos():
    return service.obtener_todos()

@router.get("/listar_auditor_interno_por_id/{auditor_id}")
def listar_auditor_interno_por_id(auditor_id: str):
    auditor = service.obtener_por_id(auditor_id)
    if auditor:
        return auditor
    raise HTTPException(status_code=404, detail="Auditor no encontrado")

