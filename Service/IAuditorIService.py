#Clase abstracta para Auditor Interno
from abc import ABC, abstractmethod
from Model.AuditorIModel import AuditorInternoModel
from typing import List, Optional

class IAuditorInternoService(ABC):

    #Metodo abstracto para crear auditor interno
    @abstractmethod
    def crear_auditor_interno(self, auditor_interno: AuditorInternoModel) -> str:
        pass

    #Metodo abstracto para listar auditores internos
    @abstractmethod
    def listar_auditores_internos(self) -> List[AuditorInternoModel]:
        pass
    
    #Metodo Abstracto para logear un auditor interno
    @abstractmethod
    def logear_auditor_interno(self, usuario: str, contraseña: str) -> Optional[AuditorInternoModel]:
        pass
