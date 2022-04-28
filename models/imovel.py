from app import db

class Imovel(db.Model):
  __tablename__ = 'imoveis'

  id = db.Column(db.Integer, primary_key=True)
  endereco = db.Column(db.String())
  cidade = db.Column(db.String())
  estado = db.Column(db.String())
  cep = db.Column(db.String())
  tipo_imovel = db.Column(db.String())
  descricao_imovel = db.Column(db.String())
  id_proprietario = db.Column(db.Integer, db.ForeignKey('proprietarios.id'), nullable=False) #Preencher corretamente
  contratos = db.relationship('Contrato', backref='imovel', lazy=True)
 

  def __init__(self, endereco, cidade, estado, cep, tipo_imovel, descricao_imovel, id_proprietario):
    self.endereco = endereco
    self.cidade = cidade
    self.estado = estado
    self.cep = cep
    self.tipo_imovel = tipo_imovel
    self.descricao_imovel = descricao_imovel
    self.id_proprietario = id_proprietario
  
  def __repr__(self):
    return f"Imóvel: {self.id} - Proprietário:{self.proprietario.nome}"
