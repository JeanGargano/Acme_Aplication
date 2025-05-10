#Clase de repositorio, tiene comunicacón directa con la base de datos
from configurations import db
from bson import ObjectId
from Model.PlanAccionModel import PlanDeAccionModel
from bson.errors import InvalidId


class PlanAccionRepository:
    #Inicializa la instacia de la bd 
    def __init__(self):
        self.collection = db["Plan_de_accion"]

    #Inserta un plan en la base de datos
    def guardar_plan(self, plan_de_accion:PlanDeAccionModel):
        result = self.collection.insert_one(plan_de_accion.dict(by_alias=True))
        return str(result)

    #Trae un plan de la bd por su id
    def listar_planes_por_auditor_interno(self, auditorI_id: str):
        auditorI_id = auditorI_id.strip()  # Asegura que no vengan espacios
        # Proyección para excluir _id
        data_cursor = self.collection.find(
            {"auditor_interno": auditorI_id},
            {"_id": 0}  # <--- Aquí excluimos el _id
        )
        data_list = list(data_cursor)

        if not data_list:
            raise ValueError(f"No se encontraron planes de acción para el auditor con ID: {auditorI_id}")
        return data_list

    
    #Actualiza el plan de accion
    def actualizar_plan(self, id: str, comentario: str, estado: str):
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": {"comentario": comentario, "estado": estado}}  
            )
            return result.modified_count > 0
        except Exception as e:
            raise e

