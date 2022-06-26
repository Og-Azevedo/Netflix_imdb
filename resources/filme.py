from flask_restful import Resource, reqparse
from models.filme import FilmeModel
from flask_jwt_extended import jwt_required

#path / filmes?genero=1234&imdb_min=7.0&imadb_max=8.0
path_params = reqparse.RequestParser()
path_params.add_argument('genero', type=int)
path_params.add_argument('imdb_min', type=float)
path_params.add_argument('imdb_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


class Filmes(Resource):

    def get(self):

        dados = path_params.parse_args()
        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
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

    @jwt_required()
    def post(self, filme_id):

        if FilmeModel.find_filme(filme_id):
            return {"message":f"Esse filme_id '{filme_id}' já existe!"}, 400

        dados = Filme.argumentos.parse_args()
        filme_objeto = FilmeModel(filme_id, **dados)
        filme_objeto.save_filme()
        return filme_objeto.json()

    @jwt_required()
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

    @jwt_required()
    def delete(self, filme_id):
        # global filmes
        # filmes = [filme for filme in filmes if filme['filme_id'] != filme_id]
        # return {'message':'Filme deletado com sucesso'}

        filme_encontrado = FilmeModel.find_filme(filme_id)
        if filme_encontrado:
            filme_encontrado.delete_filme()
            return {'message': 'Filme deletado.'}
        return {'message': 'Filme not found'},404
