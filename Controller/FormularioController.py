#Endpoints para formulario
from fastapi import APIRouter, Depends, HTTPException, Query
from Model.FormularioModel import FormularioModel
from Service.FormularioServiceImp import FormularioServiceImp
from typing import List

router = APIRouter()

# Controlador para crear formulario
@router.post("/crear_formulario")
def crear_formulario(
    formulario: FormularioModel,
    service: FormularioServiceImp = Depends()
):
    try:
        form = service.crear_formulario(formulario)
        if form:
            return {f"fomulario creado exitosamente"}
        else:
            raise HTTPException(status_code=500, detail="Error en el servicio")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al crear el formulario")

# Controlador para listar formularios
@router.get("/listar_formularios",)
def listar_formularios(service: FormularioServiceImp = Depends()):
    try:
        return service.listar_formularios()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

# Controlador para listar formulario por norma
@router.get("/listar_por_nombre")
def listar_formulario_por_nombre(
    nombre: str = Query(...),
    service: FormularioServiceImp = Depends()
):  
    try:
        return service.listar_formulario_por_nombre(nombre)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    

# Controlador para eliminar un formulario por ID
@router.delete("/eliminar_formulario")
def eliminar_formulario(
    id: str = Query(...),
    service: FormularioServiceImp = Depends()):
    try:
        eliminado = service.eliminar_formulario_por_id(id)
        if eliminado:
            return {"mensaje": f"Formulario con ID {id} eliminado exitosamente"}
        else:
            raise HTTPException(status_code=404, detail="Formulario no encontrado")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al eliminar el formulario")


