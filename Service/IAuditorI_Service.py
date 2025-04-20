from abc import ABC, abstractmethod
from Model.AuditorI_Model import AuditorInterno
from typing import List, Optional

class IAuditorInternoService(ABC):

    @abstractmethod
    def crear_auditor_interno(self, auditor_interno: AuditorInterno) -> str:
        pass

    @abstractmethod
    def listar_auditores_internos(self) -> List[AuditorInterno]:
        pass

    @abstractmethod
    def listar_auditor_interno_por_id(self, auditor_id: str) -> Optional[AuditorInterno]:
        pass
