"""Persistência PostgreSQL — US-01 a US-05; RF-01 a RF-05.

A interface pública desta classe é a mesma do MVP em memória.
A API não precisa de conhecer os detalhes das consultas SQL (RNF-04).
"""
from .db import connect
from .models import Task, TaskCreate


class TaskStore:
    """Operações sobre tarefas; cada método abre e fecha a ligação."""

    def list_tasks(self) -> list[Task]:
        """US-01/US-05; RF-01: listar tarefas pela ordem de criação."""
        with connect() as connection:
            rows = connection.execute(
                "SELECT id, title, description, status FROM tasks ORDER BY id"
            ).fetchall()
        return [Task(**row) for row in rows]

    def create(self, data: TaskCreate) -> Task:
        """US-02; RF-02: criar tarefa Aberta e devolver o ID gerado pela BD."""
        with connect() as connection:
            row = connection.execute(
                """
                INSERT INTO tasks (title, description, status)
                VALUES (%s, %s, 'Aberta')
                RETURNING id, title, description, status
                """,
                (data.title, data.description),
            ).fetchone()
        return Task(**row)

    def set_status(self, task_id: int, status: str) -> Task | None:
        """US-03/US-04; RF-03/RF-04: atualizar ou devolver None para 404.

        Os valores são passados como parâmetros, nunca concatenados no SQL.
        """
        with connect() as connection:
            row = connection.execute(
                """
                UPDATE tasks SET status = %s WHERE id = %s
                RETURNING id, title, description, status
                """,
                (status, task_id),
            ).fetchone()
        return Task(**row) if row is not None else None
