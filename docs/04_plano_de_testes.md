# SmartTasks — Plano de testes e relatórios

## 1. Objetivo e âmbito
Validar o MVP por testes unitários, funcionais BDD e de integração, com evidência obrigatória de todas as execuções. **Este documento é uma especificação; os testes Python e ficheiros .feature serão implementados na fase de código, após aprovação.**

## 2. Ferramentas
- `pytest`: testes unitários e de integração.
- `pytest-bdd`: cenários Gherkin executáveis através de funções Python.
- `pytest-html`: relatórios HTML.
- `pytest --junitxml=...`: relatórios JUnit XML.
- `fastapi.testclient.TestClient`: testes HTTP sem necessidade de serviço externo.
- Docker Compose: teste de arranque e acesso local.

## 3. Localização prevista
```text
tests/unit/test_tasks.py
tests/integration/test_api.py
tests/integration/test_docker.py
tests/bdd/features/ana.feature
tests/bdd/features/miguel.feature
tests/bdd/features/sofia.feature
tests/bdd/test_steps.py
tests/conftest.py
reports/unit/
reports/bdd/
reports/integration/
```
Os `.feature` usam palavras-chave Gherkin compatíveis com pytest-bdd. Para evitar incompatibilidades, os cenários executáveis serão escritos com `Feature`, `Scenario`, `Given`, `When`, `Then`, `And`; as histórias e descrições mantêm-se em português.

## 4. Cenários de aceitação em Gherkin
Os identificadores BDD correspondem às User Stories em docs/02_requisitos_e_mvp.md. Os passos abaixo são a especificação a converter em ficheiros .feature e funções Python.

```gherkin
Feature: Ana gere tarefas

  # BDD-01 / US-01
  Scenario: Consultar lista inicialmente vazia
    Given que não existem tarefas
    When Ana consulta a lista
    Then é apresentada a mensagem "Não existem tarefas"

  # BDD-02 / US-02
  Scenario: Criar tarefa sem descrição
    Given que não existem tarefas
    When Ana cria a tarefa "Preparar reunião" sem descrição
    Then a tarefa recebe um identificador único
    And aparece na lista com estado "Pendente"

  Scenario Outline: Rejeitar título inválido
    Given que não existem tarefas
    When Ana tenta criar uma tarefa com o título "<titulo>"
    Then a criação é rejeitada com uma mensagem de validação
    And a lista continua vazia
    Examples:
      | titulo |
      |        |
      |       |

  # BDD-03 / US-03
  Scenario: Concluir uma tarefa pendente
    Given que existe uma tarefa com estado "Pendente"
    When Ana conclui a tarefa
    Then o estado passa a "Concluída"

  # BDD-04 / US-04
  Scenario: Reabrir uma tarefa concluída
    Given que existe uma tarefa com estado "Concluída"
    When Ana reabre a tarefa
    Then o estado passa a "Pendente"
```

```gherkin
Feature: Miguel acompanha tarefas

  # BDD-05 / US-05
  Scenario: Consultar tarefas partilhadas
    Given que existem duas tarefas
    When Miguel consulta a lista
    Then são apresentadas as duas tarefas

  # BDD-06 / US-06
  Scenario: Distinguir estados
    Given que existe uma tarefa "Pendente" e outra "Concluída"
    When Miguel consulta a lista
    Then cada tarefa apresenta o seu estado correto

  # BDD-07 / US-07
  Scenario: Consultar título e descrição
    Given que existe uma tarefa com título e descrição
    When Miguel consulta a tarefa na lista
    Then vê o título e a descrição registados

  # BDD-08 / US-08
  Scenario: Consultar estado atualizado
    Given que existe uma tarefa com estado "Pendente"
    When a tarefa é concluída
    And Miguel consulta a lista atualizada
    Then a tarefa aparece como "Concluída"
```

```gherkin
Feature: Sofia valida a aplicação

  # BDD-09 / US-09
  Scenario: Iniciar serviço local
    Given que Docker e Docker Compose estão disponíveis
    When Sofia inicia o serviço com Docker Compose
    Then a aplicação responde em "http://localhost:8080"

  # BDD-10 / US-10
  Scenario: Verificar saúde da aplicação
    Given que a aplicação está operacional
    When Sofia faz GET em "/health"
    Then recebe HTTP 200

  # BDD-11 / US-11
  Scenario: Executar testes e produzir evidência
    Given que os testes estão instalados
    When Sofia executa a suite de testes
    Then são produzidos relatórios JUnit XML e HTML
    And os relatórios indicam testes aprovados e falhados

  # BDD-12 / US-12
  Scenario: Verificar separação modular
    Given que o código da aplicação está disponível
    When Sofia verifica a estrutura do projeto
    Then a API, as regras de tarefas e o armazenamento estão separados
```

Os cenários BDD-09, BDD-11 e BDD-12 podem usar passos Python que invocam verificações técnicas; não são testes de interface. O BDD-11 não deve invocar recursivamente a própria suite: o seu passo verifica artefactos gerados por uma execução independente. BDD-09 requer Docker disponível e não deve ser confundido com um teste unitário.

## 5. Testes unitários obrigatórios
| ID | Verificação |
|---|---|
| UT-01 | Criar tarefa válida com descrição |
| UT-02 | Criar tarefa válida sem descrição |
| UT-03 | Rejeitar título vazio |
| UT-04 | Rejeitar título só com espaços |
| UT-05 | Gerar identificadores únicos |
| UT-06 | Iniciar tarefa em Pendente |
| UT-07 | Concluir Pendente |
| UT-08 | Reabrir Concluída |
| UT-09 | Rejeitar conclusão repetida |
| UT-10 | Rejeitar reabertura repetida |
| UT-11 | Listar tarefas e lista vazia |
| UT-12 | Isolar armazenamento em memória entre instâncias |

## 6. Integração e verificações técnicas
| ID | Verificação |
|---|---|
| IT-01 | GET /api/tasks |
| IT-02 | POST /api/tasks com 201 |
| IT-03 | POST inválido com 422 |
| IT-04 | POST /api/tasks/{id}/complete |
| IT-05 | POST /api/tasks/{id}/reopen |
| IT-06 | ID inexistente com 404 |
| IT-07 | Transição inválida com 409 |
| IT-08 | GET /health com 200 |
| IT-09 | Docker Compose inicia e responde em localhost:8080 |
| IT-10 | Reinício do processo elimina tarefas em memória |
| IT-11 | Interface contém lista, formulário e ações esperadas |
| IT-12 | Dependências e configuração não contêm credenciais |

A atualização visual sem recarregamento manual (RNF-03) requer teste de interface real ou verificação equivalente do comportamento do JavaScript; TestClient isoladamente não executa JavaScript. Esta lacuna de cobertura deverá ficar assinalada até existir teste adequado.

## 7. Execução e relatórios
Exemplos de comandos a implementar e documentar após existir código:
```bash
python -m pytest tests/unit --junitxml=reports/unit/results.xml --html=reports/unit/results.html --self-contained-html
python -m pytest tests/bdd --junitxml=reports/bdd/results.xml --html=reports/bdd/results.html --self-contained-html
python -m pytest tests/integration --junitxml=reports/integration/results.xml --html=reports/integration/results.html --self-contained-html
```
Os testes que exigem Docker devem ser executados num ambiente com Docker disponível e podem ter comando separado para não bloquear a suite local. O relatório deve identificar data/hora, ambiente, comando, testes executados, aprovados, falhados, ignorados e erros. Um processo de execução deverá preservar os relatórios mesmo quando houver falhas. A pasta `reports/` contém artefactos gerados e deve ficar excluída do controlo de versões, salvo decisão posterior.

## 8. Critério de aprovação e rastreabilidade
- Cada US-01 a US-12 tem pelo menos um cenário BDD-01 a BDD-12.
- RF-01 a RF-08 têm cenários e/ou testes de integração; RNF e RT têm evidência específica conforme matriz.
- Todos os testes obrigatórios executados passam; não há falhas nem erros.
- Existem relatórios XML e HTML para todas as suites executadas.
- Limitações de ambiente e verificações ainda não automatizadas são identificadas expressamente; não se declaram como aprovadas.
- A documentação aprovada não representa evidência de execução de testes.

## 9. Próxima fase
Implementar aplicação, ficheiros .feature, passos pytest-bdd, testes unitários e de integração, mecanismo de geração de relatórios e validação Docker; apresentar plano e obter aprovação antes de publicar código.

## 10. Regra de documentação pedagógica

O código e os ficheiros de suporte (`Dockerfile`, `compose.yaml`, dependências, exclusões e scripts) devem explicar a finalidade das decisões relevantes. Cada teste deve ser rastreável a pelo menos um requisito e, quando aplicável, a uma User Story e a um cenário BDD. Os testes Python incluem um mapa de funções para IDs UT/IT no cabeçalho; os cenários Gherkin incluem os identificadores BDD/US/RF em comentários. Os relatórios XML e HTML são a evidência real de execução, não os comentários.

**Limitações de validação:** BDD-09 verifica a configuração Compose, não prova que o contentor arranca; BDD-11 verifica relatórios previamente gerados; o teste HTTP da interface não executa JavaScript. Estas verificações exigem execução complementar antes de declarar validação completa.
