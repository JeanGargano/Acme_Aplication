import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ['mongodb_url'] = 'mongodb://localhost:27017/test'
os.environ['API_KEY'] = 'fake-key'


from dotenv import load_dotenv

from Service.IRespuestaService import IRespuestaService
from Repository.RespuestaRepository import RespuestaRepository
from Model.RespuestaModel import RespuestaModel
from typing import List, Optional
from uuid import UUID
from fastapi import Depends
import logging


load_dotenv()

logger = logging.getLogger(__name__)

class RespuestaServiceImp(IRespuestaService):

    # Método constructor e inyección de dependencias
    def __init__(self, repo: RespuestaRepository = Depends()):
        self.repo = repo

    # Método para crear respuestas de un formulario
    def crear_respuesta(self, respuesta: RespuestaModel) -> str:
        if not respuesta:
            logger.warning("Intento de crear una respuesta fallido")
            raise ValueError("Datos de respuesta incompletos")

        res = self.repo.crear_respuesta(respuesta)
        logger.info("Respuesta creada con éxito")
        return res
