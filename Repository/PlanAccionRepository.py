#Clase de repositorio, tiene comunicacón directa con la base de datos
from configurations import db
from bson import ObjectId
from Model.PlanAccionModel import PlanDeAccionCreate, EvidenciaMeta
from bson.errors import InvalidId
from typing import List
import logging
logger = logging.getLogger(__name__)


class PlanAccionRepository:
    #Inicializa la instacia de la bd 
    def __init__(self):
        self.collection = db["Plan_de_accion"]

    # Obtener plan por id
    def obtener_plan_por_id(self, plan_id: str):
        return self.collection.find_one({"_id": ObjectId(plan_id)})

    # Inserta un plan en la base de datos
    def guardar_plan(self, plan_de_accion:PlanDeAccionCreate):
        result = self.collection.insert_one(plan_de_accion.dict(by_alias=True))
        return str(result)

    # Trae un plan de la bd por su id
    def listar_planes_por_auditor_interno(self, auditorI_id: str):
        auditorI_id = auditorI_id.strip()
        data_cursor = self.collection.find({"auditor_interno": auditorI_id})
        data_list = []
        for doc in data_cursor:
            doc["_id"] = str(doc["_id"]) 
            data_list.append(doc)

        if not data_list:
            raise ValueError(f"No se encontraron planes de acción para el auditor con ID: {auditorI_id}")
        return data_list

    # Trae los planes de la BD por su auditor interno y cuyo estado sea 'pendiente'
    def listar_planes_pendientes_por_auditor_interno(self, auditorI_id: str):
        auditorI_id = auditorI_id.strip()
        logger.info(f"Buscando en MongoDB con auditorI_id: '{auditorI_id}'")
        
        try:
            data_cursor = self.collection.find({
                "auditor_interno": auditorI_id,
                "estado": "pendiente"
            })
            data_list = list(data_cursor)  # Convertir cursor a lista inmediatamente
            logger.info(f"Documentos encontrados: {len(data_list)}")
            
            for doc in data_list:
                doc["_id"] = str(doc["_id"])
            
            if not data_list:
                logger.warning("No se encontraron documentos")
                raise ValueError(f"No se encontraron planes de acción pendientes para el auditor con ID: {auditorI_id}")
                
            return data_list
        except Exception as e:
            logger.error(f"Error al consultar MongoDB: {str(e)}", exc_info=True)
            raise
    
    #Añade un comentario al plan de accion y le cambia el estado
    def actualizar_estado_comentario(self, id: str, comentario: str, estado: str):
        try:
            result = self.collection.update_one(
                {"_id": ObjectId(id)},
                {"$set": {"comentario": comentario, "estado": estado}}  
            )
            return result.modified_count > 0
        except Exception as e:
            raise e

    #Añade nuevas evidencias al plan de accion guardado en la base de datos  
    def añadir_evidencias(self, plan_id: str, evidencias: List[EvidenciaMeta]) -> bool:
        updates = {}
        for evidencia in evidencias:
            key = f"etapas.{evidencia.indice_etapa}.evidencia"
            updates[key] = evidencia.evidencia.strip()
        result = self.collection.update_one(
            {"_id": ObjectId(plan_id)},
            {"$set": updates}
        )
        return result.modified_count > 0
    
    def asignar_plan(self, auditorE_id: str, plan_id: str) -> bool:
        result = self.collection.update_one(
            {"_id": ObjectId(auditorE_id)},
            {"$addToSet": {"planesAsignados": plan_id}} 
        )
        return result.modified_count > 0


