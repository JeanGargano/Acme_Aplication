from Service.IAuditorI_Service import IAuditorInternoService
from Repository.AuditorI_Repository import AuditorInternoRepository
from Model.AuditorI_Model import AuditorInterno
from typing import List, Optional

class AuditorInternoService(IAuditorInternoService):

    def __init__(self):
        self.repo = AuditorInternoRepository()
    
    def crear_auditor_interno(self, auditor_interno: AuditorInterno) -> str:
        return self.repo.crear_auditor_interno(auditor_interno)

    def listar_auditores_internos(self) -> List[AuditorInterno]:
        return self.repo.listar_auditores_internos()
    
    def listar_auditor_interno_por_id(self, auditor_id) -> Optional[AuditorInterno]:
        return self.repo.listar_auditores_internos_por_id(auditor_id)

 
