#Clase Abstracta para Auditor Externo
from abc import ABC, abstractmethod
from Model.AuditorEModel import AuditorExternoModel
from typing import List, Optional

class IAuditorExternoService(ABC):

    #Metodo Abstracto para crear auditor externo
    @abstractmethod
    def crear_auditor_externo(self, auditor_externo: AuditorExternoModel) -> str:
        pass

    #Metodo Abstracto para listar auditores externos
    @abstractmethod
    def listar_auditores_externos(self) -> List[AuditorExternoModel]:
        pass

    #Metodo Abstracto para logear auditor externo
    @abstractmethod
    def logear_auditor_externo(self, usuario: str, contraseña: str) -> Optional[AuditorExternoModel]:
        pass
    

