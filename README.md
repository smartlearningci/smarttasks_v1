# SmartTasks — TaskFlow

MVP pedagógico de gestão de tarefas com Python, FastAPI e Docker. Dados em memória: **as tarefas perdem-se quando o processo reinicia**. Sem login ou base de dados.

## Obter e iniciar

Requisitos: Git e Docker com Docker Compose.

```bash
git clone https://github.com/smartlearningci/smarttasks_v1.git
cd smarttasks_v1
docker compose up --build -d
```

Abrir http://localhost:8080. Verificar saúde em http://localhost:8080/health.

## Operações da API

- `GET /api/tasks` — listar tarefas.
- `POST /api/tasks` — criar, JSON: `{"titulo":"Preparar reunião","descricao":"Opcional"}`.
- `POST /api/tasks/{id}/complete` — concluir.
- `POST /api/tasks/{id}/reopen` — reabrir.
- `GET /health` — saúde.

Estados: `Pendente` e `Concluída`. Erros: 422 para entrada inválida, 404 para ID inexistente e 409 para transição inválida.

## Testes e relatórios

Requisitos locais: Python 3.12 e ambiente virtual.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
bash scripts/run_tests.sh
```

O script produz HTML a partir de JUnit XML, mesmo quando há falhas. Os relatórios HTML/XML são locais e não são versionados. A execução de testes Docker requer Docker disponível; os testes de integração HTTP usam TestClient e não exigem Docker.

## Parar

```bash
docker compose down
```

## Documentação

Consultar `docs/` para contexto, requisitos, arquitetura, User Stories, Gherkin e estratégia de testes.
