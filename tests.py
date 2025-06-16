import pytest
import requests

#CRUD
BASE_URL = 'http://127.0.0.1:5000'
tasks = []

#test para a rota de criar uma nova tarefa
def test_create_task():
  #criamos um dicionario simulando os dados enviados pelo cliente
  new_task_data = {
    'title': 'Nova taefa',
    'description': 'Descricao da nova tarefa'
  }

  #usamos a biblioteca requests para enviar esses dados e salvamos a resposta em uma variavel
  response = requests.post(f'{BASE_URL}/tasks', json=new_task_data)

  #usamos o assert da biblioteca pytest para verificas se o status do retorno foi sucesso
  assert response.status_code == 200
  response_json = response.json()
  assert 'message' in response_json
  assert 'id' in response_json
  tasks.append(response_json['id'])