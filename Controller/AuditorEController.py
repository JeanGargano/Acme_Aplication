#Endpoints para Auditor Externo
from fastapi import APIRouter, Depends, HTTPException, Query
from Model.AuditorEModel import AuditorExternoCreate
from Model.AuditorResponse import AuditorResponse
from Service.AuditorEServiceImp import AuditorExternoServiceImp
from typing import List, Optional
from Model.LoginRequest import LoginRequest

router = APIRouter()
 
# Crear auditor externo
@router.post("/crear_auditor_externo")
def crear_auditor_externo(
    auditor_externo: AuditorExternoCreate,
    service: AuditorExternoServiceImp = Depends()
):
    try:
        auditor_E = service.crear_auditor_externo(auditor_externo)
        return {"mensaje": "Auditor Externo creado con éxito", "auditor": auditor_E}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear auditor externo: {str(e)}")

# Listar todos los auditores externos
@router.get("/listar_auditores_externos")
def listar_auditores_externos(service: AuditorExternoServiceImp = Depends()):
    try:
        return service.listar_auditores_externos()
    except Exception:
        raise HTTPException(status_code=500, detail="Error al obtener auditores externos.")

#Controlador para logear Auditor externo
@router.post("/logear_auditor_externo")
def logear_auditor_externo(
    datos: LoginRequest,
    service: AuditorExternoServiceImp = Depends()
):
    auditorE = service.logear_auditor_externo(datos.usuario, datos.contraseña)
    if auditorE is None:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return auditorE
