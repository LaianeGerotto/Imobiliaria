from app import db
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(100), unique=True)
    senha = db.Column(db.String(100))
    nome = db.Column(db.String(1000))
