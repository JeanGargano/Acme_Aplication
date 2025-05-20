#Clase Abstracta para Plan de Accion
from abc import ABC, abstractmethod
from typing import List
from Model.PlanAccionModel import PlanDeAccionModel, PlanDeAccionCreate, Actualizar_estado_comentario, EvidenciaRequest

class IPlanAccionService(ABC):

    #Metodo abstracto para crear plan de accion
    @abstractmethod
    def guardar_plan(self, plan_accion: PlanDeAccionCreate) -> str:
        pass

    #Metodo abstracto para listar plan de accion por auditor interno
    @abstractmethod
    def listar_plan_por_auditor_interno(self, auditorI_id: str) -> List[PlanDeAccionModel]:
        pass
    
    #Método abstracto para listar plan de acción por id
    @abstractmethod
    def listar_plan_por_id(self, plan_id: str) -> PlanDeAccionModel:
        pass

    #Metodo para actulizar el estado de un plan de accion y añadirle un comentario
    @abstractmethod
    def actualizar_estado_comentario(self, data: Actualizar_estado_comentario) -> str:
        pass

    #Metodo para añadir evidencias a un plan de acción
    @abstractmethod
    def añadir_evidencias(self, data: EvidenciaRequest) -> bool:
        pass
    
    #Metodo para enviar un plan a un aditor externo
    def enviar_plan_a_auditorExterno(self, plan_id: str) -> bool:
        pass

    def listar_planes_pendientes_por_auditor_interno(self, auditorI_id: str) -> List[str]:
        pass
    

    

