"""Testes de integração da API HTTP, sem executar browser ou Docker.

As verificações exercitam a API através do FastAPI TestClient.
"""


def test_health_and_empty_list(client):
    """IT-01/08 | RF-01/08 | US-01/10 | BDD-01/10.

    Objetivo: confirmar que o health check responde e que a lista
    inicial não contém tarefas. Esperado: HTTP 200 e dados corretos.
    """
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/api/tasks").json() == []


def test_create_and_list(client):
    """IT-02 | RF-01/02/07 | US-02 | BDD-02.

    Objetivo: criar uma tarefa pela API e voltar a consultá-la.
    Esperado: HTTP 201, descrição opcional vazia e estado Pendente.
    """
    result = client.post("/api/tasks", json={"titulo": "Preparar reunião"})
    assert result.status_code == 201
    assert result.json()["estado"] == "Pendente"
    assert result.json()["descricao"] == ""
    assert client.get("/api/tasks").json() == [result.json()]


def test_validation(client):
    """IT-03 | RF-03/07 | US-02 | BDD-02.

    Objetivo: rejeitar títulos vazios, espaços e ausência de título.
    Esperado: HTTP 422 e nenhuma tarefa criada.
    """
    for title in ("", "   "):
        assert client.post("/api/tasks", json={"titulo": title}).status_code == 422
    assert client.post("/api/tasks", json={"descricao": "sem título"}).status_code == 422
    assert client.get("/api/tasks").json() == []


def test_complete_reopen_and_errors(client):
    """IT-04/05/06/07 | RF-04/05/07 | US-03/04/08 | BDD-03/04/08.

    Objetivo: testar as duas transições, rejeitar repetições e IDs
    inexistentes. Esperado: 200 nos sucessos, 409 nas repetições e
    404 para identificadores desconhecidos.
    """
    task_id = client.post("/api/tasks", json={"titulo": "Teste"}).json()["id"]
    complete = f"/api/tasks/{task_id}/complete"
    reopen = f"/api/tasks/{task_id}/reopen"
    assert client.post(complete).json()["estado"] == "Concluída"
    assert client.post(complete).status_code == 409
    assert client.post(reopen).json()["estado"] == "Pendente"
    assert client.post(reopen).status_code == 409
    assert client.post("/api/tasks/999/complete").status_code == 404
    assert client.post("/api/tasks/999/reopen").status_code == 404


def test_html(client):
    """IT-11 | RNF-01/02 | US-01/02.

    Objetivo: confirmar a entrega da página HTML e presença dos
    elementos essenciais. Esperado: HTTP 200 e textos da interface.
    Limite: TestClient não executa JavaScript nem valida interação visual.
    """
    response = client.get("/")
    assert response.status_code == 200
    for content in ("SmartTasks", "Criar tarefa", "Não existem tarefas", "Concluir", "Reabrir"):
        assert content in response.text
