from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId

class FormularioModel(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    norma: str
    titulo: str
    preguntas: List[str]
