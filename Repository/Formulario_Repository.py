from configurations import db
from bson import ObjectId
from Model.Formulario_Model import Formulario

class FormularioRepository:

    def __init__(self):
        self.collection = db["Formulario"]

    def crear_formulario(self, formulario: Formulario):
        result = self.collection.insert_one(formulario.dict(by_alias=True))
        return str(result.inserted_id)

    def listar_formularios(self):
        return [Formulario(**doc) for doc in self.collection.find()]
    
    def listar_formulario_por_id(self, formulario_id: str):
        data = self.collection.find_one({"_id": ObjectId(formulario_id)})
        return Formulario(**data) if data else None
    




