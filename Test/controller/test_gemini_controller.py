import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")
print(f"API_KEY: {api_key}")

if not api_key:
    raise Exception("API_KEY no encontrada")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

prompt = "Dame un ejemplo de plan de acción"
response = model.generate_content(prompt)
print(response.text)

import pytest
from unittest.mock import MagicMock
from Service.GeminiServiceImp import GeminiServiceImp
from Model.PromptModel import PromptModel

# Mock del repositorio
mock_repo = MagicMock()
service = GeminiServiceImp(repo=mock_repo)

def test_generar_reporte_exitoso():
    # Datos de prueba
    prompt = PromptModel(prompt=[
        {"pregunta": "¿Cuál es el objetivo?", "respuesta": "Mejorar calidad", "evidencia": "Reporte de calidad"}
    ])
    mock_repo.generar_reporte.reset_mock()  # Asegurarse de que el mock esté limpio
    mock_repo.generar_reporte.return_value = {"reporte": "Reporte generado exitosamente"}

    # Llamar al método
    response = service.generar_reporte(prompt)

    # Verificar resultados
    assert response == {"reporte": "Reporte generado exitosamente"}
    mock_repo.generar_reporte.assert_called_once_with(prompt)

def test_generar_reporte_sin_prompt():
    with pytest.raises(ValueError, match="El prompt es requerido y no puede estar vacío."):
        service.generar_reporte(None)

def test_generar_reporte_error_en_repositorio():
    # Datos de prueba
    prompt = PromptModel(prompt=[
        {"pregunta": "¿Cuál es el objetivo?", "respuesta": "Mejorar calidad", "evidencia": "Reporte de calidad"}
    ])
    mock_repo.generar_reporte.reset_mock()  # Asegurarse de que el mock esté limpio
    mock_repo.generar_reporte.side_effect = Exception("Error en el repositorio")

    # Llamar al método y verificar excepción
    with pytest.raises(RuntimeError, match="Error al procesar el prompt."):
        service.generar_reporte(prompt)
    mock_repo.generar_reporte.assert_called_once_with(prompt)
