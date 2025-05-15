import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ['mongodb_url'] = 'mongodb://localhost:27017/test'
os.environ['API_KEY'] = 'fake-key'

from dotenv import load_dotenv



import pytest
from Service.AuditorIServiceImp import AuditorInternoServiceImp
from Model.AuditorIModel import AuditorInternoModel
from unittest.mock import MagicMock
import bcrypt

load_dotenv()


@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def service(mock_repo):
    return AuditorInternoServiceImp(repo=mock_repo)

def test_crear_auditor_interno_valido(service, mock_repo):
    auditor = AuditorInternoModel(nombre="Laura", usuario="laura123", contraseña="123456", compañia="Acme Corp")
    mock_repo.crear_auditor_interno.return_value = auditor

    resultado = service.crear_auditor_interno(auditor)

    assert resultado.nombre == "Laura"
    mock_repo.crear_auditor_interno.assert_called_once()

def test_crear_auditor_interno_invalido(service):
    with pytest.raises(ValueError):
        service.crear_auditor_interno(None)

def test_listar_auditores_internos(service, mock_repo):
    mock_repo.listar_auditores_internos.return_value = [
        AuditorInternoModel(nombre="Mario", usuario="mario123", contraseña="clave", compañia="Acme Corp")
    ]

    resultado = service.listar_auditores_internos()
    assert len(resultado) == 1

def test_logear_auditor_interno_valido(service, mock_repo):
    password_plano = "mi_clave"
    password_hash = bcrypt.hashpw(password_plano.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    auditor = {
        "_id": "123abc",
        "nombre": "Sofía",
        "usuario": "sofia123",
        "contraseña": password_hash
    }
    mock_repo.buscar_auditor_interno_por_usuaroi.return_value = auditor

    resultado = service.logear_auditor_interno("sofia123", "mi_clave")
    assert resultado["nombre"] == "Sofía"
    assert resultado["_id"] == "123abc"

def test_logear_auditor_interno_password_incorrecto(service, mock_repo):
    hash_correcto = bcrypt.hashpw("correcta".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    auditor = {"_id": "id123", "usuario": "fallo", "contraseña": hash_correcto}
    mock_repo.buscar_auditor_interno_por_usuaroi.return_value = auditor

    resultado = service.logear_auditor_interno("fallo", "incorrecta")
    assert resultado is None

def test_logear_auditor_interno_no_existe(service, mock_repo):
    mock_repo.buscar_auditor_interno_por_usuaroi.return_value = None

    resultado = service.logear_auditor_interno("nadie", "clave")
    assert resultado is None
