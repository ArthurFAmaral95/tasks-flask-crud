from flask import Flask

#iniciando a aplicacao
#quando estamos iniciando uma aplicacao a partir de um framework de terceiros usamos o parametro __name__
#quando iniciamos de forma manual usamos o __main__
app = Flask(__name__)

#criando rotas de comunicacao com os usuarios
#rota padrao --> "/" --> toda vez que um usuario acessar o app sera via essa rota
@app.route('/')
def hello_world():
  return 'Hello, world!'

#rota sobre (about)
@app.route('/sobre')
def about():
  return 'Página sobre.'


#executando o app
#o metodo debug é para verificarmos informacoes do servidor
#ao fazer o if garantimos que o servidor só vai rodar quando fizermos isso (rodar o servidor) de forma manual --> recomendado rodar dessa forma durante o desenvolvimento, servidor local
if __name__ == '__main__':
  app.run(debug=True)
