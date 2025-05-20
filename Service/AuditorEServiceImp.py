#Clase que implementa los metodos Abstractos de la interfaz, se comunica con el repositorio
from Service.IAuditorEService import IAuditorExternoService
from Repository.AuditorERepository import AuditorExternoRepository
from Model.AuditorEModel import AuditorExternoModel, AuditorExternoCreate
from typing import List, Optional
from bson import ObjectId
from fastapi import Depends
import logging
import bcrypt

#Modulo de python para gestionar logs
logger = logging.getLogger(__name__)

#Metodo para verificar la contraseña
def verificar_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

class AuditorExternoServiceImp(IAuditorExternoService):
    #Constructor de clase e inyeccion de dependencias
    def __init__(self, repo: AuditorExternoRepository = Depends()):
        self.repo = repo

    #Metodo para crear auditor externo
    def crear_auditor_externo(self, auditor_externo: AuditorExternoCreate) ->  AuditorExternoCreate:
        if not auditor_externo or not auditor_externo.nombre:
            logger.warning("Intento de crear un auditor externo inválido.")
            raise ValueError("Datos de auditor externo incompletos o inválidos.")
        
        auditorE = self.repo.crear_auditor_externo(auditor_externo)
        logger.info(f"Auditor externo creado {auditorE}")
        return auditorE

    #Metodo para listar auditores externos
    def listar_auditores_externos(self) -> List[AuditorExternoModel]:
        return self.repo.listar_auditores_externos()
    
    
    #Metodo para logear auditor externo
    def logear_auditor_externo(self, usuario: str, contraseña: str) -> dict | None:
        auditor = self.repo.buscar_auditor_externo_por_usuario(usuario)
        if auditor and verificar_password(contraseña, auditor["contraseña"]):
            auditor["_id"] = str(auditor["_id"])  # Convertimos el ObjectId
            return auditor
        return None





