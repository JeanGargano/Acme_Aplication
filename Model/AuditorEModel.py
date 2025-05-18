#Modelo de datos para Auditor Externo
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
from typing import Annotated, List


class AuditorExternoModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    nombre: str
    usuario: str
    contraseña: str
    planesAsignados: Optional[List[str]] = Field(default_factory=list)
    #Permite serializar los campos del modelo
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class AuditorExternoCreate(BaseModel):
    nombre: str
    usuario: str
    contraseña: str
    planesAsignados: List[str] = Field(default_factory=list)