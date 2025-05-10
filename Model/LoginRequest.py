#Modelo para manejar Login
from pydantic import BaseModel
class LoginRequest(BaseModel):
    usuario: str
    contraseña: str