import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test para crear formulario
def test_crear_formulario():
    formulario_data = {
        "nombre": "Formulario 1",
        "titulo": "Formulario de Calidad",
        "descripcion": "Descripción del formulario",
        "norma": "ISO 9001",
        "preguntas": ["¿Cuál es su nombre?", "¿Cuál es su edad?"]
    }
    response = client.post("/formulario/crear_formulario", json=formulario_data)
    assert response.status_code == 200
    assert response.json() == "Formulario guardado exitosamente"

# Test para listar formularios
def test_listar_formularios():
    response = client.get("/formulario/listar_formularios")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test para listar formulario por norma
def test_listar_formulario_por_norma():
    response = client.get("/formulario/listar_por_norma", params={"norma": "ISO 9001"})
    assert response.status_code == 200
    assert isinstance(response.json(), dict)  # Validar que la respuesta sea un objeto
    assert "norma" in response.json()  # Validar que el campo 'norma' esté presente
    assert response.json()["norma"] == "ISO 9001"