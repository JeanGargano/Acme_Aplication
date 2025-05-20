#Clase Abstracta para los metodos de la repuesta del formulario
from abc import ABC, abstractmethod
from Model.RespuestaModel import RespuestaModel
from typing import List, Optional

class IRespuestaService(ABC):

    #Metodo abstracto para crear repuestas de un formulario
    @abstractmethod
    def crear_respuesta(self, respuesta: RespuestaModel) -> str:
        pass



    
