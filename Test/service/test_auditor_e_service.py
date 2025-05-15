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

def generar_password_segura(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

@pytest.fixture
def mock_repo():
    return MagicMock()

def test_logear_auditor_externo_correcto(mock_repo):
    # Arrange
    contraseña_original = "miPasswordSegura123"
    hash = generar_password_segura(contraseña_original)
    mock_repo.buscar_auditor_externo_por_usuario.return_value = {
        "_id": "fakeid",
        "usuario": "auditor1",
        "contraseña": hash,
        "nombre": "Auditor Uno"
    }

    service = AuditorExternoServiceImp(repo=mock_repo)

    # Act
    result = service.logear_auditor_externo("auditor1", contraseña_original)

    # Assert
    assert result is not None
    assert result["usuario"] == "auditor1"
    assert "_id" in result


def test_logear_auditor_externo_incorrecto(mock_repo):
    # Arrange
    contraseña_original = "miPasswordSegura123"
    hash = generar_password_segura(contraseña_original)
    mock_repo.buscar_auditor_externo_por_usuario.return_value = {
        "_id": "fakeid",
        "usuario": "auditor1",
        "contraseña": hash,
        "nombre": "Auditor Uno"
    }

    service = AuditorExternoServiceImp(repo=mock_repo)

    # Act
    result = service.logear_auditor_externo("auditor1", "claveIncorrecta")

    # Assert
    assert result is None
