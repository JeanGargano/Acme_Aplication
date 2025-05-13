import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test para crear respuesta
def test_crear_respuesta():
    respuesta_data = {
        "titulo": "Encuesta de satisfacción",
        "respuestas": [
            {"pregunta": "¿Cómo calificaría nuestro servicio?", "respuesta": "Excelente", "evidencia": "Foto del producto"},
            {"pregunta": "¿Recomendaría nuestro servicio?", "respuesta": "Sí", "evidencia": "Comentario positivo"}
        ],
        "auditorInterno": "645a1c2f4f1c4b3d2e1a1b1c",
        "idFormulario": "645a1c2f4f1c4b3d2e1a1b1d"
    }
    response = client.post("/respuesta/crear_respuesta", json=respuesta_data)
    assert response.status_code == 200
    assert response.json()["mensaje"] == "Respuestas enviadas con éxito"
