#Clase que implementa los metodos Abstractos de la interfaz, se comunica con el repositorio
from Service.IRespuestaService import IRespuestaService
from Repository.RespuestaRepository import RespuestaRepository
from Model.RespuestaModel import RespuestaModel
from typing import List, Optional
from uuid import UUID
from fastapi import Depends
import logging

#Modulo de python para gestionar logs
logger = logging.getLogger(__name__)

class RespuestaServiceImp(IRespuestaService):

    #Metodo constructor e inyeccio de dependencias
    def __init__(self, repo: RespuestaRepository = Depends()):
        self.repo = repo

    #Metodo para crear respuestas de un formulario
    def crear_respuesta(self, respuesta: RespuestaModel) -> str:
        if not respuesta:
            logger.warning("Intento de de crear una respuesta fallido")
            raise ValueError("Datos de respuesta incompletos")

        res = self.repo.crear_respuesta(respuesta)
        logger.info("Respuesta creada con exito")
        return res
