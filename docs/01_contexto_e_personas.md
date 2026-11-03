# SmartTasks — Contexto e personas

## 1. Empresa e problema
A TaskFlow é uma empresa fictícia de serviços com 25 colaboradores. As tarefas internas são atualmente geridas por emails, mensagens e reuniões, sem lista central. Isto dificulta saber que tarefas existem e quais estão concluídas.

## 2. Objetivos
- Centralizar o registo e a consulta das tarefas numa aplicação web local.
- Permitir criar, concluir e reabrir tarefas com apenas dois estados.
- Facilitar o acompanhamento visual do trabalho.
- Demonstrar, numa formação de Cloud Computing, a passagem de requisitos a testes, API, containerização e evolução arquitetural.

## 3. Personas
| Persona | Papel | Necessidade | Utilização prevista |
|---|---|---|---|
| Ana Martins | Colaboradora | Registar e acompanhar atividades | Consultar, criar, concluir e reabrir tarefas |
| Miguel Costa | Responsável de equipa | Acompanhar o trabalho | Consultar tarefas, descrições e estados atualizados |
| Sofia Almeida | Responsável de TI | Manter o serviço operacional | Iniciar a aplicação, verificar saúde, executar testes e manter o código |

As personas são perspetivas de utilização, **não perfis de autorização**: não existe login, controlo de acesso ou atribuição de tarefas. Qualquer utilizador da interface pode executar as operações disponíveis.

## 4. Âmbito pedagógico e limites
O MVP disponibiliza uma única lista partilhada de tarefas, criação com título obrigatório e descrição opcional, conclusão e reabertura. Não inclui edição, eliminação, responsáveis, prioridades, datas-limite, filtros, pesquisa, autenticação, notificações ou base de dados. Os dados em memória perdem-se quando o processo reinicia.

## 5. Lacunas identificadas e resolvidas na especificação
| ID | Lacuna | Decisão para o MVP |
|---|---|---|
| L-01 | Lista vazia | Mostrar «Não existem tarefas» |
| L-02 | Título inválido | Rejeitar vazio ou apenas espaços |
| L-03 | Identificação | Gerar ID único automaticamente |
| L-04 | Transição repetida | Rejeitar conclusão de concluída e reabertura de pendente |
| L-05 | ID inexistente | Responder HTTP 404 |
| L-06 | Reinício | Perda de tarefas documentada e verificável |
| L-07 | Testes ausentes | pytest e pytest-bdd |
| L-08 | Relatórios ausentes | XML JUnit e HTML por categoria |
| L-09 | Rastreabilidade ausente | Matriz requisito–história–cenário–teste |
| L-10 | Docker não validado | Verificação automatizada de integração local |

Estas decisões apenas explicitam regras necessárias para implementar e testar o âmbito aprovado.
