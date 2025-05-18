#Clase que implementa los metodos de la interfaz, se comunica con el repositorio
from Model.FormularioModel import FormularioModel
from Repository.FormularioRepository import FormularioRepository
from Service.IFormularioService import IFormularioService
from bson import ObjectId
from fastapi import Depends
import logging
from typing import List

#Modulo de python para gestionar logs
logger = logging.getLogger(__name__)

class FormularioServiceImp(IFormularioService):
    #Constructor de clase e inyeccion de dependencias
    def __init__(self, repo: FormularioRepository = Depends()):
        self.repo = repo

    #Metodo para crear formulario
    def crear_formulario(self, formulario: FormularioModel) -> FormularioModel:
        if not formulario:
            logger.warning("Formulario inválido: Faltan campos")
            raise ValueError("Faltan campos para crear el formulario")
        form = self.repo.crear_formulario(formulario)
        if form:
            logger.info(f"Formulario creado: {form}")
            return form
        else:
            logger.error("No se pudo crear el formulario en la base de datos.")
            raise Exception("Error al guardar el formulario.")

    #Metodo para listar formularios
    def listar_formularios(self) -> List[FormularioModel]:
        formularios = self.repo.listar_formularios()
        if(formularios):
            logger.info("Formularios listados de forma exitosa")
            return formularios
        else:
            logger.info("No se han podido listar formularios")

    #Metodo para listar formulario por norma
    def listar_formulario_por_nombre(self, nombre: str) -> str:
        if not nombre:
            logger.warning("No esta llegando la norma en el json")
            raise ValueError("La norma es necesaria para la ejecucion de este metodo")
        form = self.repo.listar_formulario_por_nombre(nombre)
        if form:
            logger.info(f"Formulario encontrado con norma: {form}")
            return form
        else:
            logger.info("Formulario no encontrado")
            raise Exception("Error al buscar el formulario")

            
