from configurations import db
from bson import ObjectId
from Model.PlanAccion_Model import PlanDeAccion


class PlanAccionRepository: 
    def __init__(self):
        self.collection = db["Plan_de_accion"]

    def crear_plan(self, plan_de_accion:PlanDeAccion):
        result = self.collection.insert_one(plan_de_accion.dict(by_alias=True))
        return str(result.inserted_id)

    def listar_planes(self):
        return [PlanDeAccion(**doc) for doc in self.collection.find()]

    def listar_plan_por_id(self, plan_id: str):
        data = self.collection.find_one({"_id": ObjectId(plan_id)})
        return PlanDeAccion(**data) if data else None

