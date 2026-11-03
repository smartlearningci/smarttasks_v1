Feature: Ana gere tarefas
  Scenario: US-01 Lista vazia
    Given que a lista está vazia
    When consulto a lista de tarefas
    Then recebo uma lista vazia

  Scenario: US-02 Criar tarefa
    Given que a lista está vazia
    When crio uma tarefa com título válido
    Then a tarefa fica Pendente

  Scenario: US-02 Rejeitar título vazio
    Given que a lista está vazia
    When crio uma tarefa com título vazio
    Then recebo erro de validação

  Scenario: US-03 Concluir tarefa
    Given que existe uma tarefa Pendente
    When concluo a tarefa
    Then a tarefa fica Concluída

  Scenario: US-04 Reabrir tarefa
    Given que existe uma tarefa Concluída
    When reabro a tarefa
    Then a tarefa fica Pendente
