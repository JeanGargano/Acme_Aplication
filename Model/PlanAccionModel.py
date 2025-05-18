from pydantic import BaseModel, Field
from bson import ObjectId
from pymongo import MongoClient
from typing import Annotated, List, Optional


class Fase(BaseModel):
    meta: str
    evidencia: str = Field("Aun no ha cargado evidencia para esta meta")

class PlanDeAccionModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    objetivo: str
    etapas: List[Fase]
    auditor_interno: str
    comentario: str = Field("No se han realizado comentarios")
    estado: str = Field(default="pendiente")

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

class PlanDeAccionCreate(BaseModel):
    objetivo: str
    etapas: List[Fase]
    auditor_interno: str
    comentario: str = Field("No se han realizado comentarios")
    estado: str = Field(default="pendiente")

class Actualizar_estado_comentario(BaseModel):
    id: str
    comentario: str
    estado: str

class EvidenciaMeta(BaseModel):
    indice_etapa: int  # posición en el array etapas
    evidencia: str

class EvidenciaRequest(BaseModel):
    plan_id: str  # ID del plan de acción
    evidencias: List[EvidenciaMeta]
    

