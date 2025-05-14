from typing import List, Optional
from pydantic import BaseModel, Field

class FormularioModel(BaseModel):
    id: Optional[str] = Field(alias="_id")
    norma: str
    titulo: str
    preguntas: List[str]
