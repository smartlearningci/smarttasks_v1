def test_health_and_empty_list(client):
    assert client.get('/health').json()=={'status':'ok'}
    assert client.get('/api/tasks').json()==[]

def test_create_and_list(client):
    result=client.post('/api/tasks',json={'titulo':'Preparar reunião'})
    assert result.status_code==201
    assert result.json()['estado']=='Pendente'
    assert result.json()['descricao']==''
    assert client.get('/api/tasks').json()==[result.json()]

def test_validation(client):
    for title in ('','   '):
        assert client.post('/api/tasks',json={'titulo':title}).status_code==422
    assert client.post('/api/tasks',json={'descricao':'sem título'}).status_code==422
    assert client.get('/api/tasks').json()==[]

def test_complete_reopen_and_errors(client):
    task_id=client.post('/api/tasks',json={'titulo':'Teste'}).json()['id']
    complete=f'/api/tasks/{task_id}/complete'
    reopen=f'/api/tasks/{task_id}/reopen'
    assert client.post(complete).json()['estado']=='Concluída'
    assert client.post(complete).status_code==409
    assert client.post(reopen).json()['estado']=='Pendente'
    assert client.post(reopen).status_code==409
    assert client.post('/api/tasks/999/complete').status_code==404
    assert client.post('/api/tasks/999/reopen').status_code==404

def test_html(client):
    response=client.get('/')
    assert response.status_code==200
    for content in ('SmartTasks','Criar tarefa','Não existem tarefas','Concluir','Reabrir'):
        assert content in response.text
