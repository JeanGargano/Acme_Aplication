#Endpoints para Auditor Interno
from fastapi import APIRouter, Depends, HTTPException, Query
from Model.AuditorIModel import AuditorInternoCreate
from Model.LoginRequest import LoginRequest
from Model.AuditorResponse import AuditorResponse
from Service.AuditorIServiceImp import AuditorInternoServiceImp
from typing import List, Optional

router = APIRouter()

#Controlador para crear auditor interno
@router.post("/crear_auditor_interno")
def crear_auditor_interno(
    auditor_interno: AuditorInternoCreate,
    service: AuditorInternoServiceImp = Depends()
):
    try:
        auditor_I = service.crear_auditor_interno(auditor_interno)
        return "Auditor interno creado con exito", auditor_I
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error al crear el auditor interno.")

#Controlador para listar auditores internos
@router.get("/listar_auditores_internos")
def listar_auditores_internos(service: AuditorInternoServiceImp = Depends()):
    try:
        return service.listar_auditores_internos()
    except Exception:
        raise HTTPException(status_code=500, detail="Error al obtener auditores internos.")

#Controlador para logear Auditor interno
@router.post("/logear_auditor_interno")
def logear_auditor_interno(
    datos: LoginRequest,
    service: AuditorInternoServiceImp = Depends()
):
    auditor = service.logear_auditor_interno(datos.usuario, datos.contraseña)
    if auditor is None:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return auditor

#Controaldor para eliminar Auditor externo
@router.delete("/eliminar_auditor_interno")
def eliminar_auditor_interno(
    usuario: str = Query(...),
    service: AuditorInternoServiceImp = Depends()
):
    try:
        eliminado = service.eliminar_auditor_interno(usuario)
        if eliminado:
            return {"mensaje": f"Audito interno con usuario {usuario} eliminado exitosamente"}
        else:
            raise HTTPException(status_code=404, detail="Auditor interno no encontrado")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al eliminar el Auditor interno")

