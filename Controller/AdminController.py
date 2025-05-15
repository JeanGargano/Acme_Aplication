from fastapi import APIRouter, HTTPException
from Service.AdminService import AdminService
from Model.UsuarioModel import Usuario

router = APIRouter()
servicio_cambio = AdminService()


@router.put("/cambiar")
def cambiar_auditor(data: Usuario):
    try:
        nuevo_id = servicio_cambio.cambiar_tipo_auditor(data)
        return {"mensaje": "Auditor cambiado exitosamente", "nuevo_id": str(nuevo_id)}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
