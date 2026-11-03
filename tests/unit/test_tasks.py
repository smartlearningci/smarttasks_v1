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
