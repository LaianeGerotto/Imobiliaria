from flask import abort, flash, redirect, render_template, request, url_for
from app import app, db
from models.contrato import Contrato
from models.imovel import Imovel
from models.cliente import Cliente
from models.corretor import Corretor
from flask_login import login_required

# Rotas API

@app.route('/contratos', methods=['POST', 'GET'])
def handle_contratos():
  if request.method == 'POST':
    if request.is_json:
      data = request.get_json()
      novo_contrato = Contrato(inicio_contrato=data['inicio_contrato'], termino_contrato=data['termino_contrato'], valor=data['valor'], id_cliente=data['id_cliente'], id_corretor=data['id_corretor'], id_imovel=data['id_imovel'])
      db.session.add(novo_contrato)
      db.session.commit()
      return {'Mensagem': f"Contrato {novo_contrato.id} foi criado com sucesso."}
    else:
      return {"Erro": "A requesição não foi carregada no formato JSON."}
  
  elif request.method == 'GET':
    contratos = Contrato.query.all()
    results = [
      {          
        'inicio_contrato': contrato.inicio_contrato,
        'termino_contrato': contrato.termino_contrato,
        'valor': contrato.valor,
        'cliente': {
          'nome': contrato.cliente.nome
        },
        'corretor':{
          'nome': contrato.corretor.nome
        },
        'imovel':{
          'id': contrato.imovel.id,
          'proprietario': contrato.imovel.id_proprietario,
          'descricao': contrato.imovel.descricao_imovel
        },
        'id': contrato.id,
      } for contrato in contratos
    ]

    return {"Total de Contratos": len(results), "Contratos": results}

@app.route('/contratos/<contrato_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_contrato(contrato_id):
  contrato = Contrato.query.get_or_404(contrato_id)
  if request.method == 'GET':
    response = {         
        'inicio_contrato': contrato.inicio_contrato,
        'termino_contrato': contrato.termino_contrato,
        'valor': contrato.valor,
        'cliente': {
          'nome': contrato.cliente.nome
        },
        'corretor':{
          'nome': contrato.corretor.nome
        },
        'imovel':{
          'id': contrato.imovel.id,
          'proprietario': contrato.imovel.id_proprietario,
          'descricao': contrato.imovel.descricao_imovel
        }
    }
    return {"Mensagem": "Sucesso", "Contratos": response}
  
  elif request.method == 'PUT':
    data = request.get_json()      
    contrato.inicio_contrato = data['inicio_contrato']
    contrato.cidade=data['termino_contrato']
    contrato.valor=data['valor']
    contrato.id_cliente=data['id_cliente']
    contrato.id_corretor=data['id_corretor']
    contrato.id_imovel=data['id_imovel']
    db.session.add(contrato)
    db.session.commit()
    return {"Mensagem": f"Contrato {contrato.id} atualizado com sucesso!"}
  
  elif request.method == 'DELETE':
    db.session.delete(contrato)
    db.session.commit()
    return {"Mensagem": f"Contrato {contrato.id} deletado com sucesso!"}

# Páginas Web

@app.route('/contrato_menu', methods=['POST', 'GET'])
@login_required
def contrato_menu():
  return render_template('contrato/contrato_menu.html', contratos = Contrato.query.all())

@app.route('/contrato_cadastro', methods = ['GET', 'POST'])
@login_required
def contrato_cadastro():
  if request.method == 'POST':
    if not request.form['inicio_contrato'] or not request.form['termino_contrato'] or not request.form['valor'] or not request.form['id_cliente'] or not request.form['id_corretor'] or not request.form['id_imovel']:
      flash('Por favor, insira todos os campos', 'error')
    else:
      contrato = Contrato(
        inicio_contrato=request.form['inicio_contrato'],
        termino_contrato=request.form['termino_contrato'],
        valor=request.form['valor'],
        id_cliente=request.form['id_cliente'],
        id_corretor=request.form['id_corretor'],
        id_imovel=request.form['id_imovel']
      )
      db.session.add(contrato)
      db.session.commit()
      return redirect(url_for('contrato_menu'))
  imoveis = Imovel.query.all()
  clientes = Cliente.query.all()
  corretores = Corretor.query.all()
  return render_template(
    'contrato/contrato_cadastro.html', 
    imoveis=imoveis, 
    clientes=clientes,
    corretores=corretores
  )

@app.route('/contrato_alterar/<contrato_id>', methods=['GET', 'POST'])
@login_required
def contrato_alterar(contrato_id):
  contrato = Contrato.query.get_or_404(contrato_id)
  if request.method == 'POST':    
      contrato.inicio_contrato = request.form['inicio_contrato']
      contrato.termino_contrato = request.form['termino_contrato']
      contrato.valor = request.form['valor']
      contrato.id_cliente=request.form['id_cliente']
      contrato.id_corretor=request.form['id_corretor']
      contrato.id_imovel=request.form['id_imovel']
      db.session.add(contrato)
      db.session.commit()
      return redirect(url_for('contrato_menu'))
  imoveis = Imovel.query.all()
  clientes = Cliente.query.all()
  corretores = Corretor.query.all()
  
  return render_template(
    'contrato/contrato_alterar.html', 
    imoveis=imoveis, 
    clientes=clientes,
    corretores=corretores,
    contrato=contrato
  )

@app.route('/contrato_visualizar/<contrato_id>', methods=['GET'])
@login_required
def contrato_visualizar(contrato_id):
  contrato = Contrato.query.get_or_404(contrato_id)          
  return render_template('contrato/contrato_visualizar.html', contrato = contrato)


@app.route('/contrato_menu/<contrato_id>/delete', methods=['GET','POST'])
@login_required
def contrato_delete(contrato_id):
  contrato = Contrato.query.get_or_404(contrato_id)
  if request.method == 'POST':
    if contrato:
      db.session.delete(contrato)
      db.session.commit()
      return redirect('/contrato_menu')
    abort(404)
  return render_template('/static/form.js', link_cancelar='contrato_menu')
