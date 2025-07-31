from config import db 
from flask_login import UserMixin
#UserMixin guarda todos o metodos e funcionalidade para seja identificada como usuario pelo loginmaneger

class Usuarios(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    cep = db.Column(db.String(9), nullable=False)
    rua = db.Column(db.String(50), nullable= False)
    numero = db.Column(db.String(5), nullable= False)
    complemento = db.Column(db.String(50), nullable = True)
    bairro = db.Column(db.String(50), nullable = False)
    cidade = db.Column(db.String(50), nullable = False)
    estado = db.Column(db.String(2), nullable=False)
    usuario = db.Column(db.String(12), nullable=False)
    senha = db.Column(db.LargeBinary, nullable=False, unique=True)
    
