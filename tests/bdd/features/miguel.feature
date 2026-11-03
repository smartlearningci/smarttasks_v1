Feature: Miguel acompanha tarefas
  # BDD-05 | RF-01 | US-05 | Objetivo: consultar lista partilhada; esperado: duas tarefas.
  Scenario: US-05 Consultar lista partilhada
    Given que existem duas tarefas
    When consulto a lista de tarefas
    Then vejo duas tarefas

  # BDD-06 | RF-06 | US-06 | Objetivo: distinguir estados; esperado: Pendente e Concluída.
  Scenario: US-06 Distinguir estados
    Given que existem tarefas em dois estados
    When consulto a lista de tarefas
    Then vejo Pendente e Concluída

  # BDD-07 | RF-01/02 | US-07 | Objetivo: ler conteúdo; esperado: título e descrição.
  Scenario: US-07 Consultar título e descrição
    Given que existe uma tarefa com descrição
    When consulto a lista de tarefas
    Then vejo o título e a descrição

  # BDD-08 | RF-04/05, RNF-03 | US-08 | Objetivo: acompanhar atualização; esperado: Concluída.
  Scenario: US-08 Consultar estado atualizado
    Given que existe uma tarefa Pendente
    When concluo a tarefa
    And consulto a lista de tarefas
    Then a tarefa fica Concluída
