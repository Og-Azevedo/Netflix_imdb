from sql_alchemy import banco


class FilmeModel(banco.Model):
    #Cria uma tabela no banco com as colunas abaixo
    __tablename__ = 'filmes'

    filme_id = banco.Column(banco.Integer, primary_key=True)
    nome = banco.Column(banco.String(80))
    genero = banco.Column(banco.Integer)
    imdb = banco.Column(banco.Float(precision=1))

    def __init__(self, filme_id, nome, genero, imdb):
        self.filme_id = filme_id
        self.nome = nome
        self.genero = genero
        self.imdb = imdb

    def json(self):
        return {
            'filme_id' : self.filme_id,
            'nome' : self.nome,
            'genero' : self.genero,
            'imdb' : self.imdb

        }

    @classmethod
    def find_filme(cls, filme_id):
        filme = cls.query.filter_by(filme_id=filme_id).first() #SELECT * FROM filmes WHERE filme_id = filme_id
        if filme:
            return filme
        return None

    def save_filme(self):
        try:
            banco.session.add(self)
            banco.session.commit()
        except:
            return {'message':'Ocorreu um erro no servidor' }, 500

    def update_filme(self, nome, genero, imdb):
        self.nome = nome
        self.genero = genero
        self.imdb = imdb

    def delete_filme(self):
        try:
            banco.session.delete(self)
            banco.session.commit()
        except:
            return {'message':'Ocorreu um erro no servidor' }, 500