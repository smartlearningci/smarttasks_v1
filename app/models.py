"""Modelos da API: entrada validada e resposta (US-02; RF-02)."""
from pydantic import BaseModel, Field, field_validator


class TaskCreate(BaseModel):
    """Dados recebidos na criação: título obrigatório e descrição opcional."""
    title: str = Field(min_length=1)
    description: str = ""

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        """Retira espaços exteriores e rejeita títulos apenas com espaços."""
        value = value.strip()
        if not value:
            raise ValueError("O título não pode estar vazio.")
        return value


class Task(BaseModel):
    """Tarefa devolvida pela API, incluindo identificador e estado."""
    id: int
    title: str
    description: str
    status: str
