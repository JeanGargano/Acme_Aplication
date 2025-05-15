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
    formulario = FormularioModel(
        norma="ISO 9001",
        titulo="Formulario 1",
        preguntas=["campo1", "campo2"]
    )
    mock_repo.crear_formulario.return_value = formulario

    resultado = service.crear_formulario(formulario)

    assert resultado.titulo == "Formulario 1"
    mock_repo.crear_formulario.assert_called_once_with(formulario)

def test_crear_formulario_invalido(service):
    with pytest.raises(ValueError):
        service.crear_formulario(None)

def test_listar_formularios_con_datos(service, mock_repo):
    mock_repo.listar_formularios.return_value = [
        FormularioModel(norma="ISO", titulo="F1", preguntas=["c1"]),
        FormularioModel(norma="ISO", titulo="F2", preguntas=["c2"])
    ]

    resultado = service.listar_formularios()
    assert len(resultado) == 2

def test_listar_formularios_sin_datos(service, mock_repo):
    mock_repo.listar_formularios.return_value = []

    resultado = service.listar_formularios()
    assert resultado is None

def test_listar_formulario_por_norma_valido(service, mock_repo):
    norma = "ISO 9001"
    formulario = FormularioModel(
        norma=norma,
        titulo="FISO",
        preguntas=["campo"]
    )
    mock_repo.listar_formulario_por_norma.return_value = formulario

    resultado = service.listar_formulario_por_norma(norma)

    assert resultado.norma == norma

def test_listar_formulario_por_norma_vacio(service):
    with pytest.raises(ValueError):
        service.listar_formulario_por_norma("")

def test_listar_formulario_por_norma_no_encontrado(service, mock_repo):
    mock_repo.listar_formulario_por_norma.return_value = None

    with pytest.raises(Exception):
        service.listar_formulario_por_norma("ISO inexistente")
