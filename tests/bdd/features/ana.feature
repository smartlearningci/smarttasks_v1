Feature: Ana gere tarefas
  # BDD-01 | RF-01/06 | US-01
  Scenario: US-01 Lista vazia
    Given que a lista está vazia
    When consulto a lista de tarefas
    Then recebo uma lista vazia

  # BDD-02 | RF-02/03 | US-02
  Scenario: US-02 Criar tarefa
    Given que a lista está vazia
    When crio uma tarefa com título válido
    Then a tarefa fica Pendente

  # BDD-02 | RF-03 | US-02
  Scenario: US-02 Rejeitar título vazio
    Given que a lista está vazia
    When crio uma tarefa com título vazio
    Then recebo erro de validação

  # BDD-03 | RF-04 | US-03
  Scenario: US-03 Concluir tarefa
    Given que existe uma tarefa Pendente
    When concluo a tarefa
    Then a tarefa fica Concluída

  # BDD-04 | RF-05 | US-04
  Scenario: US-04 Reabrir tarefa
    Given que existe uma tarefa Concluída
    When reabro a tarefa
    Then a tarefa fica Pendente
