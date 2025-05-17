from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId

class FormularioModel(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    nombre: str
    descripcion: str
    tipo: str
    preguntas: List[str]
