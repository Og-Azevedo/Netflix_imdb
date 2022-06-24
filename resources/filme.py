from flask_restful import Resource, reqparse
from models.filme import FilmeModel

filmes = [
    {
        'filme_id': 0,
        'nome':'47 Ronins',
        'genero': 1365,
        'imdb':7.7,
    },
    {
        'filme_id': 1,
        'nome':'14 montanhas',
        'genero': 1365,
        'imdb':5.7,
    },
    {
        'filme_id': 2,
        'nome':'Rambo',
        'genero': 1365,
        'imdb':4.7,
    }
]



class Filmes(Resource):

    def get(self):
        return {'filmes': [filme.json() for filme in FilmeModel.query.all()]}

class Filme(Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank.")
    argumentos.add_argument('genero', type=int,required=True,help="The field 'genero' cannot be left blank.")
    argumentos.add_argument('imdb', type=float,required=True,help="The field 'imdb' cannot be left blank.")


    def get(self, filme_id):
        filme = FilmeModel.find_filme(filme_id)
        if filme:
            return filme.json()
        return {'message':'Filme não encontrado'}, 404 #not_found

    def post(self, filme_id):

        if FilmeModel.find_filme(filme_id):
            return {"message":f"Esse filme_id '{filme_id}' já existe!"}, 400

        dados = Filme.argumentos.parse_args()
        filme_objeto = FilmeModel(filme_id, **dados)
        filme_objeto.save_filme()
        return filme_objeto.json()

    def put(self, filme_id):

        dados = Filme.argumentos.parse_args()



        filme_encontrado = FilmeModel.find_filme(filme_id)
        if filme_encontrado:
            filme_encontrado.update_filme(**dados)
            filme_encontrado.save_filme()
            return filme_encontrado.json(), 200 #sucesso
        else:
            filme_novo = FilmeModel(filme_id, **dados)
            filme_novo.save_filme()
            return filme_novo.json(), 201 #criado

    def delete(self, filme_id):
        # global filmes
        # filmes = [filme for filme in filmes if filme['filme_id'] != filme_id]
        # return {'message':'Filme deletado com sucesso'}

        filme_encontrado = FilmeModel.find_filme(filme_id)
        if filme_encontrado:
            filme_encontrado.delete_filme()
            return {'message': 'Filme deletado.'}
        return {'message': 'Filme not found'},404
