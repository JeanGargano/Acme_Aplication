#Clase que implementa los metodos Abstractos de la interfaz, se comunica con el repositorio
from Service.IPlanAccionService import IPlanAccionService
from Repository.PlanAccionRepository import PlanAccionRepository
from Model.PlanAccionModel import PlanDeAccionModel, Actualizar_plan
from typing import List
from fastapi import Depends
import logging

#Modulo de python para gestionar logs
logger = logging.getLogger(__name__)

class PlanDeAccionServiceImp(IPlanAccionService):

    #Metodo constructor e inyeccion de dependencias
    def __init__(self, repo: PlanAccionRepository = Depends()):
        self.repo = repo

    #Metodo para crear plan de accion
    def guardar_plan(self, plan_de_accion: PlanDeAccionModel) -> PlanDeAccionModel:
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
        

    
    #Metodo para actulizar un plan de accion
    def actualizar_plan(self, data: Actualizar_plan) -> bool:
        if not data.id:
            raise ValueError("El id no puede estar vacío")
        return self.repo.actualizar_plan(data.id, data.comentario, data.estado)
