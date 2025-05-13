import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import pytest
from fastapi.testclient import TestClient
from fastapi import status, Depends
from Controller import AuditorEController
from Service.AuditorEServiceImp import AuditorExternoServiceImp
from Model.AuditorEModel import AuditorExternoModel
from Model.LoginRequest import LoginRequest

from main import app  # Asegúrate que tu archivo main.py tenga `app = FastAPI()` y haya incluido los routers

# Usa un mock del servicio para evitar lógica real de base de datos
class MockAuditorExternoService:
    def crear_auditor_externo(self, auditor_externo: AuditorExternoModel):
        return {"nombre": f"{auditor_externo.nombre} Pérez", "usuario": auditor_externo.usuario}

    def listar_auditores_externos(self):
        return [{"nombre": "Auditor 1"}, {"nombre": "Auditor 2"}]

    def logear_auditor_externo(self, usuario, contraseña):
        if usuario == "valido" and contraseña == "1234":
            return {"usuario": usuario}
        return None

# Remplazar la dependencia en pruebas
app.dependency_overrides[AuditorExternoServiceImp] = lambda: MockAuditorExternoService()
client = TestClient(app)

# --- PRUEBAS ---

def test_crear_auditor_externo():
    auditor = {
        "nombre": "Juan",
        "usuario": "juan123",
        "contraseña": "pampampam",
        "correo": "juan@example.com"
    }
    response = client.post("/crear_auditor_externo", json=auditor)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["mensaje"] == "Auditor Externo creado con éxito"
    assert response.json()["auditor"]["nombre"] == "Juan Pérez"

def test_listar_auditores_externos():
    response = client.get("/listar_auditores_externos")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_logear_auditor_externo_valido():
    data = {
        "usuario": "valido",
        "contraseña": "1234"
    }
    response = client.post("/logear_auditor_externo", json=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["usuario"] == "valido"

def test_logear_auditor_externo_invalido():
    data = {
        "usuario": "invalido",
        "contraseña": "0000"
    }
    response = client.post("/logear_auditor_externo", json=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()["detail"] == "Credenciales inválidas"
