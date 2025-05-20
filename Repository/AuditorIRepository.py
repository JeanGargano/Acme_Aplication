#Clase de repositorio, tiene comunicacón directa con la base de datos
from configurations import db
from bson import ObjectId
from Model.AuditorIModel import AuditorInternoModel
import bcrypt


class AuditorInternoRepository:

    #Inicializa la instacia de la bd
    def __init__(self):
        self.collection = db["Auditor_interno"]

    # Inserta un auditor interno en la bd
    def crear_auditor_interno(self, auditor_model):
        auditor_dict = auditor_model.dict()
        nombre_usuario = auditor_dict["usuario"]
        #Verificación en la base de datos si ya existe un auditor con el mismo nombre
        if self.collection.find_one({"usuario": nombre_usuario}):
            raise ValueError(f"Ya existe un auditor interno con el nombre de usuario '{nombre_usuario}'.")
        # Hashear la contraseña antes de guardar
        contraseña_plana = auditor_dict["contraseña"]
        hashed = bcrypt.hashpw(contraseña_plana.encode('utf-8'), bcrypt.gensalt())
        
        auditor_dict["contraseña"] = hashed.decode('utf-8')  # guarda como string
        result = self.collection.insert_one(auditor_dict)
        return str(result.inserted_id)

    # Trae los auditores internos de la bd
    def listar_auditores_internos(self):
        return [AuditorInternoModel(**{**doc, "_id": str(doc["_id"])}) for doc in self.collection.find()]

    #Buscar Auditor interno por usuario
    def buscar_auditor_interno_por_usuario(self, usuario: str):
        return self.collection.find_one({"usuario": usuario})


    def eliminar_auditor_interno(self, id: str) -> bool:
        result = self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0



