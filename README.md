# SmartTasks — V2 com persistência PostgreSQL

Aplicação pedagógica TaskFlow: criar, listar, concluir e reabrir tarefas. A API e a interface HTML são as mesmas da V1. **Na V2, as tarefas ficam guardadas em PostgreSQL**, no volume Docker `postgres_data`.

## Requisitos
Git, Docker e Docker Compose.

## Clonar e configurar
```bash
git clone https://github.com/smartlearningci/smarttasks.git
cd smarttasks
cp .env.example .env
```
Editar `.env` e substituir `SUBSTITUIR_LOCALMENTE` por uma password forte, local. **Não publicar o ficheiro `.env`**. Se já existir um volume PostgreSQL inicializado, alterar a password no `.env` não altera automaticamente a password do utilizador existente na base.

## Construir e iniciar
```bash
docker compose config --quiet
docker compose up -d --build
docker compose ps
```
Abrir **http://localhost:8080**. O serviço `db` usa PostgreSQL 17 e é aguardado pelo healthcheck antes de iniciar a aplicação. A porta 5432 não é publicada; ambos comunicam pela rede padrão do Compose.

## Verificar aplicação e base de dados
```bash
curl http://localhost:8080/health
curl http://localhost:8080/api/tasks
```
Criar uma tarefa na interface, concluí-la e reabri-la. Consultar a tabela real:
```bash
docker compose exec db psql -U smarttasks -d smarttasks -c "SELECT id, title, description, status FROM tasks ORDER BY id;"
```
Reiniciar apenas a aplicação e verificar que a tarefa continua na interface e na BD:
```bash
docker compose restart smarttasks
```

## Testes automatizados
```bash
docker compose run --rm --no-deps smarttasks python -m pytest -q tests/test_api.py
```
Os testes de contrato HTTP usam um duplo de armazenamento e **não modificam a base de dados real**.

Os testes T-14 a T-20 verificam PostgreSQL numa **base separada** cujo nome termina em `_test`. Não os executar sobre a base `smarttasks`. Para criar uma base de testes local (uma única vez):
```bash
docker compose exec db psql -U smarttasks -d postgres -c "CREATE DATABASE smarttasks_test;"
```
Para executar T-14 a T-20 dentro do container, definir `TEST_DATABASE_URL` apenas no comando de teste, com a password local corretamente codificada para URL. Alternativamente, executar os testes num ambiente Python de desenvolvimento que tenha acesso à base de testes. Sem `TEST_DATABASE_URL`, os testes de integração são assinalados como **skipped**, não como aprovados.

Cada teste identifica US, RF/RNF, objetivo e resultado esperado. Consultar `docs/04_rastreabilidade_e_testes.md`.

## Diagnóstico e recuperação sem perda de dados
1. `docker compose ps`: verificar se `db` está saudável e `smarttasks` em execução.
2. `docker compose logs --tail=80 db` e `docker compose logs --tail=80 smarttasks`: procurar falhas de autenticação, ligação ou esquema.
3. Confirmar que `.env` existe e contém a password definida quando o volume PostgreSQL foi inicializado. Se a password mudou, corrigir a configuração ou alterar a password do utilizador na base de forma controlada.
4. `docker compose up -d --build`: voltar a iniciar sem eliminar volumes.
5. Se houver erro de ligação, verificar `docker compose exec db pg_isready -U smarttasks -d smarttasks`.

**Não utilizar `docker compose down -v` como tentativa de reparação**: esse comando remove o volume e pode destruir dados.

## Parar
```bash
docker compose down
```
O volume `postgres_data` permanece.

## Organização
- `app/main.py`: endpoints HTTP e inicialização de esquema.
- `app/models.py`: modelos e validações existentes.
- `app/store.py`: consultas SQL parametrizadas; `app/db.py`: ligação e esquema.
- `app/static/index.html`: interface HTML preservada.
- `tests/test_api.py`: contrato HTTP; `tests/test_postgres.py`: integração real.
- `docs/`: requisitos, US, arquitetura e rastreabilidade.

**Fora do âmbito:** login, filas, notificações, serviços externos pagos, CI/CD e observabilidade avançada.
