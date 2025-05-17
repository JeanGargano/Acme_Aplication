#Modelo de datos para Auditor Interno
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
from typing import Annotated

#Forma de mapear objects ids en python
ObjectIdStr = Annotated[str, Field(pattern="^[a-f\d]{24}$")]

class AuditorInternoModel(BaseModel):
    nombre: str
    compañia: str
    usuario: str
    contraseña: str

    #Permite serializar los campos del modelo
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

#Clase para manejar respuestas al logear


