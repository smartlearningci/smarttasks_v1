# SmartTasks — Requisitos e MVP

## Funcionalidades incluídas
| ID | Requisito funcional | Critério de aceitação |
| --- | --- | --- |
| RF-01 | Listar tarefas | Ao abrir a interface, são apresentadas as tarefas existentes e o seu estado; uma lista vazia é apresentada sem erro. |
| RF-02 | Criar tarefa | Um título não vazio é obrigatório; a descrição é opcional; uma tarefa válida surge na lista com estado **Aberta**. |
| RF-03 | Concluir tarefa | Uma tarefa aberta pode passar ao estado **Concluída**, refletindo-se na lista. |
| RF-04 | Reabrir tarefa | Uma tarefa concluída pode voltar ao estado **Aberta**, refletindo-se na lista. |
| RF-05 | Disponibilizar API HTTP | A API permite listar, criar, concluir e reabrir tarefas, com respostas HTTP apropriadas. |
| RF-06 | Verificar saúde | `GET /health` devolve HTTP 200 enquanto a aplicação estiver operacional. |

## User Stories do MVP
As personas descrevem necessidades, não permissões: não há autenticação nesta versão.

| ID | Persona | User Story | Critério de aceitação | Requisitos |
| --- | --- | --- | --- | --- |
| US-01 | Ana | Como colaboradora, quero consultar a lista de tarefas para acompanhar o trabalho. | Lista com título e estado; vazia sem erro. | RF-01 |
| US-02 | Ana | Como colaboradora, quero criar tarefas com título e descrição opcional para registar trabalho. | Título obrigatório, rejeição de branco; tarefa criada Aberta. | RF-02 |
| US-03 | Ana | Como colaboradora, quero concluir uma tarefa para assinalar o seu fim. | Estado muda para Concluída na lista. | RF-03 |
| US-04 | Ana | Como colaboradora, quero reabrir uma tarefa concluída para voltar a acompanhá-la. | Estado muda para Aberta na lista. | RF-04 |
| US-05 | Miguel | Como responsável de equipa, quero consultar tarefas e estados para acompanhar a equipa. | Consulta usa a mesma listagem de US-01, sem novas permissões. | RF-01 |
| US-06 | Sofia | Como responsável de TI, quero verificar se a aplicação responde para apoiar a manutenção. | GET /health responde HTTP 200. | RF-06 |

RF-05 (API HTTP) suporta US-01 a US-06. Os RNF são condições transversais de execução e qualidade, não novas funcionalidades.

## Requisitos não funcionais
| ID | Requisito | Critério de aceitação |
| --- | --- | --- |
| RNF-01 | Acesso local | Interface acessível em `http://localhost:8080` com a aplicação em execução. |
| RNF-02 | Docker | Dois serviços Docker Compose (`smarttasks` e `db`), com porta da aplicação `127.0.0.1:8080:8000`; PostgreSQL não publica a porta 5432. |
| RNF-03 | Simplicidade | Interface HTML simples, sem autenticação. |
| RNF-04 | Modularidade | Organização do código que separe as operações sobre tarefas da exposição HTTP, facilitando evolução posterior. |
| RNF-05 | Dados temporários | Tarefas persistidas em PostgreSQL no volume nomeado `postgres_data`, mantendo-se após reinício/recriação da aplicação; inicialização de esquema sem apagar dados. |
| RNF-06 | Clareza pedagógica | Código e testes documentados; cada teste identifica o objetivo e os requisitos verificados. |

## Percurso mínimo de aceitação
1. Iniciar o serviço Docker e abrir `http://localhost:8080`.
2. Consultar a lista de tarefas.
3. Criar uma tarefa com título e sem descrição; confirmar que aparece como **Aberta**.
4. Concluir a tarefa; confirmar o estado **Concluída**.
5. Reabrir a tarefa; confirmar o estado **Aberta**.
6. Consultar `GET /health` e confirmar HTTP 200.
7. Reiniciar a aplicação e confirmar que as tarefas continuam disponíveis no PostgreSQL.

## Evolução V2 aprovada
A V2 substitui o armazenamento temporário por PostgreSQL. RF-01 a RF-06 e US-01 a US-06 mantêm os mesmos comportamentos e critérios funcionais; RNF-02 e RNF-05 foram atualizados. A V1 usava armazenamento em memória e um único serviço. A migração é de arquitetura, não acrescenta novas operações de utilizador.

## Fora do MVP
- Login, gestão de utilizadores e permissões.
- Notificações e serviços cloud pagos.
- Filas, CI/CD e observabilidade avançada.

Estas exclusões não impedem a discussão de evoluções futuras; não devem ser implementadas nesta fase.
