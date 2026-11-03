Feature: Sofia verifica o serviço
  # BDD-10 | RF-08 | US-10
  Scenario: US-10 Verificar saúde
    Given que a aplicação está disponível
    When consulto o health check
    Then recebo HTTP 200

  # BDD-12 | RNF-05 | US-12
  Scenario: US-12 Verificar modularidade
    Given que o projeto está disponível
    When verifico os módulos
    Then a API e o armazenamento estão separados

  # BDD-09 | RT-04/05/06 | US-09
  Scenario: US-09 Validar execução Docker
    Given que Docker está disponível
    When verifico a configuração Docker
    Then existe um serviço com porta local correta

  # BDD-11 | RNF-06 | US-11
  Scenario: US-11 Validar relatórios de testes
    Given que os relatórios de testes foram gerados
    When verifico os relatórios
    Then existem relatórios XML e HTML
