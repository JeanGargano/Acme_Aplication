import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ['mongodb_url'] = 'mongodb://localhost:27017/test'
os.environ['API_KEY'] = 'fake-key'

from dotenv import load_dotenv

from Service.IPlanAccionService import IPlanAccionService
from Repository.PlanAccionRepository import PlanAccionRepository
from Model.PlanAccionModel import PlanDeAccionModel, Actualizar_estado_comentario, EvidenciaRequest
from typing import List
from fastapi import Depends
import logging
from bson import ObjectId


load_dotenv()

logger = logging.getLogger(__name__)

class PlanDeAccionServiceImp(IPlanAccionService):

    def __init__(self, repo: PlanAccionRepository = Depends()):
        self.repo = repo

    def guardar_plan(self, plan_accion: PlanDeAccionModel) -> str:
        if not plan_accion:
            logger.warning("Intento fallido: datos del plan incompletos o inválidos.")
            raise ValueError("Datos del plan de acción incompletos o inválidos.")
        plan = self.repo.guardar_plan(plan_accion)
        logger.info(f"Plan de acción creado con éxito: {plan}")
        return plan

    def listar_plan_por_auditor_interno(self, auditorI_id: str) -> List[PlanDeAccionModel]:
        if not auditorI_id:
            logger.warning("Id de auditor interno vacío o inválido.")
            raise ValueError("Id del auditor interno es requerido.")
        planes = self.repo.listar_planes_por_auditor_interno(auditorI_id)
        logger.info(f"Planes listados con éxito para auditor: {auditorI_id}")
        return planes

    def actualizar_estado_comentario(self, data: Actualizar_estado_comentario) -> str:
        if not data.id:
            raise ValueError("El id del plan no puede estar vacío.")
        resultado = self.repo.actualizar_estado_comentario(data)
        logger.info(f"Estado y comentario actualizado para plan id: {data.id}")
        return resultado

    def añadir_evidencias(self, data: EvidenciaRequest) -> bool:
        if not ObjectId.is_valid(data.plan_id):
            raise ValueError("ID del plan no válido.")
        plan = self.repo.obtener_plan_por_id(data.plan_id)
        if not plan:
            raise ValueError("No se encontró plan con el ID proporcionado.")
        # Validación y lógica adicional pueden ir aquí si quieres
        resultado = self.repo.añadir_evidencias(data.plan_id, data.evidencias)
        logger.info(f"Evidencias añadidas al plan id: {data.plan_id}")
        return resultado
