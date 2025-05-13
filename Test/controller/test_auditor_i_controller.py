import sys
import os

import pytest
from fastapi.testclient import TestClient
from main import app
from Model.AuditorIModel import AuditorInternoModel
from Model.LoginRequest import LoginRequest

client = TestClient(app)

# Test para crear auditor interno
def test_crear_auditor_interno():
    auditor_data = {
        "nombre": "Juan Perez",
        "compañia": "Acme Corp",
        "usuario": "juan.perez",
        "contraseña": "password123",
        "email": "juan.perez@example.com",
        "telefono": "1234567890"
    }
    response = client.post("/auditor_interno/crear_auditor_interno", json=auditor_data)
    assert response.status_code == 200
    assert "Auditor interno creado con exito" in response.json()[0]

# Test para listar auditores internos
def test_listar_auditores_internos():
    response = client.get("/auditor_interno/listar_auditores_internos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test para logear auditor interno
def test_logear_auditor_interno():
    login_data = {
        "usuario": "Juanes",
        "contraseña": "$2b$12$.3cgthVOpNymN0ZEFFrrYecYOsNyHoizl0RM0NmsOafNliqvRJxcW"
    }
    response = client.post("/auditor_interno/logear_auditor_interno", json=login_data)
    if response.status_code == 401:
        assert response.json()["detail"] == "Credenciales inválidas"
    else:
        assert response.status_code == 200
        assert "email" in response.json()
