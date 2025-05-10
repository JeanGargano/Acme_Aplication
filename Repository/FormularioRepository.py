#Clase repositorio tiene comunicación directa con la base de datos
from configurations import db
from Model.FormularioModel import FormularioModel
from bson import ObjectId
class FormularioRepository:
    
    #Metodo constructor de clase e instanciando la base de datos
    def __init__(self):
        self.collection = db['Formulario']

    #Insertar un formulario en la base de datos
    def crear_formulario(self, formulario:FormularioModel):
        form_data = formulario.dict(by_alias=True)
        result = self.collection.insert_one(form_data)
        return str(result.inserted_id)

    #Trae los formularios creados en la base de datos
    def listar_formularios(self):
        return [FormularioModel(**doc) for doc in self.collection.find()]

    #Trae un formulario segun la norma
    def listar_formulario_por_norma(self, norma: str):
        data = self.collection.find_one({"norma": norma})
        return FormularioModel(**data) if data else None
   
