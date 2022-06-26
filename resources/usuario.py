from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="'Login' field cannot be left blank!")
atributos.add_argument('senha', type=str, required=True, help="'Senha' field cannot be left blank!")

class Usuario(Resource):

    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message':'User não encontrado'}, 404 #not_found

    @jwt_required()
    def delete(self, user_id):
        user_encontrado = UserModel.find_user(user_id)
        if user_encontrado:
            user_encontrado.delete_user()
            return {'message': 'Usuario deletado.'}
        return {'message': 'User not found'},404

class UserRegister(Resource):

    def post(self):

        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {'message':f'The login {dados["login"]} already exists.'}

        usuario = UserModel(**dados)
        usuario.save_user()
        return {'message':'Login criado com sucesso'},201

class UserLogin(Resource):

    @classmethod
    def post(cls):

        dados = atributos.parse_args()
        user = UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.senha)
            return {'acces_token': token_de_acesso}, 200
        return {'message':'The login or password is incorrect.'}, 401

class UserLogout():

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message':'User logedOut!'}