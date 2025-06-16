from flask import Flask, request, jsonify
from models.task import Task

#iniciando a aplicacao
#quando estamos iniciando uma aplicacao a partir de um framework de terceiros usamos o parametro __name__
#quando iniciamos de forma manual usamos o __main__
app = Flask(__name__)

#CRUD --> Create, Read, Update and Delete
tasks = []
task_id_control = 1

#criando as rotas
#rota create --> criando um nova tarefa
@app.route('/tasks', methods=['POST'])
def create_task():
  global task_id_control #preciso pra funcao ter acesso a essa variavel global
  data = request.get_json()
  #algumas maneiras de acessar o conteudo enviado para o servidor --> com as chaves, mesma forma que acessamos atibutos de dicionairos, ou com o metodo get, que podemos definir um valor padrao caso o cliente nao envie nenhuma informacao
  new_task = Task(id=task_id_control, title=data['title'], description=data.get('description',''))
  task_id_control += 1
  tasks.append(new_task)
  return jsonify({'message': 'Nova tarefa criada com sucesso', 'id': new_task.id})

#rota read --> retornando todas as tarefas
@app.route('/tasks', methods=['GET'])
def get_tasks():
  #usamos list comprehension e o metodo to_dict da classe Task para transformar os itens da lista tasks no formato de objeto que precisamos
  task_list = [task.to_dict() for task in tasks]

  output = {
    'tasks': task_list,
    'total_tasks': len(task_list)
  }
  return jsonify(output)

#rota read --> retorna uma task especifica
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
  for t in tasks:
    if t.id == id:
      return jsonify(t.to_dict())
    
  return jsonify({'message':'Não foi possível encontrar a atividade'}), 404

#rota update --> atualizando uma tarefa
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
  task = None #criado para retornar em caso de nao encontramos a da task do id informado
  for t in tasks:
    if t.id == id:
      task = t
      break #faz com que o loop pare depois que já encontramos a task desejada

  if task == None:
    return jsonify({'message': 'Não foi possivel encontrar a atividade'}), 404
  
  data = request.get_json()
  task.title = data['title']
  task.description = data['description']
  task.completed = data['completed']
  return jsonify({'message':'Tarefa atualizada com sucesso'})

#rota delete --> deletando uma task da lista
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
  task = None
  for t in tasks:
    if t.id == id:
      task = t
      break
  
  if not task:
    return jsonify({'message': 'Não foi possível encontrar a atividade'}), 404
  
  tasks.remove(task)
  return jsonify({'message':'Tarefa deletada com sucesso'})

#executando o app
#o metodo debug é para verificarmos informacoes do servidor
#ao fazer o if garantimos que o servidor só vai rodar quando fizermos isso (rodar o servidor) de forma manual --> recomendado rodar dessa forma durante o desenvolvimento, servidor local
if __name__ == '__main__':
  app.run(debug=True)
