#Clase de repositorio, tiene comunicacón directa con la base de datos
from configurations import db
from bson import ObjectId
from Model.RespuestaModel import RespuestaModel

class RespuestaRepository:

    #Inicializa la instacia de la bd
    def __init__(self):
        self.collection = db["Respuesta"]

    #Inserta las respuestas de un formulario en la bd
    def crear_respuesta(self, respuesta: RespuestaModel):
        result = self.collection.insert_one(respuesta.dict(by_alias=True))
        return str(result)

    
    
    




