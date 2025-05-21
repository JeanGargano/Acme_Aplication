from Model.AuditorEModel import AuditorExternoModel
from Model.AuditorIModel import AuditorInternoModel
from Repository.AuditorERepository import AuditorExternoRepository
from Repository.AuditorIRepository import AuditorInternoRepository
from Model.UsuarioModel import Usuario

class AdminService:
    def __init__(self):
        self.repo_externo = AuditorExternoRepository()
        self.repo_interno = AuditorInternoRepository()

    def cambiar_tipo_auditor(self, data: Usuario):
        usuario = data.usuario
        interno = self.repo_interno.buscar_auditor_interno_por_usuario(usuario)
        if interno:
            self.repo_interno.collection.delete_one({"usuario": usuario})
            nuevo_externo = AuditorExternoModel(
                nombre=interno["nombre"],
                usuario=interno["usuario"],
                contraseña=interno["contraseña"]  
            )
            return self.repo_externo.collection.insert_one(nuevo_externo.dict()).inserted_id
        externo = self.repo_externo.buscar_auditor_externo_por_usuario(usuario)
        if externo:
            self.repo_externo.collection.delete_one({"usuario": usuario})
            nuevo_interno = AuditorInternoModel(
                nombre=externo["nombre"],
                compañia=data.compañia,
                usuario=externo["usuario"],
                contraseña=externo["contraseña"]
            )
            return self.repo_interno.collection.insert_one(nuevo_interno.dict()).inserted_id

        raise ValueError("El auditor no fue encontrado en ninguna colección.")