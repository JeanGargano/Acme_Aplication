import sys
import os

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test para crear plan de acción
def test_guardar_plan():
    plan_data = {
        "objetivo": "Mejorar procesos internos",
        "etapas": [
            {"meta": "Revisar documentos"}
        ],
        "auditor_interno": "12345",
        "comentario": "Plan inicial"
    }
    response = client.post("/plan_de_accion/guardar_plan", json=plan_data)
    assert response.status_code == 200
    assert response.json()["mensaje"] == "Se ha creado el plan de acción exitosamente"

# Test para listar planes por auditor interno
def test_listar_plan_por_auditor_interno():
    response = client.get("/plan_de_accion/listar_plan_por_auditor_interno", params={"auditorI_id": "12345"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test para actualizar comentario y estado
def test_actualizar_comentario_estado():
    data = {
        "id": "6820f863faeb3db927271e7e",  # Usar un ObjectId válido simulado
        "estado": "Completado",
        "comentario": "Plan completado exitosamente"
    }
    response = client.post("/plan_de_accion/actualizar_comentario_estado", json=data)
    assert response.status_code == 200
    assert response.json()["message"] == "Plan actualizado correctamente"

# Test para añadir evidencias
def test_añadir_evidencias():
    data = {
        "plan_id": "6820f863faeb3db927271e7e",
        "evidencias": [
            {"indice_etapa": 0, "evidencia": "Evidencia 1"},
            {"indice_etapa": 1, "evidencia": "Evidencia 2"}
        ]
    }
    response = client.post("/plan_de_accion/añadir_evidencias", json=data)
    assert response.status_code == 200
    assert response.json()["mensaje"] == "Evidencias actualizadas correctamente"
