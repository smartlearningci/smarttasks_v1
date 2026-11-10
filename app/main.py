"""Camada HTTP SmartTasks (RF-01 a RF-06).

As rotas e os formatos de resposta permanecem iguais aos do MVP V1.
A persistência fica isolada em app/store.py e app/db.py (RNF-04).
"""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from .db import initialize_schema
from .models import Task, TaskCreate
from .store import TaskStore


@asynccontextmanager
async def lifespan(application: FastAPI):
    """RNF-05: inicializar a tabela antes de aceitar pedidos HTTP.

    CREATE TABLE IF NOT EXISTS não apaga tarefas existentes.
    Se a BD não estiver acessível, o arranque falha visivelmente.
    """
    initialize_schema()
    yield


app = FastAPI(title="SmartTasks", version="1.0.0", lifespan=lifespan)
store = TaskStore()


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    """US-01/US-02; RNF-01/RNF-03: servir a interface HTML existente."""
    return FileResponse(Path(__file__).parent / "static" / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    """US-06; RF-06: manter a resposta HTTP 200 do MVP."""
    return {"status": "ok"}


@app.get("/api/tasks", response_model=list[Task])
def list_tasks() -> list[Task]:
    """US-01/US-05; RF-01/RF-05: devolver tarefas existentes."""
    return store.list_tasks()


@app.post("/api/tasks", response_model=Task, status_code=201)
def create_task(data: TaskCreate) -> Task:
    """US-02; RF-02/RF-05: criar tarefa com entrada validada."""
    return store.create(data)


@app.patch("/api/tasks/{task_id}/complete", response_model=Task)
def complete_task(task_id: int) -> Task:
    """US-03; RF-03/RF-05: concluir tarefa ou responder 404."""
    task = store.set_status(task_id, "Concluída")
    if task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    return task


@app.patch("/api/tasks/{task_id}/reopen", response_model=Task)
def reopen_task(task_id: int) -> Task:
    """US-04; RF-04/RF-05: reabrir tarefa ou responder 404."""
    task = store.set_status(task_id, "Aberta")
    if task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    return task
