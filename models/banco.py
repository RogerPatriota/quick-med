from ..extensions import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150))
    email = db.Column(db.String(50))
    senha = db.Column(db.String(40))
    consultas = db.relationship('Consulta', backref='usuario')

    def __repr__(self) -> str:
        return "<Usuario(nome={}, email={}, senha ={})>".format(self.nome, self.email, self.senha)
#consultas_lucas = Consulta.query.filter_by(idUser = lucas.id).all()

class Hospital(db.Model):
    __tablename__ = "hospitais"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150))
    email = db.Column(db.String(50))
    endereco = db.Column(db.String(50))
    especialidade = db.Column(db.String(50))
    senha = db.Column(db.String(40))
    consutas = db.relationship('Consulta', backref='hospital')

    def __repr__(self) -> str:
        return "<Hospital(nome={}, email={}, endereco={}, especialidade={}, senha={})>".format(self.nome, self.email, self.endereco, self.especialidade, self.senha)

class Consulta(db.Model):
    __tablename__ = 'consultas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idUser = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    idHospitail = db.Column(db.Integer, db.ForeignKey('hospitais.id'))

    def __repr__(self) -> str:
        return "<Consultas()>"