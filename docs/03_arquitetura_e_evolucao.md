# SmartTasks — Arquitetura e evolução

## 1. Arquitetura inicial
```text
Browser
  http://localhost:8080
          |
          | HTTP em 127.0.0.1:8080
          v
+--------------------------------------------+
| Docker Compose — um serviço smarttasks      |
| Mapeamento 127.0.0.1:8080 -> container:8000 |
|                                            |
| Python + FastAPI                           |
|  - Interface web HTML simples              |
|  - API HTTP /api/tasks e GET /health       |
|  - Regras de criação e estados             |
|  - Repositório em memória                  |
+--------------------------------------------+
```
Não existe base de dados, volume, fila, serviço cloud ou credencial. A perda de tarefas após reinício é intencional nesta versão.

## 2. Organização proposta
```text
README.md
docs/
  01_contexto_e_personas.md
  02_requisitos_e_mvp.md
  03_arquitetura_e_evolucao.md
  04_plano_de_testes.md
app/                  # aplicação, API, regras e armazenamento
tests/
  unit/               # regras e armazenamento
  integration/        # endpoints e verificação Docker
  bdd/
    features/         # cenários .feature em Gherkin
    test_steps.py     # ligação Gherkin -> Python
  conftest.py
reports/              # relatórios gerados localmente, não versionados
requirements.txt
Dockerfile
compose.yaml
.dockerignore
```
A documentação desta fase descreve a estrutura; não cria ainda código, testes executáveis ou configuração Docker.

## 3. Princípios
- Separar API, regras de negócio e armazenamento para facilitar substituições futuras.
- Manter apenas dois estados e operações mínimas.
- Limitar a publicação da porta no host a 127.0.0.1.
- Não incorporar segredos no código ou na imagem.
- Produzir relatórios de testes reproduzíveis antes de declarar o MVP validado.

## 4. Evolução futura — não implementar no MVP
| Etapa | Possível alteração | Motivo |
|---|---|---|
| PostgreSQL | Substituir repositório em memória por acesso a base de dados | Persistir tarefas |
| Volumes | Volume para os dados do PostgreSQL | Preservar dados entre reinícios |
| Redes internas | Separar tráfego entre aplicação e base de dados | Isolar serviços |
| Filas | Adicionar fila e worker apenas se surgirem tarefas assíncronas | Desacoplar processamento |
| CI/CD | Executar testes, gerar relatórios e construir imagem automaticamente | Validar alterações |
| Observabilidade | Logs estruturados, métricas e monitorização | Diagnosticar funcionamento |

Nenhuma destas etapas constitui funcionalidade aprovada para a primeira versão.

## 5. Validação
A implementação futura deverá incluir pytest, pytest-bdd, testes de integração FastAPI e verificação Docker. Cada execução deverá gerar relatório JUnit XML e HTML, com resultados e falhas identificáveis. Ver docs/04_plano_de_testes.md.
