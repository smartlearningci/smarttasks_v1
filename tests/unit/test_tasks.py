"""Testes unitários — RNF-06 e matriz de rastreabilidade.

test_empty_and_creation: UT-01/02/05/06/11, RF-01/02, US-01/02, BDD-01/02.
test_invalid_title: UT-03/04, RF-03, US-02, BDD-02.
test_transitions: UT-07/08/09/10, RF-04/05, US-03/04, BDD-03/04.
test_store_isolation: UT-12, RT-07, US-12.
"""
import pytest
from app.store import InvalidTransition, NotFound, TaskStore

def test_empty_and_creation():
    store=TaskStore()
    assert store.list()==[]
    a=store.create("  Reunião  ","Notas")
    b=store.create("Relatório")
    assert a=={"id":1,"titulo":"Reunião","descricao":"Notas","estado":"Pendente"}
    assert b["id"]!=a["id"] and b["descricao"]==""
    assert len(store.list())==2

@pytest.mark.parametrize("title",["","  ","\t"])
def test_invalid_title(title):
    with pytest.raises(ValueError):
        TaskStore().create(title)

def test_transitions():
    store=TaskStore()
    task_id=store.create("Teste")["id"]
    assert store.complete(task_id)["estado"]=="Concluída"
    with pytest.raises(InvalidTransition):store.complete(task_id)
    assert store.reopen(task_id)["estado"]=="Pendente"
    with pytest.raises(InvalidTransition):store.reopen(task_id)
    with pytest.raises(NotFound):store.complete(999)

def test_store_isolation():
    first,second=TaskStore(),TaskStore()
    first.create("Só na primeira")
    assert second.list()==[]
