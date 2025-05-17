from pydantic import BaseModel, HttpUrl
from typing import List

class Item(BaseModel):
    pregunta: str
    respuesta: str
    evidencia: str 

class PromptModel(BaseModel):
    prompt: List[Item]


class PromptDocumento(BaseModel):
    prompt: str