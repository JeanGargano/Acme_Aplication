import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ['mongodb_url'] = 'mongodb://localhost:27017/test'
os.environ['API_KEY'] = 'fake-key'


from dotenv import load_dotenv
import pytest
from unittest.mock import MagicMock
from Service.PlanAccionServiceImp import PlanDeAccionServiceImp
from Model.PlanAccionModel import PlanDeAccionModel, Actualizar_estado_comentario, EvidenciaMeta
from bson import ObjectId

load_dotenv()

@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def service(mock_repo):
    return PlanDeAccionServiceImp(repo=mock_repo)

def test_guardar_plan_exitoso(service, mock_repo):
    plan = PlanDeAccionModel(
        objetivo="Plan 1",
        etapas=[],
        auditor_interno="auditor123"
    )
    mock_repo.guardar_plan.return_value = plan

    resultado = service.guardar_plan(plan)

    assert resultado == plan
    mock_repo.guardar_plan.assert_called_once_with(plan)

def test_guardar_plan_falla_con_valor_none(service):
    with pytest.raises(ValueError):
        service.guardar_plan(None)

def test_listar_plan_por_auditor_interno_exitoso(service, mock_repo):
    auditor_id = "abc123"
    mock_repo.listar_planes_por_auditor_interno.return_value = ["plan1", "plan2"]

    resultado = service.listar_plan_por_auditor_interno(auditor_id)

    assert resultado == ["plan1", "plan2"]
    mock_repo.listar_planes_por_auditor_interno.assert_called_once_with(auditor_id)

def test_listar_plan_por_auditor_interno_falla_con_id_vacio(service):
    with pytest.raises(ValueError):
        service.listar_plan_por_auditor_interno(None)

def test_actualizar_estado_comentario_exitoso(service, mock_repo):
    data = Actualizar_estado_comentario(id="123", comentario="Comentario", estado="En progreso")
    mock_repo.actualizar_estado_comentario.return_value = True

    resultado = service.actualizar_estado_comentario(data)

    assert resultado is True
    mock_repo.actualizar_estado_comentario.assert_called_once_with(data.id, data.comentario, data.estado)

def test_actualizar_estado_comentario_falla_con_id_vacio(service):
    # Usar un string vacío para forzar la validación de id vacío
    data = Actualizar_estado_comentario(id="", comentario="Comentario", estado="En progreso")
    with pytest.raises(ValueError):
        service.actualizar_estado_comentario(data)

def test_añadir_evidencias_exitoso(service, mock_repo):
    plan_id = str(ObjectId())
    evidencias = [
        EvidenciaMeta(indice_etapa=0, evidencia="evidencia1"),
        EvidenciaMeta(indice_etapa=1, evidencia="evidencia2")
    ]
    plan_mock = {
        "etapas": [{}, {}]
    }
    mock_repo.obtener_plan_por_id.return_value = plan_mock
    mock_repo.añadir_evidencias.return_value = True

    resultado = service.añadir_evidencias(plan_id, evidencias)

    assert resultado is True
    mock_repo.obtener_plan_por_id.assert_called_once_with(plan_id)
    mock_repo.añadir_evidencias.assert_called_once()

def test_añadir_evidencias_falla_id_invalido(service):
    with pytest.raises(ValueError):
        service.añadir_evidencias("1234", [])

def test_añadir_evidencias_falla_plan_no_encontrado(service, mock_repo):
    plan_id = str(ObjectId())
    mock_repo.obtener_plan_por_id.return_value = None

    with pytest.raises(ValueError):
        service.añadir_evidencias(plan_id, [])

def test_añadir_evidencias_falla_indice_fuera_de_rango(service, mock_repo):
    plan_id = str(ObjectId())
    plan_mock = {
        "etapas": [{}]
    }
    mock_repo.obtener_plan_por_id.return_value = plan_mock
    evidencias = [EvidenciaMeta(indice_etapa=2, evidencia="evidencia")]

    with pytest.raises(ValueError):
        service.añadir_evidencias(plan_id, evidencias)

def test_añadir_evidencias_falla_evidencia_vacia(service, mock_repo):
    plan_id = str(ObjectId())
    plan_mock = {
        "etapas": [{}]
    }
    mock_repo.obtener_plan_por_id.return_value = plan_mock
    evidencias = [EvidenciaMeta(indice_etapa=0, evidencia=" ")]

    with pytest.raises(ValueError):
        service.añadir_evidencias(plan_id, evidencias)
