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

# Función auxiliar para encriptar contraseña
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def service(mock_repo):
    return AuditorInternoServiceImp(repo=mock_repo)

def test_login_exitoso(service, mock_repo):
    hashed = hash_password("clave123")
    mock_repo.buscar_auditor_interno_por_usuario.return_value = {
        "_id": "abc123",
        "usuario": "admin",
        "contraseña": hashed
    }
    result = service.logear_auditor_interno("admin", "clave123")
    assert result is not None
    assert result["_id"] == "abc123"

def test_login_fallido(service, mock_repo):
    hashed = hash_password("clave123")
    mock_repo.buscar_auditor_interno_por_usuario.return_value = {
        "usuario": "admin",
        "contraseña": hashed
    }
    result = service.logear_auditor_interno("admin", "otra_clave")
    assert result is None

def test_crear_auditor_interno_valido(service, mock_repo):
    auditor = AuditorInternoModel(nombre="Carlos", usuario="carlos123", contraseña="abc123", compañia="Acme Corp")
    mock_repo.crear_auditor_interno.return_value = auditor
    resultado = service.crear_auditor_interno(auditor)
    assert resultado.nombre == "Carlos"

def test_crear_auditor_interno_invalido(service):
    with pytest.raises(ValueError):
        service.crear_auditor_interno(AuditorInternoModel(nombre="", usuario="u", contraseña="c"))
