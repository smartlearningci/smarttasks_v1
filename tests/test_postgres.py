"""T-14 a T-20: testes reais de integração PostgreSQL.

Só correm quando TEST_DATABASE_URL aponta para uma BD de testes com nome
terminado em '_test'. Cada teste usa um esquema próprio e descartável;
NUNCA se apagam tabelas da base smarttasks de produção/formação.
"""
import os
import uuid

import pytest
from fastapi.testclient import TestClient

from app import db, main
from app.models import TaskCreate
from app.store import TaskStore


@pytest.fixture
def pg(monkeypatch):
    """Criar esquema isolado; remover apenas esse esquema no fim do teste."""
    psycopg = pytest.importorskip("psycopg")
    from psycopg import sql

    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        pytest.skip("Definir TEST_DATABASE_URL para uma BD separada *_test")

    # Validar o nome da BD antes de executar qualquer comando de limpeza.
    from urllib.parse import urlsplit
    database = urlsplit(url).path.lstrip("/")
    if not database.endswith("_test"):
        pytest.fail("TEST_DATABASE_URL deve apontar para uma BD *_test")

    schema = "test_" + uuid.uuid4().hex
    with psycopg.connect(url, autocommit=True) as connection:
        connection.execute(
            sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(schema))
        )

    original_connect = db.connect

    def test_connect():
        from psycopg.rows import dict_row
        return psycopg.connect(
            url, options=f"-c search_path={schema}", row_factory=dict_row
        )

    monkeypatch.setattr(db, "connect", test_connect)
    # store.py importou a função diretamente: atualizar a referência também.
    import app.store as store_module
    monkeypatch.setattr(store_module, "connect", test_connect)
    monkeypatch.setattr(main, "initialize_schema", db.initialize_schema)
    monkeypatch.setattr(main, "store", TaskStore())

    try:
        db.initialize_schema()
        yield TestClient(main.app)
    finally:
        with psycopg.connect(url, autocommit=True) as connection:
            connection.execute(
                sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(schema))
            )


def test_t14_create(pg):
    """T-14 | US-02; RF-02/RF-05: POST grava tarefa e devolve 201/Aberta."""
    response = pg.post("/api/tasks", json={"title": "Tarefa persistente"})
    assert response.status_code == 201
    assert response.json()["status"] == "Aberta"


def test_t15_list(pg):
    """T-15 | US-01/US-05; RF-01: GET lista tarefas gravadas em PostgreSQL."""
    pg.post("/api/tasks", json={"title": "Primeira"})
    pg.post("/api/tasks", json={"title": "Segunda"})
    assert len(pg.get("/api/tasks").json()) == 2


def test_t16_complete(pg):
    """T-16 | US-03; RF-03: PATCH concluir grava Concluída na BD."""
    task = pg.post("/api/tasks", json={"title": "Concluir"}).json()
    assert pg.patch(f"/api/tasks/{task['id']}/complete").json()["status"] == "Concluída"
    assert pg.get("/api/tasks").json()[0]["status"] == "Concluída"


def test_t17_reopen(pg):
    """T-17 | US-04; RF-04: PATCH reabrir grava Aberta na BD."""
    task = pg.post("/api/tasks", json={"title": "Reabrir"}).json()
    pg.patch(f"/api/tasks/{task['id']}/complete")
    assert pg.patch(f"/api/tasks/{task['id']}/reopen").json()["status"] == "Aberta"


def test_t18_persist_new_store(pg):
    """T-18 | US-01/US-02; RNF-05: novo TaskStore lê a tarefa já gravada."""
    pg.post("/api/tasks", json={"title": "Conservar"})
    assert TaskStore().list_tasks()[0].title == "Conservar"


def test_t19_schema_idempotent(pg):
    """T-19 | RNF-04/RNF-05: inicialização repetida não elimina dados."""
    pg.post("/api/tasks", json={"title": "Não apagar"})
    db.initialize_schema()
    db.initialize_schema()
    assert pg.get("/api/tasks").json()[0]["title"] == "Não apagar"


def test_t20_errors(pg):
    """T-20 | US-02/US-03/US-04; RF-02 a RF-05: 422 e 404 preservados."""
    assert pg.post("/api/tasks", json={"title": "   "}).status_code == 422
    assert pg.patch("/api/tasks/999/complete").status_code == 404
    assert pg.patch("/api/tasks/999/reopen").status_code == 404
