"""Testes da API — US, requisitos, objetivo e resultado esperado.

Estes testes usam uma implementação em memória APENAS COMO DUPLO DE TESTE:
validam o contrato HTTP sem alterar a base de dados real. A persistência
PostgreSQL é verificada separadamente em tests/test_postgres.py.
"""
import pytest
from fastapi.testclient import TestClient

from app import main
from app.main import app
from app.models import Task


class FakeTaskStore:
    """Duplo mínimo com a mesma interface de TaskStore, só para testes HTTP."""

    def __init__(self):
        self.tasks = {}
        self.next_id = 1

    def list_tasks(self):
        return list(self.tasks.values())

    def create(self, data):
        task = Task(
            id=self.next_id, title=data.title,
            description=data.description, status="Aberta"
        )
        self.tasks[task.id] = task
        self.next_id += 1
        return task

    def set_status(self, task_id, status):
        task = self.tasks.get(task_id)
        if task is not None:
            task.status = status
        return task


@pytest.fixture
def client(monkeypatch):
    """Isola cada teste e dispensa PostgreSQL nos testes de contrato HTTP."""
    monkeypatch.setattr(main, "initialize_schema", lambda: None)
    monkeypatch.setattr(main, "store", FakeTaskStore())
    with TestClient(app) as test_client:
        yield test_client


def test_health(client):
    """US-06 | RF-06: GET /health deve devolver 200 e status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_empty(client):
    """US-01/US-05 | RF-01/RF-05: lista inicial vazia devolve 200 e []."""
    response = client.get("/api/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_create_and_list(client):
    """US-02/US-01 | RF-02/RF-01/RF-05: criar sem descrição e listar Aberta."""
    response = client.post("/api/tasks", json={"title": "  Rever proposta  "})
    assert response.status_code == 201
    task = response.json()
    assert task == {
        "id": 1, "title": "Rever proposta", "description": "", "status": "Aberta"
    }
    assert client.get("/api/tasks").json() == [task]


def test_create_with_description(client):
    """US-02 | RF-02/RF-05: descrição fornecida deve ser conservada."""
    response = client.post(
        "/api/tasks", json={"title": "Preparar reunião", "description": "Notas"}
    )
    assert response.status_code == 201
    assert response.json()["description"] == "Notas"


def test_multiple_tasks(client):
    """US-01/US-05/US-02 | RF-01/RF-02: duas tarefas distintas na lista."""
    for title in ("Primeira", "Segunda"):
        assert client.post("/api/tasks", json={"title": title}).status_code == 201
    tasks = client.get("/api/tasks").json()
    assert [task["id"] for task in tasks] == [1, 2]
    assert [task["title"] for task in tasks] == ["Primeira", "Segunda"]


def test_complete_and_reopen(client):
    """US-03/US-04 | RF-03/RF-04/RF-05: estados mudam também na lista."""
    task = client.post("/api/tasks", json={"title": "Preparar reunião"}).json()
    url = f"/api/tasks/{task['id']}"

    completed = client.patch(f"{url}/complete")
    assert completed.status_code == 200
    assert completed.json()["status"] == "Concluída"
    assert client.get("/api/tasks").json()[0]["status"] == "Concluída"

    reopened = client.patch(f"{url}/reopen")
    assert reopened.status_code == 200
    assert reopened.json()["status"] == "Aberta"
    assert client.get("/api/tasks").json()[0]["status"] == "Aberta"


@pytest.mark.parametrize(
    "payload", [{}, {"title": ""}, {"title": "   "}, {"title": None}]
)
def test_invalid_title(client, payload):
    """US-02 | RF-02/RF-05: título inválido devolve 422 e não cria tarefa."""
    response = client.post("/api/tasks", json=payload)
    assert response.status_code == 422
    assert client.get("/api/tasks").json() == []


def test_missing_task(client):
    """US-03/US-04 | RF-03/RF-04/RF-05: ID inexistente devolve 404."""
    assert client.patch("/api/tasks/999/complete").status_code == 404
    assert client.patch("/api/tasks/999/reopen").status_code == 404


def test_html_interface(client):
    """US-01/US-02 | RNF-03: a página inicial fornece HTML e formulário."""
    response = client.get("/")
    assert response.status_code == 200
    assert "SmartTasks" in response.text
    assert "create-form" in response.text
