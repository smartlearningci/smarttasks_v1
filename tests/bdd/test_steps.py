from pathlib import Path
import pytest
from pytest_bdd import given, scenarios, then, when

scenarios('features/ana.feature', 'features/miguel.feature', 'features/sofia.feature')

@pytest.fixture
def context():
    return {}

@given('que a lista está vazia')
def empty(client):
    assert client.get('/api/tasks').json() == []

@given('que existe uma tarefa Pendente')
def pending(client, context):
    context['id'] = client.post('/api/tasks', json={'titulo':'Teste'}).json()['id']

@given('que existe uma tarefa Concluída')
def completed(client, context):
    pending(client, context)
    client.post(f"/api/tasks/{context['id']}/complete")

@given('que existem duas tarefas')
def two_tasks(client):
    for title in ('A', 'B'):
        client.post('/api/tasks', json={'titulo':title})

@given('que existem tarefas em dois estados')
def two_states(client):
    two_tasks(client)
    client.post('/api/tasks/1/complete')

@given('que existe uma tarefa com descrição')
def with_description(client):
    client.post('/api/tasks', json={'titulo':'Reunião', 'descricao':'Preparar agenda'})

@given('que a aplicação está disponível')
def available(client):
    assert client.get('/health').status_code == 200

@given('que o projeto está disponível')
def project():
    assert Path('app/main.py').exists()

@when('consulto a lista de tarefas')
def list_tasks(client, context):
    context['response'] = client.get('/api/tasks')

@when('crio uma tarefa com título válido')
def create_valid(client, context):
    context['response'] = client.post('/api/tasks', json={'titulo':'Preparar reunião'})
    context['id'] = context['response'].json()['id']

@when('crio uma tarefa com título vazio')
def create_invalid(client, context):
    context['response'] = client.post('/api/tasks', json={'titulo':'  '})

@when('concluo a tarefa')
def complete(client, context):
    context['response'] = client.post(f"/api/tasks/{context['id']}/complete")

@when('reabro a tarefa')
def reopen(client, context):
    context['response'] = client.post(f"/api/tasks/{context['id']}/reopen")

@when('consulto o health check')
def health(client, context):
    context['response'] = client.get('/health')

@when('verifico os módulos')
def modules(context):
    context['modules'] = [Path('app/main.py').exists(), Path('app/store.py').exists()]

@then('recebo uma lista vazia')
def is_empty(context):
    assert context['response'].json() == []

@then('a tarefa fica Pendente')
def is_pending(client, context):
    assert client.get('/api/tasks').json()[0]['estado'] == 'Pendente'

@then('a tarefa fica Concluída')
def is_completed(client, context):
    assert client.get('/api/tasks').json()[0]['estado'] == 'Concluída'

@then('recebo erro de validação')
def validation(context):
    assert context['response'].status_code == 422

@then('vejo duas tarefas')
def see_two(context):
    assert len(context['response'].json()) == 2

@then('vejo Pendente e Concluída')
def see_states(context):
    assert {task['estado'] for task in context['response'].json()} == {'Pendente', 'Concluída'}

@then('vejo o título e a descrição')
def see_description(context):
    task = context['response'].json()[0]
    assert (task['titulo'], task['descricao']) == ('Reunião', 'Preparar agenda')

@then('recebo HTTP 200')
def health_ok(context):
    assert context['response'].status_code == 200

@then('a API e o armazenamento estão separados')
def modular(context):
    assert all(context['modules'])

@given('que Docker está disponível')
def docker_available():
    import shutil
    if shutil.which('docker') is None:
        pytest.skip('Docker indisponível neste ambiente')

@when('verifico a configuração Docker')
def docker_config(context):
    import subprocess
    result = subprocess.run(['docker', 'compose', 'config'], capture_output=True, text=True, timeout=30)
    context['docker_config'] = result

@then('existe um serviço com porta local correta')
def docker_valid(context):
    assert context['docker_config'].returncode == 0
    assert '127.0.0.1' in context['docker_config'].stdout
    assert '8080' in context['docker_config'].stdout

@given('que os relatórios de testes foram gerados')
def reports_generated():
    if not Path('reports/unit/results.xml').exists() or not Path('reports/integration/results.xml').exists():
        pytest.skip('Relatórios de suites independentes ainda não gerados')

@when('verifico os relatórios')
def check_reports(context):
    context['reports'] = [Path('reports/unit/results.xml'), Path('reports/unit/results.html'), Path('reports/integration/results.xml'), Path('reports/integration/results.html')]

@then('existem relatórios XML e HTML')
def reports_exist(context):
    assert all(path.is_file() for path in context['reports'])
