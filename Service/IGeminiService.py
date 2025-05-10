#Clase Abstracta para Gemini
from abc import ABC, abstractmethod
from Model.PromptModel import PromptModel
import json

class IGeminiService(ABC):

    #Metodo abstracto para generar reporte
    @abstractmethod
    def generar_reporte(self, prompt: PromptModel) -> json:
        pass





