"""API HTTP SmartTasks — RF-01 a RF-08, US-01 a US-08 e US-10.

GET /health (RF-08) devolve 200; GET /api/tasks (RF-01/06) lista;
POST /api/tasks (RF-02/03) cria com 201 ou validação 422;
POST /api/tasks/{id}/complete e /reopen (RF-04/05) mudam estado.
ID inexistente -> 404; transição inválida -> 409.
O armazenamento em memória reinicia com o processo (RT-07).
"""
from pathlib import Path
from typing import Annotated
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, StringConstraints, field_validator
from app.store import InvalidTransition, NotFound, TaskStore

app = FastAPI(title="SmartTasks")
store = TaskStore()

class TaskCreate(BaseModel):
    titulo: Annotated[str, StringConstraints(min_length=1)]
    descricao: str = ""

    @field_validator("titulo")
    @classmethod
    def valid_title(cls, value):
        if not value.strip():
            raise ValueError("O título é obrigatório.")
        return value.strip()

@app.get("/")
def home():
    return FileResponse(Path(__file__).parent / "index.html")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/tasks")
def list_tasks():
    return store.list()

@app.post("/api/tasks", status_code=201)
def create_task(task: TaskCreate):
    return store.create(task.titulo, task.descricao)

def change_state(task_id: int, action: str):
    try:
        return store.complete(task_id) if action == "complete" else store.reopen(task_id)
    except NotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except InvalidTransition as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc

@app.post("/api/tasks/{task_id}/complete")
def complete_task(task_id: int):
    return change_state(task_id, "complete")

@app.post("/api/tasks/{task_id}/reopen")
def reopen_task(task_id: int):
    return change_state(task_id, "reopen")
