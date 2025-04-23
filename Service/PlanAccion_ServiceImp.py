from Service.IPlanAccion_Service import IPlanAccionService
from Repository.PlanAccion_Repository import PlanAccionRepository
from Model.PlanAccion_Model import PlanDeAccion
from typing import List, Optional

class PlanDeAccionService(IPlanAccionService):

    def __init__(self):
        self.repo = PlanAccionRepository()
    
    def crear_plan(self, plan_de_accion: PlanDeAccion) -> str:
        return self.repo.crear_plan(plan_de_accion)

    def listar_planes(self) -> List[PlanDeAccion]:
        return self.repo.listar_planes()

    def listar_plan_por_id(self, plan_id: str) -> Optional[PlanDeAccion]:
        return self.repo.listar_plan_por_id(plan_id)
