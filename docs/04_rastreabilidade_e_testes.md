# SmartTasks — Rastreabilidade e verificação

## Matriz de requisitos funcionais
| US | RF | Critério resumido | Teste automatizado |
| --- | --- | --- | --- |
| US-01, US-05 | RF-01 | Lista vazia e tarefas existentes | test_list_empty; test_create_and_list; test_multiple_tasks |
| US-02 | RF-02 | Título obrigatório, descrição opcional, estado Aberta | test_create_and_list; test_create_with_description; test_invalid_title |
| US-03 | RF-03 | Concluir e refletir estado | test_complete_and_reopen; test_missing_task |
| US-04 | RF-04 | Reabrir e refletir estado | test_complete_and_reopen; test_missing_task |
| US-01 a US-06 | RF-05 | API HTTP com respostas e erros apropriados | test_list_empty; test_create_and_list; test_complete_and_reopen; test_invalid_title; test_missing_task |
| US-06 | RF-06 | GET /health devolve HTTP 200 | test_health |

## Requisitos não funcionais
| RNF | Evidência / verificação | Estado |
| --- | --- | --- |
| RNF-01 | Abrir http://localhost:8080 após Docker Compose | Manual, pendente |
| RNF-02 | docker compose config; build; up; confirmar dois serviços, aplicação em 127.0.0.1:8080 e db sem porta publicada | Manual, pendente |
| RNF-03 | test_html_interface; experimentar formulário e botões no browser | Parcial: teste automatizado de HTML; browser pendente |
| RNF-04 | Inspeção de app/main.py, app/models.py e app/store.py | Inspeção estrutural |
| RNF-05 | T-18 (nova instância lê dados); reiniciar container e confirmar conservação das tarefas | Integração PostgreSQL T-18; reinício real pendente |
| RNF-06 | Docstrings com US/RF/RNF; revisão dos testes e README | Inspeção documental |

## Execução e limitações
A V1 registou 13 testes aprovados. Na V2, os testes de contrato HTTP usam um duplo de armazenamento e os testes T-14 a T-20 exigem uma base PostgreSQL de testes. Não apresentar testes não executados como aprovados. Docker, integração e browser necessitam de validação no ambiente disponível.

## Validação manual sugerida
1. `docker compose config` e `docker compose build`.
2. `docker compose up -d`; abrir http://localhost:8080 e criar, listar, concluir e reabrir.
3. `curl http://localhost:8080/health` e verificar HTTP 200.
4. Criar uma tarefa, reiniciar apenas o container da aplicação e confirmar que a tarefa permanece.
5. `docker compose down`.

**Fora do âmbito:** filas, login, notificações, CI/CD e serviços pagos.

## V2 — Testes de persistência PostgreSQL

| Teste | User Stories | Requisitos | Objetivo e resultado esperado |
| --- | --- | --- | --- |
| T-14 | US-02 | RF-02, RF-05 | Criar tarefa por POST; HTTP 201 e estado Aberta |
| T-15 | US-01, US-05 | RF-01 | Listar duas tarefas efetivamente gravadas |
| T-16 | US-03 | RF-03 | Concluir e observar estado Concluída na consulta |
| T-17 | US-04 | RF-04 | Reabrir e observar estado Aberta |
| T-18 | US-01, US-02 | RNF-05 | Nova instância TaskStore recupera dados gravados |
| T-19 | — | RNF-04, RNF-05 | Inicializar esquema duas vezes sem perda de tarefas |
| T-20 | US-02, US-03, US-04 | RF-02 a RF-05 | Preservar respostas HTTP 422 e 404 |

**Segurança dos testes:** `TEST_DATABASE_URL` deve apontar para uma base separada cujo nome termina em `_test`. Cada teste cria um esquema temporário com identificador único, removendo apenas esse esquema após terminar. Nunca executar os testes de integração sobre a base `smarttasks` utilizada pelos formandos.

**Estado de execução nesta entrega:** testes de contrato e integração não devem ser considerados executados até validação num ambiente com dependências e PostgreSQL. A matriz descreve cobertura prevista, não certificação de execução.
