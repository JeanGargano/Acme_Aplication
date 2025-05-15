#Modelo de datos para Auditor Externo
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
from typing import Annotated


class AuditorExternoModel(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    nombre: str
    usuario: str
    contraseña: str

    #Permite serializar los campos del modelo
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
