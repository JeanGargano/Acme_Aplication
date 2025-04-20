from typing import Optional, List
from pydantic import BaseModel, Field
from bson import ObjectId
from pymongo import MongoClient
from typing import Annotated

ObjectIdStr = Annotated[str, Field(pattern="^[a-f\d]{24}$")]

class Pregunta(BaseModel):
    nombre: str
    Respuesta: Optional[str] = None
    Evidencia: Optional[str] = None

class Formulario(BaseModel):
    id: ObjectIdStr = Field(alias="_id")
    fecha: str  
    titulo: str
    preguntas: List[Pregunta]
    auditorInterno: ObjectIdStr  # Relación con AuditorInterno
    auditorExterno: ObjectIdStr  # Relación con AuditorExterno
    estado: str
    planAccion: ObjectIdStr #Relacion con plan de accion
    reporte: str