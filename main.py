from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv 
import os
from Controller import AuditorE_Controller, AuditorI_Controller, PlanAccion_Controller, Formulario_Controller


load_dotenv() 

app = FastAPI()
app.include_router(Formulario_Controller.router, prefix="/api")
app.include_router(AuditorI_Controller.router, prefix="/api")
app.include_router(AuditorE_Controller.router, prefix="/api")
app.include_router(PlanAccion_Controller.router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
