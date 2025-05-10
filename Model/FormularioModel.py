from typing import List
from pydantic import BaseModel

class FormularioModel(BaseModel):
    norma: str
    titulo: str
    preguntas: List[str]
