"""Testes unitários SmartTasks — regras de negócio sem HTTP.

Cada teste documenta objetivo, requisitos, história e resultado esperado.
A correspondência entre testes e requisitos também aparece no relatório global.
"""
import pytest
from app.store import InvalidTransition, NotFound, TaskStore


def test_empty_and_creation():
    """UT-01/02/05/06/11 | RF-01/02/06 | US-01/02 | BDD-01/02.

    Objetivo: verificar lista inicialmente vazia, criação com e sem descrição,
    remoção de espaços exteriores, IDs distintos e estado inicial Pendente.
    Esperado: duas tarefas listadas, sem perda dos dados fornecidos.
    """
    store = TaskStore()
    assert store.list() == []
    a = store.create("  Reunião  ", "Notas")
    b = store.create("Relatório")
    assert a == {"id": 1, "titulo": "Reunião", "descricao": "Notas", "estado": "Pendente"}
    assert b["id"] != a["id"] and b["descricao"] == ""
    assert len(store.list()) == 2


@pytest.mark.parametrize("title", ["", "  ", "\t"], ids=["vazio", "espacos", "tabulacao"])
def test_invalid_title(title):
    """UT-03/04 | RF-03 | US-02 | BDD-02.

    Objetivo: rejeitar títulos vazios ou compostos apenas por espaços.
    Esperado: ValueError; nenhuma tarefa inválida pode ser criada.
    """
    with pytest.raises(ValueError):
        TaskStore().create(title)


def test_transitions():
    """UT-07/08/09/10 | RF-04/05/07 | US-03/04 | BDD-03/04.

    Objetivo: concluir e reabrir uma tarefa; impedir ações repetidas
    e operações sobre identificadores inexistentes.
    Esperado: estados corretos e exceções de domínio explícitas.
    """
    store = TaskStore()
    task_id = store.create("Teste")["id"]
    assert store.complete(task_id)["estado"] == "Concluída"
    with pytest.raises(InvalidTransition):
        store.complete(task_id)
    assert store.reopen(task_id)["estado"] == "Pendente"
    with pytest.raises(InvalidTransition):
        store.reopen(task_id)
    with pytest.raises(NotFound):
        store.complete(999)


def test_store_isolation():
    """UT-12 | RT-07 | US-12.

    Objetivo: confirmar que instâncias de armazenamento não partilham dados.
    Esperado: a segunda instância começa vazia; não há persistência externa.
    """
    first, second = TaskStore(), TaskStore()
    first.create("Só na primeira")
    assert second.list() == []
