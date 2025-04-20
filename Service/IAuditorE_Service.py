from abc import ABC, abstractmethod
from Model.AuditorE_Model import AuditorExterno
from typing import List, Optional

class IAuditorExternoService(ABC):

    @abstractmethod
    def crear_auditor_externo(self, auditor_externo: AuditorExterno) -> str:
        pass

    @abstractmethod
    def listar_auditores_externos(self) -> List[AuditorExterno]:
        pass
    
    @abstractmethod
    def listar_auditor_externo_por_id(self, auditor_id: str) -> Optional[AuditorExterno]:
        pass

