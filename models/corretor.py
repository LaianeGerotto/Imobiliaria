from app import db

class Corretor(db.Model):
  __tablename__ = 'corretores'

  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String())
  cpf_cnpj = db.Column(db.String())
  tipo_pessoa = db.Column(db.String())  
  telefone = db.Column(db.String())
  email = db.Column(db.String())
  contratos = db.relationship('Contrato', backref='corretor', lazy=True)

  def __init__(self, nome, cpf_cnpj, tipo_pessoa,telefone, email):
    self.nome = nome
    self.cpf_cnpj = cpf_cnpj
    self.tipo_pessoa = tipo_pessoa
    self.telefone = telefone
    self.email = email
  
  def __repr__(self):
    return f"Nome: {self.nome}"
