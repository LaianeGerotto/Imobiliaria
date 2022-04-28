from app import db

class Cliente(db.Model):
  __tablename__ = 'clientes'

  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String())
  cpf_cnpj = db.Column(db.String())
  tipo_pessoa = db.Column(db.String())
  endereco = db.Column(db.String())
  cidade = db.Column(db.String())
  estado = db.Column(db.String())
  cep = db.Column(db.String())
  telefone = db.Column(db.String())
  email = db.Column(db.String())
  contratos = db.relationship('Contrato', backref='cliente', lazy=True)

  def __init__(self, nome, cpf_cnpj, tipo_pessoa, endereco, cidade, estado, cep, telefone, email):
    self.nome = nome
    self.cpf_cnpj = cpf_cnpj
    self.tipo_pessoa = tipo_pessoa
    self.endereco = endereco
    self.cidade = cidade
    self.estado = estado
    self.cep = cep
    self.telefone = telefone
    self.email = email
  
  def __repr__(self):
    return f"{self.nome}"  
 