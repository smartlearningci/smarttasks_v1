# SmartTasks — Arquitetura V2 com PostgreSQL

## Continuidade funcional
Mantêm-se interface HTML, FastAPI, os endpoints HTTP e os modelos da V1. A V2 substitui apenas a camada de armazenamento.

## Componentes
- `app/main.py`: API e inicialização do esquema durante o arranque.
- `app/models.py`: modelos e validações da API, inalterados.
- `app/store.py`: operações SQL parametrizadas com a mesma interface da V1.
- `app/db.py`: ligação por variáveis PGHOST, PGPORT, PGDATABASE, PGUSER e PGPASSWORD; criação idempotente da tabela `tasks`.
- `compose.yaml`: serviço `smarttasks` depende do healthcheck do serviço `db` (PostgreSQL 17).
- `postgres_data`: volume nomeado que conserva dados após reinício/recriação.
- `app/static/index.html`: interface existente, sem alterações.

## Fluxo de dados
```text
Browser localhost:8080
  → smarttasks: FastAPI (porta 8000)
    → TaskStore (SQL parametrizado)
      → db:5432 (rede interna Compose)
        → volume postgres_data
```

A porta 5432 não é publicada no computador. As credenciais são fornecidas pelo ficheiro local `.env`, excluído do Git. Não existem credenciais reais no repositório.

## Inicialização do esquema
No arranque da API, `initialize_schema()` executa `CREATE TABLE IF NOT EXISTS tasks`. A tabela contém `id`, `title`, `description` e `status`. Não executa `DROP`, `TRUNCATE` ou apagamentos. Para alterações estruturais futuras, será necessária migração explícita.

## Testes e limites
- `tests/test_api.py`: contrato HTTP com armazenamento simulado, sem tocar em dados reais.
- `tests/test_postgres.py`: T-14 a T-20 numa base separada `*_test` com esquemas temporários isolados.
- A validação de reinício real, acesso pelo browser e Docker deve ser executada no computador dos formandos.

## Evoluções futuras fora do âmbito
Filas, autenticação, notificações, CI/CD, observabilidade avançada e serviços pagos. Não foram acrescentados nesta V2.
