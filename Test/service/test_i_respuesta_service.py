import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ['mongodb_url'] = 'mongodb://localhost:27017/test'
os.environ['API_KEY'] = 'fake-key'


from dotenv import load_dotenv

from Service.IRespuestaService import IRespuestaService
from Repository.RespuestaRepository import RespuestaRepository
from Model.RespuestaModel import RespuestaModel
from fastapi import Depends
import logging
from typing import List

load_dotenv()

logger = logging.getLogger(__name__)

class RespuestaServiceImp(IRespuestaService):

    def __init__(self, repo: RespuestaRepository = Depends()):
        self.repo = repo

    def crear_respuesta(self, respuesta: RespuestaModel) -> str:
        if not respuesta:
            logger.warning("Intento de crear una respuesta inválida: datos incompletos")
            raise ValueError("Datos de respuesta incompletos o inválidos.")
        try:
            resultado = self.repo.crear_respuesta(respuesta)
            logger.info(f"Respuesta creada correctamente con id: {resultado}")
            return resultado
        except Exception as e:
            logger.error(f"Error al crear respuesta: {e}")
            raise
