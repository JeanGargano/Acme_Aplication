#Clase que implementa los metodos Abstractos de la interfaz, se comunica con el repositorio
from Service.IPlanAccionService import IPlanAccionService
from Repository.PlanAccionRepository import PlanAccionRepository
from Repository.AuditorERepository import AuditorExternoRepository
from Model.PlanAccionModel import PlanDeAccionModel, PlanDeAccionCreate, Actualizar_estado_comentario, EvidenciaMeta
from typing import List
from fastapi import Depends
import logging
from bson import ObjectId
from bson.errors import InvalidId
import random
from bson import ObjectId
from fastapi import HTTPException

#Modulo de python para gestionar logs
logger = logging.getLogger(__name__)

class PlanDeAccionServiceImp(IPlanAccionService):

    #Metodo constructor e inyeccion de dependencias
    def __init__(self, repo: PlanAccionRepository = Depends(), auditor_repo: AuditorExternoRepository = Depends()):
        self.repo = repo
        self.auditor_repo = auditor_repo

    #Metodo para crear plan de accion
    def guardar_plan(self, plan_de_accion: PlanDeAccionCreate) -> PlanDeAccionCreate:
        if not plan_de_accion:
            logger.warning("Intento de crear un plan de acción fallido.")
            raise ValueError("Datos del plan de acción incompletos o inválidos.")
        
        plan = self.repo.guardar_plan(plan_de_accion)
        logger.info(f"Plan de acción creado con exito {plan}")
        return plan

    #Metodo para listar planes de accion accion por id de auditor interno
    def listar_plan_por_auditor_interno(self, auditorI_id) -> List[str]:
        if not auditorI_id:
            logger.warning("Intento fallido")
            raise ValueError("Id invalido o vacio")
        planes = self.repo.listar_planes_por_auditor_interno(auditorI_id)
        logger.info(f"Planes de acción listados con exito {planes}")
        return planes
    
    #Método para listar plan de accion por id
    def listar_plan_por_id(self, plan_id: str) -> PlanDeAccionModel:
        if not ObjectId.is_valid(plan_id):
            raise ValueError("ID de plan inválido.")

        plan = self.repo.obtener_plan_por_id(plan_id)

        if not plan:
            raise ValueError("No se encontró ningún plan con el ID proporcionado.")

        plan["_id"] = str(plan["_id"])
        return PlanDeAccionModel(**plan)
    
    #Metodo para actulizar el estado de un plan de accion y añadirle un comentario
    def actualizar_estado_comentario(self, data: Actualizar_estado_comentario) -> bool:
        if not data.id:
            raise ValueError("El id no puede estar vacío")
        return self.repo.actualizar_estado_comentario(data.id, data.comentario, data.estado)
    
    
    #Metodo para añadir evidencias a un plan de accion
    def añadir_evidencias(self, plan_id: str, evidencias: List[EvidenciaMeta]) -> bool:
        # Validar ID
        if not ObjectId.is_valid(plan_id):
            raise ValueError("El ID del plan no es válido.")
        # Obtener plan
        plan = self.repo.obtener_plan_por_id(plan_id)
        if not plan:
            raise ValueError("No se encontró ningún plan con el ID proporcionado.")
        etapas = plan.get("etapas", [])
        num_etapas = len(etapas)
        updates = []
        for evidencia in evidencias:
            idx = evidencia.indice_etapa
            if not (0 <= idx < num_etapas):
                raise ValueError(f"Índice fuera de rango: {idx}. Etapas disponibles: {num_etapas}")
            if not evidencia.evidencia or not evidencia.evidencia.strip():
                raise ValueError(f"La evidencia en la etapa {idx} está vacía.")
            updates.append(evidencia)
        if not updates:
            raise ValueError("No se proporcionaron evidencias válidas.")

        return self.repo.añadir_evidencias(plan_id, updates)
    

    #Metodo para enviar plan a auditor externo
    def enviar_plan_a_auditorExterno(self, plan_id: str) -> bool:
        if not plan_id:
            logger.warning("Intento de enviar plan de accion fallido")
            raise ValueError("El ID del plan no puede enviarse vacio")
        auditores = self.auditor_repo.listar_auditores_externos()
        if not auditores:
            logger.info("No hay auditores externos disponibles")
        # Elegir uno aleatoriamente
        auditor_aleatorio = random.choice(auditores)
        auditorE_id = auditor_aleatorio.id
        # Asignar el plan al auditor seleccionado
        asignado = self.auditor_repo.asignar_plan(auditorE_id, plan_id)
        print(asignado)
        if not asignado:
            raise ValueError("No se pudo asignar el plan al auditor externo")
        return True
    
    # Método para listar planes pendientes por auditor interno
    def listar_planes_pendientes_por_auditor_interno(self, auditorI_id: str) -> List[str]:
        if not auditorI_id:
            logger.warning("Intento de listar planes pendientes con ID vacío.")
            raise ValueError("El ID del auditor no puede estar vacío.")
        
        planes_pendientes = self.repo.listar_planes_pendientes_por_auditor_interno(auditorI_id)
        logger.info(f"Planes de acción pendientes listados con éxito para el auditor {auditorI_id}")
        return planes_pendientes





