import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import main
from app.store import TaskStore

@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(main, "store", TaskStore())
    with TestClient(app) as test_client:
        yield test_client
