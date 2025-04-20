from abc import ABC, abstractmethod
from Model.Formulario_Model import Formulario
from typing import List, Optional

class IFormularioService(ABC):

    @abstractmethod
    def crear_formulario(self, formulario: Formulario) -> str: pass

    @abstractmethod
    def listar_formularios(self) -> List[Formulario]: pass

    @abstractmethod
    def listar_formulario_por_id(self, formulario_id: str) -> Optional[Formulario]: pass

    
