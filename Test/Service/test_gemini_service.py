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
    prompt = PromptModel(
        prompt=[
            Item(pregunta="¿Cuál es el resumen del informe?", respuesta="Respuesta de ejemplo", evidencia="Evidencia de ejemplo")
        ]
    )
    mock_repo.generar_reporte.return_value = {"respuesta": "Este es el resumen"}
    result = service.generar_reporte(prompt)
    assert result["respuesta"] == "Este es el resumen"

def test_generar_reporte_prompt_none(service):
    with pytest.raises(ValueError, match="El prompt es requerido"):
        service.generar_reporte(None)

def test_generar_reporte_falla_en_repo(service, mock_repo):
    prompt = PromptModel(
        prompt=[
            Item(pregunta="¿Cuál es el resumen?", respuesta="Respuesta", evidencia="Evidencia")
        ]
    )
    mock_repo.generar_reporte.side_effect = Exception("Fallo interno")
    with pytest.raises(RuntimeError, match="Error al procesar el prompt"):
        service.generar_reporte(prompt)

def test_generar_reporte_sin_respuesta(service, mock_repo):
    prompt = PromptModel(
        prompt=[
            Item(pregunta="¿Qué pasó?", respuesta="Respuesta", evidencia="Evidencia")
        ]
    )
    mock_repo.generar_reporte.return_value = None
    result = service.generar_reporte(prompt)
    assert result is None