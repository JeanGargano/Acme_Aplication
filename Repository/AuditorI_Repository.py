from configurations import db
from bson import ObjectId
from Model.AuditorI_Model import AuditorInterno


class AuditorInternoRepository:

    def __init__(self):
        self.collection = db["Auditor_interno"]

    def crear_auditor_interno(self, auditor_inerno: AuditorInterno):
        result = self.collection.insert_one(auditor_inerno.dict(by_alias = True))
        return str(result.inserted_id)

    def listar_auditores_internos(self):
        return [AuditorInterno(**doc) for doc in self.collection.find()]

    def listar_auditores_internos_por_id(self, auditorI_id: str):
        data = self.collection.find_one({"_id": ObjectId(auditorI_id)})
        return AuditorInterno(**data) if data else None
    


