import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ['mongodb_url'] = 'mongodb://localhost:27017/test'
os.environ['API_KEY'] = 'fake-key'

from dotenv import load_dotenv

import pytest
from Service.FormularioServiceImp import FormularioServiceImp
from Model.FormularioModel import FormularioModel
from unittest.mock import MagicMock

load_dotenv()

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def service(mock_repo):
    return FormularioServiceImp(repo=mock_repo)

def test_crear_formulario_valido(service, mock_repo):
    form = FormularioModel(
        norma="ISO9001",
        titulo="Formulario de prueba",
        preguntas=["¿Pregunta 1?", "¿Pregunta 2?"]
    )
    mock_repo.crear_formulario.return_value = form
    result = service.crear_formulario(form)
    assert result.norma == "ISO9001"

def test_crear_formulario_invalido(service):
    with pytest.raises(ValueError, match="Faltan campos"):
        service.crear_formulario(None)

def test_listar_formularios_con_datos(service, mock_repo):
    mock_repo.listar_formularios.return_value = [
        FormularioModel(
            norma="ISO9001",
            titulo="Formulario de prueba",
            preguntas=["¿Pregunta 1?", "¿Pregunta 2?"]
        )
    ]
    result = service.listar_formularios()
    assert len(result) > 0

def test_listar_formularios_vacio(service, mock_repo):
    mock_repo.listar_formularios.return_value = []
    result = service.listar_formularios()
    assert result is None  # porque no retorna nada si no hay formularios

def test_listar_formulario_por_norma_valida(service, mock_repo):
    mock_repo.listar_formulario_por_norma.return_value = "Formulario de prueba"
    result = service.listar_formulario_por_norma("ISO9001")
    assert result == "Formulario de prueba"

def test_listar_formulario_por_norma_vacia(service):
    with pytest.raises(ValueError, match="La norma es necesaria"):
        service.listar_formulario_por_norma("")

def test_listar_formulario_por_norma_no_encontrada(service, mock_repo):
    mock_repo.listar_formulario_por_norma.return_value = None
    with pytest.raises(Exception, match="Error al buscar el formulario"):
        service.listar_formulario_por_norma("NO_EXISTE")
