#Clase que implementa los metodos Abstractos de la interfaz, se comunica con el repositorio
from Service.IAuditorIService import IAuditorInternoService
from Repository.AuditorIRepository import AuditorInternoRepository
from Model.AuditorIModel import AuditorInternoModel
from typing import List, Optional
from bson import ObjectId
from fastapi import Depends
import logging
import bcrypt
from bson import ObjectId

# Modulo de python para gestionar logs
logger = logging.getLogger(__name__)

# Metodo para verificar contraseñas
def verificar_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

class AuditorInternoServiceImp(IAuditorInternoService):
    #Constructor de clase e inyeccion de dependencias
    def __init__(self, repo: AuditorInternoRepository = Depends()):
        self.repo = repo

    #Metodo para crear un auditor interno
    def crear_auditor_interno(self, auditor_interno: AuditorInternoModel) -> AuditorInternoModel:
        if not auditor_interno or not auditor_interno.nombre:
            logger.warning("Intento de crear un auditor interno inválido.")
            raise ValueError("Datos de auditor interno incompletos o inválidos.")

        auditor_I = self.repo.crear_auditor_interno(auditor_interno)
        logger.info(f"Auditor interno creado con ID: {auditor_I}")
        return auditor_I

    #Metodo para listar auditores externos
    def listar_auditores_internos(self) -> List[AuditorInternoModel]:
        return self.repo.listar_auditores_internos()

    #Metodo para logear auditor interno
    def logear_auditor_interno(self, usuario: str, contraseña: str) -> dict | None:
        auditor = self.repo.buscar_auditor_interno_por_usuaroi(usuario)
        if auditor and verificar_password(contraseña, auditor["contraseña"]):
            auditor["_id"] = str(auditor["_id"])  # Convertimos el ObjectId
            return auditor
        return None

