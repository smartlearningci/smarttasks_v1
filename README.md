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

## Como ler o código e relacionar requisitos com testes

1. Começar por `docs/01_contexto_e_personas.md` (problema da TaskFlow).
2. Consultar `docs/02_requisitos_e_mvp.md` (RF, RNF, RT, US e matriz).
3. Ler `app/store.py` (regras e memória), depois `app/main.py` (API).
4. Analisar `app/index.html` (interface e chamadas HTTP).
5. Estudar `Dockerfile` e `compose.yaml` (imagem, serviço e portas).
6. Nos testes, procurar os identificadores UT/IT/BDD e as referências RF/US.
7. Executar `bash scripts/run_tests.sh` e consultar `reports/*/results.xml` e `results.html`.

Os comentários documentam o comportamento esperado; não constituem prova de execução. A validação do JavaScript num browser e o arranque real Docker exigem verificações próprias.

## Relatório global dos testes

Após instalar as dependências e executar `bash scripts/run_tests.sh`, abrir `reports/index.html` num browser. O relatório reúne os testes unitários, de integração e BDD, com totais, identificação, objetivo, requisitos, User Stories e detalhes de falhas. Cada suite conserva os seus relatórios em `reports/unit/`, `reports/integration/` e `reports/bdd/`.

**Cores:** verde = aprovado; vermelho = falhou/erro; amarelo = ignorado; cinzento = não executado. Um teste ignorado não significa que passou. Os relatórios anteriores são eliminados antes de cada suite para evitar apresentar resultados antigos. O teste Docker BDD valida a configuração, não o arranque real do contentor.

## Resolução de problemas na instalação

Se surgir `No module named 'app.store'`, `fixture 'client' not found`, ausência de testes BDD ou `requirements.txt` inexistente, confirmar que a cópia do repositório está completa com `git pull origin main` e `git status`. O ficheiro `pytest.ini` define a raiz de importação; `tests/conftest.py` fornece a fixture `client`; `tests/bdd/test_steps.py` liga cenários Gherkin ao pytest. O script de testes verifica os ficheiros obrigatórios antes de iniciar. No Linux com Conda, desativar o ambiente Conda antes de ativar `.venv`, se necessário. Os relatórios são gerados localmente e não devem ser confundidos com aprovação quando há erros de preparação.
