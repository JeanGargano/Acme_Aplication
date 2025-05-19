#Flujo principal
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv 
from Controller.AuditorEController import router as auditor_e_router
from Controller.AuditorIController import router as auditor_i_router
from Controller.PlanAccionController import router as plan_accion_router
from Controller.RespuestaController import router as respuesta_router
from Controller.FormularioController import router as formulario_router
from Controller.GeminiController import router as gemini_router
from Controller.AdminController import router as admin_router
from Controller.RagServiceController import router as rag_router

import logging
import os

#Configuracion de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

#Cargar variables de entorno desde el archivo .env
load_dotenv()

#Inicializar la aplicación FastAPI
app = FastAPI()

api_router = APIRouter()

# Incluir los controladores en la API
api_router.include_router(formulario_router, prefix="/formulario", tags=["Formulario"])
api_router.include_router(auditor_i_router, prefix="/auditor_interno", tags=["Auditor Interno"])
api_router.include_router(auditor_e_router, prefix="/auditor_externo", tags=["Auditor Externo"])
api_router.include_router(plan_accion_router, prefix="/plan_de_accion", tags=["Plan de Acción"])
api_router.include_router(gemini_router, prefix="/gemini", tags=["Gemini"])
api_router.include_router(respuesta_router, prefix="/respuesta", tags=["Respuesta"])
api_router.include_router(admin_router, prefix="/admin", tags=["Administrador"])
api_router.include_router(rag_router, prefix="/rag", tags=["Rag"])
# Incluir el router principal
app.include_router(api_router)
    
# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ejecutar la aplicación
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
