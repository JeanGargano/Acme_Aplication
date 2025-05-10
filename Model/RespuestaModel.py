from typing import Optional, List
from pydantic import BaseModel, Field
from bson import ObjectId
from pymongo import MongoClient
from typing import Annotated

ObjectIdStr = Annotated[str, Field(pattern="^[a-f\d]{24}$")]

class Pregunta(BaseModel):
    pregunta: str
    respuesta: str
    evidencia: str

class RespuestaModel(BaseModel):
    titulo: str
    respuestas: List[Pregunta]
    auditorInterno: ObjectIdStr  # Relación con AuditorInterno
    idFormulario: ObjectIdStr # Relación con Formulario

    #Permite serializar los campos del modelo
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
    