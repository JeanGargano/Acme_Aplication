#Clase Abstracta para Plan de Accion
from abc import ABC, abstractmethod
from typing import List
from Model.PlanAccionModel import PlanDeAccionModel, Actualizar_plan

class IPlanAccionService(ABC):

    #Metodo abstracto para crear plan de accion
    @abstractmethod
    def guardar_plan(self, plan_accion: PlanDeAccionModel) -> str:
        pass

    #Metodo abstracto para listar plan de accion por auditor interno
    @abstractmethod
    def listar_plan_por_auditor_interno(self, auditorI_id: str) -> List[PlanDeAccionModel]:
        pass


    #Metodo para actulizar el plan de accion
    @abstractmethod
    def actualizar_plan(self, data: Actualizar_plan) -> str:
        pass


