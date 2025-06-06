from Service.IAuditorE_Service import IAuditorExternoService
from Repository.AuditorE_Repository import  AuditorExternoRepository
from Model.AuditorE_Model import AuditorExterno
from typing import List, Optional


class AuditorExternoService(IAuditorExternoService):
    def __init__(self):
        self.repo = AuditorExternoRepository()

    def crear_auditor_externo(self, auditor_externo: AuditorExterno) -> str:
        return self.repo.crear_auditor_externo(auditor_externo)

    def listar_auditores_externos(self) -> list:
        return self.repo.listar_auditores_externos()

    def listar_auditor_externo_por_id(self, auditor_id: str) -> Optional[AuditorExterno]:
        return self.repo.listar_auditor_externo_por_id(auditor_id)


  
