from fastapi import APIRouter, HTTPException
from Model.Formulario_Model import Formulario
from Service.Formulario_ServiceImp import FormularioService

router = APIRouter()
service = FormularioService()

@router.post("/crear_Formulario")
def crear_formulario(formulario: Formulario):
    formulario_id = service.crear(formulario)
    return {"id": formulario_id}

@router.get("/listar_formularios")
def listar_formularios():
    return service.listar()

@router.get("/listar_formulario_por_id/{formulario_id}")
def listar_formulario_por_id(formulario_id: str):
    formulario = service.obtener_por_id(formulario_id)
    if formulario is None:
        raise HTTPException(status_code=404, detail="Formulario no encontrado")
    return formulario



