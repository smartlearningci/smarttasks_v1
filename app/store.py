from dataclasses import dataclass
from threading import Lock

@dataclass
class Task:
    id: int
    titulo: str
    descricao: str
    estado: str = "Pendente"

    def as_dict(self):
        return vars(self).copy()

class TaskError(Exception): pass
class NotFound(TaskError): pass
class InvalidTransition(TaskError): pass

class TaskStore:
    def __init__(self):
        self._tasks = {}
        self._next_id = 1
        self._lock = Lock()

    def list(self):
        with self._lock:
            return [task.as_dict() for task in self._tasks.values()]

    def create(self, titulo, descricao=""):
        if not isinstance(titulo, str) or not titulo.strip():
            raise ValueError("O título é obrigatório.")
        with self._lock:
            task = Task(self._next_id, titulo.strip(), descricao or "")
            self._tasks[task.id] = task
            self._next_id += 1
            return task.as_dict()

    def transition(self, task_id, from_state, to_state):
        with self._lock:
            task = self._tasks.get(task_id)
            if task is None:
                raise NotFound("Tarefa não encontrada.")
            if task.estado != from_state:
                raise InvalidTransition("A tarefa já está neste estado.")
            task.estado = to_state
            return task.as_dict()

    def complete(self, task_id):
        return self.transition(task_id, "Pendente", "Concluída")

    def reopen(self, task_id):
        return self.transition(task_id, "Concluída", "Pendente")
