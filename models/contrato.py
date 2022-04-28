from app import db

class Contrato(db.Model):
  __tablename__ = 'contratos'

  id = db.Column(db.Integer, primary_key=True)
  inicio_contrato = db.Column(db.Date, nullable=False)
  termino_contrato = db.Column(db.Date, nullable=False)
  valor = db.Column(db.String())
  id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=True) 
  id_corretor = db.Column(db.Integer, db.ForeignKey('corretores.id'), nullable=True)
  id_imovel = db.Column(db.Integer, db.ForeignKey('imoveis.id'), nullable=True)

  def __init__(self, inicio_contrato, termino_contrato, valor, id_cliente, id_corretor, id_imovel):
    self.inicio_contrato = inicio_contrato
    self.termino_contrato = termino_contrato
    self.valor = valor
    self.id_cliente = id_cliente
    self.id_corretor = id_corretor
    self.id_imovel = id_imovel
  
  def __repr__(self):
    return f"<Campo Contrato\n.....>"
 