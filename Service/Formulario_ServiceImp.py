from Service.IFormulario_Service import IFormularioService
from Repository.Formulario_Repository import FormularioRepository
from Model.Formulario_Model import Formulario
from typing import List, Optional

class FormularioService(IFormularioService):
    def __init__(self):
        self.repo = FormularioRepository()

    def crear(self, formulario: Formulario) -> str:
        return self.repo.crear_formulario(formulario)
    
    def listar(self) -> List[Formulario]:
        return self.repo.listar_formularios()

    def obtener_por_id(self, formulario_id: str) -> Optional[Formulario]:
        return self.repo.listar_formulario_por_id(formulario_id)




