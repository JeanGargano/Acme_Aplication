from configurations import db
from bson import ObjectId
from Model.AuditorE_Model import AuditorExterno

class AuditorExternoRepository:

    def __init__(self):
        self.collection = db["Auditor_externo"]

    def crear_auditor_externo(self, auditorE: AuditorExterno):
        result = self.collection.insert_one(auditorE.dict(by_alias=True))
        return str(result.inserted_id)

    def listar_auditores_externos(self):
        return [AuditorExterno(**doc) for doc in self.collection.find()]

    def listar_auditor_externo_por_id(self, auditor_id: str):
        data = self.collection.find_one({"_id": ObjectId(auditor_id)})
        return AuditorExterno(**data) if data else None


