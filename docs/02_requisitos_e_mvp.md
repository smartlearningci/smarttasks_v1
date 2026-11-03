# SmartTasks — Requisitos, MVP e User Stories

## 1. Classificação
- **RF (funcional):** comportamento observável e regras de negócio.
- **RNF (não funcional):** qualidade verificável do comportamento.
- **RT (técnico):** tecnologia, execução e arquitetura. Python e Docker são RT, não RF.

## 2. Fluxo único
```text
Lista (vazia ou com tarefas)
    |
    +-- Criar (título obrigatório; descrição opcional)
    |      +-- título inválido -> mensagem; sem criação
    |      +-- título válido -> ID único; estado Pendente -> Lista
    |
    +-- Pendente --[Concluir]--> Concluída
    +-- Concluída --[Reabrir]--> Pendente
```
Não existem outros estados ou ramificações. A lista apresenta todas as tarefas; não há filtros nem paginação. Cada tarefa contém apenas `id`, `titulo`, `descricao` e `estado`. A lista começa vazia; não são necessárias tarefas de exemplo.

## 3. Requisitos funcionais
| ID | Requisito | Aceitação |
|---|---|---|
| RF-01 | Listar todas as tarefas | Lista inclui pendentes e concluídas; quando vazia mostra «Não existem tarefas» |
| RF-02 | Criar tarefa | Título obrigatório, descrição opcional, ID único e estado inicial Pendente |
| RF-03 | Validar título | Rejeita título vazio ou só com espaços e mostra mensagem compreensível |
| RF-04 | Concluir | Só Pendente passa a Concluída; repetição é rejeitada sem alterar estado |
| RF-05 | Reabrir | Só Concluída passa a Pendente; repetição é rejeitada sem alterar estado |
| RF-06 | Mostrar estado | Cada tarefa apresenta claramente Pendente ou Concluída |
| RF-07 | API HTTP | Disponibiliza listar, criar, concluir e reabrir; ID inexistente devolve 404; transição inválida devolve 409 |
| RF-08 | Health check | GET /health devolve HTTP 200 e indicador simples de funcionamento |

**Contrato HTTP proposto para testes:** `GET /api/tasks`, `POST /api/tasks`, `POST /api/tasks/{id}/complete`, `POST /api/tasks/{id}/reopen`, `GET /health`. Criar devolve 201; entrada inválida 422; transição inválida 409; ID inexistente 404. Estes caminhos e códigos ficam fixados para evitar ambiguidades de implementação.

## 4. Requisitos não funcionais
| ID | Requisito | Verificação |
|---|---|---|
| RNF-01 | Facilidade de uso | Lista e acesso à criação visíveis no ecrã inicial, sem menus |
| RNF-02 | Interface simples | Um ecrã principal com formulário e ações Concluir/Reabrir |
| RNF-03 | Feedback | Após ação bem-sucedida, lista e estados são atualizados sem recarregamento manual |
| RNF-04 | Erros compreensíveis | Erros de validação e de operação apresentados sem traceback técnico |
| RNF-05 | Modularidade | Inicialização/API, regras de tarefas e armazenamento separados |
| RNF-06 | Testabilidade | Testes automatizados de criação, validação, listagem, estados e health |

## 5. Requisitos técnicos
| ID | Requisito |
|---|---|
| RT-01 | Python 3 |
| RT-02 | FastAPI para API HTTP e interface |
| RT-03 | HTML simples; JavaScript apenas quando necessário |
| RT-04 | Um Dockerfile |
| RT-05 | compose.yaml com um serviço |
| RT-06 | Porta 127.0.0.1:8080 do host para 8000 do container |
| RT-07 | Armazenamento em memória; perda após reinício do processo |
| RT-08 | Dependências em requirements.txt |
| RT-09 | Arranque por docker compose up --build -d |
| RT-10 | Sem credenciais no código ou serviços externos pagos |

## 6. User Stories e rastreabilidade
Cada história é acompanhada por cenário Gherkin no plano de testes. O identificador BDD remete para esse cenário.

| US | Persona | História: Como..., quero..., para... | Requisitos | Evidência prevista |
|---|---|---|---|---|
| US-01 | Ana | Como Ana, quero ver todas as tarefas, para conhecer o trabalho existente | RF-01, RF-06, RNF-01 | BDD-01 |
| US-02 | Ana | Como Ana, quero criar tarefas com título e descrição opcional, para registar atividades | RF-02, RF-03, RNF-04 | BDD-02 |
| US-03 | Ana | Como Ana, quero concluir tarefas pendentes, para assinalar trabalho realizado | RF-04 | BDD-03 |
| US-04 | Ana | Como Ana, quero reabrir tarefas concluídas, para corrigir conclusões prematuras | RF-05 | BDD-04 |
| US-05 | Miguel | Como Miguel, quero consultar a lista partilhada, para acompanhar o trabalho | RF-01 | BDD-05 |
| US-06 | Miguel | Como Miguel, quero identificar o estado de cada tarefa, para distinguir pendentes de concluídas | RF-06 | BDD-06 |
| US-07 | Miguel | Como Miguel, quero ler títulos e descrições, para compreender as atividades | RF-01, RF-02 | BDD-07 |
| US-08 | Miguel | Como Miguel, quero ver alterações de estado atualizadas, para acompanhar a evolução | RF-04, RF-05, RNF-03 | BDD-08 |
| US-09 | Sofia | Como Sofia, quero iniciar o serviço com Docker Compose, para o disponibilizar localmente | RT-04, RT-05, RT-06, RT-09 | BDD-09 + Docker |
| US-10 | Sofia | Como Sofia, quero consultar /health, para verificar o funcionamento | RF-08 | BDD-10 |
| US-11 | Sofia | Como Sofia, quero executar testes automatizados, para validar operações | RNF-06 | BDD-11 + pytest |
| US-12 | Sofia | Como Sofia, quero código modular, para facilitar manutenção | RNF-05, RT-01, RT-02, RT-03, RT-08, RT-10 | BDD-12 + inspeção técnica |

## 7. Cobertura complementar de requisitos
| Requisito | Evidência adicional |
|---|---|
| RF-07 | Testes de integração dos endpoints, 404, 409 e 422 |
| RNF-02 | Verificação da interface de ecrã único |
| RNF-04 | Testes de erros de formulário/API |
| RT-07 | Teste de isolamento da memória e reinício do processo |
| RT-10 | Verificação de dependências e ausência de segredos |
| L-01 a L-10 | Cenários e testes definidos em docs/04_plano_de_testes.md |

## 8. Critério de conclusão
O MVP só é validado quando o serviço inicia, as operações e os erros previstos funcionam, os testes obrigatórios passam e existem relatórios JUnit XML e HTML de cada conjunto executado. Não se afirma que os testes já passaram antes da implementação.

## 9. Rastreabilidade no código e nos testes

Os módulos Python e os ficheiros de suporte devem conter comentários pedagógicos que expliquem a sua função. Os testes unitários e de integração identificam no cabeçalho o nome da função de teste, IDs UT/IT, requisitos RF/RNF/RT e User Stories US. Cada cenário `.feature` identifica em comentário o respetivo BDD, requisito e User Story. O plano detalhado está em `docs/04_plano_de_testes.md`.
