#Clase abstracta donde van definidos los metodos para formulario
from abc import abstractmethod, ABC
from Model.FormularioModel import FormularioModel
from typing import List, Optional

class IFormularioService(ABC):

    #Metodo abstracto para crear formulario
    @abstractmethod
    def crear_formulario(self, formulario:FormularioModel) -> str:
        pass

    #Metodo abtracto para listar formularios
    @abstractmethod
    def listar_formularios(self) ->List[str]:
        pass

    #Metodo abstracto para listar formulario por norma
    @abstractmethod
    def listar_formulario_por_nombre(self, nombre:str) -> FormularioModel:
        pass



