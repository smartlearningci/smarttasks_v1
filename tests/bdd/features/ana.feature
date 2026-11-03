Feature: Ana gere tarefas
  # BDD-01 | RF-01/06 | US-01 | Objetivo: verificar lista vazia; esperado: resposta sem tarefas.
  Scenario: US-01 Lista vazia
    Given que a lista está vazia
    When consulto a lista de tarefas
    Then recebo uma lista vazia

  # BDD-02 | RF-02/03 | US-02 | Objetivo: criar tarefa válida; esperado: estado Pendente.
  Scenario: US-02 Criar tarefa
    Given que a lista está vazia
    When crio uma tarefa com título válido
    Then a tarefa fica Pendente

  # BDD-02 | RF-03 | US-02 | Objetivo: rejeitar título vazio; esperado: erro de validação.
  Scenario: US-02 Rejeitar título vazio
    Given que a lista está vazia
    When crio uma tarefa com título vazio
    Then recebo erro de validação

  # BDD-03 | RF-04 | US-03 | Objetivo: concluir tarefa; esperado: estado Concluída.
  Scenario: US-03 Concluir tarefa
    Given que existe uma tarefa Pendente
    When concluo a tarefa
    Then a tarefa fica Concluída

  # BDD-04 | RF-05 | US-04 | Objetivo: reabrir tarefa; esperado: estado Pendente.
  Scenario: US-04 Reabrir tarefa
    Given que existe uma tarefa Concluída
    When reabro a tarefa
    Then a tarefa fica Pendente
