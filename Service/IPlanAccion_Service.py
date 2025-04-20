from abc import ABC, abstractmethod
from typing import List, Optional
from Model.PlanAccion_Model import PlanDeAccion

class IPlanAccionService(ABC):

    @abstractmethod
    def crear_plan(self, plan_accion: PlanDeAccion) -> str:
        pass

    @abstractmethod
    def listar_planes(self) -> List[PlanDeAccion]:
        pass

    @abstractmethod
    def listar_plan_por_id(self, plan_id: str) -> Optional[PlanDeAccion]:
        pass

