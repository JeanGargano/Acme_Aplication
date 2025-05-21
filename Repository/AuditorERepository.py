#Clase de repositorio, tiene comunicacón directa con la base de datos
from configurations import db
from bson import ObjectId
from Model.AuditorEModel import AuditorExternoModel, AuditorExternoCreate
import bcrypt

class AuditorExternoRepository:

    #Inicializa la instacia de la bd
    def __init__(self):
        self.collection = db["Auditor_externo"]

     # Inserta un auditor externo en la bd
    def crear_auditor_externo(self, auditor_model: AuditorExternoCreate) -> str:
        try:
            auditor_dict = auditor_model.model_dump(exclude_unset=True)
        except AttributeError:
            auditor_dict = auditor_model.dict(exclude_unset=True)
        
        if "planesAsignados" not in auditor_dict or auditor_dict["planesAsignados"] is None:
            auditor_dict["planesAsignados"] = []
        
        nombre_usuario = auditor_dict["usuario"]

        if self.collection.find_one({"usuario": nombre_usuario}):
            raise ValueError(f"Ya existe un auditor externo con el nombre de usuario '{nombre_usuario}'.")
        
        contraseña_plana = auditor_dict["contraseña"]
        hashed = bcrypt.hashpw(contraseña_plana.encode('utf-8'), bcrypt.gensalt())
        auditor_dict["contraseña"] = hashed.decode('utf-8')

        result = self.collection.insert_one(auditor_dict)
        return str(result.inserted_id)


    #Trae los auditores externos de la bd
    def listar_auditores_externos(self):
        return [AuditorExternoModel(**{**doc, "_id": str(doc["_id"])}) for doc in self.collection.find()]
    
    #Buscar Auditor Externo por usuario
    def buscar_auditor_externo_por_usuario(self, usuario: str):
        return self.collection.find_one({"usuario": usuario})

    
    def asignar_plan(self, auditorE_id: str, auditorI_id: str) -> bool:
        result = self.collection.update_one(
            {"_id": ObjectId(auditorE_id)},
            {"$addToSet": {"planesAsignados": auditorI_id}}  # evita duplicados
        )
        return result.modified_count > 0
    
    def eliminar_auditor_externo(self, usuario: str) -> bool:
        result = self.collection.delete_one({"usuario": (usuario)})
        return result.deleted_count > 0





