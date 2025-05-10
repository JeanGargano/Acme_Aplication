from pydantic import BaseModel, Field
from bson import ObjectId
from pymongo import MongoClient
from typing import Annotated, List, Optional


class Fase(BaseModel):
    meta: str
    evidencia: str

class PlanDeAccionModel(BaseModel):
    objetivo: str
    etapas: List[Fase]
    auditor_interno: str
    comentario: str = Field("No se han realizado comentarios")
    estado: str = Field(default="pendiente") 

class Actualizar_plan(BaseModel):
    id: str
    comentario: str
    estado: str
    

