import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ['mongodb_url'] = 'mongodb://localhost:27017/test'
os.environ['API_KEY'] = 'fake-key'

from dotenv import load_dotenv


import pytest
from Service.AuditorEServiceImp import AuditorExternoServiceImp
from Model.AuditorEModel import AuditorExternoModel
from unittest.mock import MagicMock
import bcrypt

load_dotenv()

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def service(mock_repo):
    return AuditorExternoServiceImp(repo=mock_repo)

def test_crear_auditor_externo_valido(service, mock_repo):
    auditor = AuditorExternoModel(nombre="Juan", usuario="juan123", contraseña="123456")
    mock_repo.crear_auditor_externo.return_value = auditor

    resultado = service.crear_auditor_externo(auditor)

    assert resultado.nombre == "Juan"
    mock_repo.crear_auditor_externo.assert_called_once()

def test_crear_auditor_externo_invalido(service):
    with pytest.raises(ValueError):
        service.crear_auditor_externo(None)

def test_listar_auditores_externos(service, mock_repo):
    mock_repo.listar_auditores_externos.return_value = [
        AuditorExternoModel(nombre="Ana", usuario="ana123", contraseña="pass")
    ]

    resultado = service.listar_auditores_externos()
    assert len(resultado) == 1

def test_logear_auditor_correcto(service, mock_repo):
    contraseña_plana = "123456"
    hash = bcrypt.hashpw(contraseña_plana.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    auditor_db = {
        "_id": "abc123",
        "nombre": "Carlos",
        "usuario": "carlos123",
        "contraseña": hash
    }
    mock_repo.buscar_auditor_externo_por_usuario.return_value = auditor_db

    resultado = service.logear_auditor_externo("carlos123", "123456")
    assert resultado["nombre"] == "Carlos"

def test_logear_auditor_contraseña_incorrecta(service, mock_repo):
    hash = bcrypt.hashpw("correcta".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    auditor_db = {"_id": "123", "usuario": "fallo", "contraseña": hash}
    mock_repo.buscar_auditor_externo_por_usuario.return_value = auditor_db

    resultado = service.logear_auditor_externo("fallo", "incorrecta")
    assert resultado is None

def test_logear_auditor_usuario_no_existe(service, mock_repo):
    mock_repo.buscar_auditor_externo_por_usuario.return_value = None

    resultado = service.logear_auditor_externo("noexiste", "algo")
    assert resultado is None
