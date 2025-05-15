import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ['mongodb_url'] = 'mongodb://localhost:27017/test'
os.environ['API_KEY'] = 'fake-key'

from dotenv import load_dotenv


import pytest
from Service.GeminiServiceImp import GeminiServiceImp
from Model.PromptModel import PromptModel, Item
from unittest.mock import MagicMock


load_dotenv()

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def service(mock_repo):
    return GeminiServiceImp(repo=mock_repo)

def test_generar_reporte_valido(service, mock_repo):
    prompt = PromptModel(prompt=[
        Item(pregunta="Genera un resumen", respuesta="Respuesta de ejemplo", evidencia="Evidencia de ejemplo")
    ])
    mock_response = {"respuesta": "Resumen generado"}
    mock_repo.generar_reporte.return_value = mock_response

    resultado = service.generar_reporte(prompt)

    assert resultado == mock_response
    mock_repo.generar_reporte.assert_called_once_with(prompt)

def test_generar_reporte_sin_prompt(service):
    with pytest.raises(ValueError):
        service.generar_reporte(None)

def test_generar_reporte_excepcion_en_repo(service, mock_repo):
    prompt = PromptModel(prompt=[
        Item(pregunta="Falla intencional", respuesta="Respuesta", evidencia="Evidencia")
    ])
    mock_repo.generar_reporte.side_effect = Exception("Error en repo")

    with pytest.raises(RuntimeError) as excinfo:
        service.generar_reporte(prompt)

    assert "Error al procesar el prompt" in str(excinfo.value)
