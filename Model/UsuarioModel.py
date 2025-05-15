from pydantic import BaseModel
class Usuario(BaseModel):
    nombre: str
    usuario: str
    contraseña: str
    compañia: str
