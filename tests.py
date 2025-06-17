import pytest
import requests

#CRUD
BASE_URL = 'http://127.0.0.1:5000'
tasks = []

#test para a rota de criar uma nova tarefa
def test_create_task():
  #criamos um dicionario simulando os dados enviados pelo cliente
  new_task_data = {
    'title': 'Nova tarefa',
    'description': 'Descricao da nova tarefa'
  }

  #usamos a biblioteca requests para enviar esses dados e salvamos a resposta em uma variavel
  response = requests.post(f'{BASE_URL}/tasks', json=new_task_data)

  #usamos o assert da biblioteca pytest para verificas se o status do retorno foi sucesso e se os dois itens que estabelecemos como retorno da request estao presentes
  assert response.status_code == 200
  response_json = response.json()
  assert 'message' in response_json
  assert 'id' in response_json
  tasks.append(response_json['id'])

#test para a rota de retornar todas as tasks
def test_get_tasks():
  response = requests.get(f'{BASE_URL}/tasks')
  assert response.status_code == 200
  response_json = response.json()
  assert 'tasks' in response_json
  assert 'total_tasks' in response_json

def test_get_task():
  if tasks:
    #testando o sucesso da rota
    task_id = tasks[0]
    response = requests.get(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 200
    response_json = response.json()
    assert task_id == response_json['id']

    #testando a falha da rota
    task_id = 100
    response = requests.get(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 404
    response_json = response.json()
    assert 'message' in response_json

def test_update_task():
  if tasks:
    task_id = tasks[0]
    payload = {
      'completed': True,
      'description': 'teste de atualizacao da tarefa',
      'title': 'tarefa atualizada'
    }
    #nessa parte verifico se a resposta da requisicao esta como deveria ser
    response = requests.put(f'{BASE_URL}/tasks/{task_id}', json=payload)
    assert response.status_code == 200
    response_json = response.json()
    assert 'message' in response_json

    #fazemos uma nova requisicao do metodo get para verificar se a task foi atualizada conforme o payload enviado
    response = requests.get(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['completed'] == payload['completed']
    assert response_json['description'] == payload['description']
    assert response_json['title'] == payload['title']

    #testando a mensagem de falha
    task_id = 100
    response = requests.put(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 404
    response_json = response.json()
    assert 'message' in response_json

def test_delete_task():
  if tasks:
    task_id = tasks[0]
    #primeiro verifico o retorno esperado do metodo delete
    response = requests.delete(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 200
    response_json = response.json()
    assert 'message' in response_json

    #faço uma nova requisicao com o metodo get para verificar se a task foi deletada (retorno 404)
    response = requests.get(f'{BASE_URL}/tasks/{task_id}')
    assert response.status_code == 404
    response_json = response.json()
    assert 'message' in response_json