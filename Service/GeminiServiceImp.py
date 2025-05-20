#Clase que implementa los metodos Abstractos de la interfaz, se comunica con el repositorio
from Service.IGeminiService import IGeminiService
from Repository.GeminiRepository import GeminiRepository
from Model.PromptModel import PromptModel
from fastapi import Depends
import logging
import json

#Modulo de python para gestionar logs
logger = logging.getLogger(__name__)

class GeminiServiceImp(IGeminiService):

    #Metodo constructor e inyeccion de dependencias
    def __init__(self, repo: GeminiRepository = Depends()):
        self.repo = repo

    #Metodo para generar reporte
    def generar_reporte(self, prompt: PromptModel ) -> json:
        if not prompt:
            logger.warning("Prompt inválido recibido.")
            raise ValueError("El prompt es requerido y no puede estar vacío.")
        try:
            response = self.repo.generar_reporte(prompt)
            if(response):
                logger.info("Prompt procesado exitosamente.")
                return response
            else:
                logger.info("El prompt no ha sido procesado correctamente")
        except Exception as e:
            logger.error(f"Error al procesar el prompt: {e}")
            raise RuntimeError("Error al procesar el prompt.")
        
 


