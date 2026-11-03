Feature: Miguel acompanha tarefas
  Scenario: US-05 Consultar lista partilhada
    Given que existem duas tarefas
    When consulto a lista de tarefas
    Then vejo duas tarefas

  Scenario: US-06 Distinguir estados
    Given que existem tarefas em dois estados
    When consulto a lista de tarefas
    Then vejo Pendente e Concluída

  Scenario: US-07 Consultar título e descrição
    Given que existe uma tarefa com descrição
    When consulto a lista de tarefas
    Then vejo o título e a descrição

  Scenario: US-08 Consultar estado atualizado
    Given que existe uma tarefa Pendente
    When concluo a tarefa
    And consulto a lista de tarefas
    Then a tarefa fica Concluída
