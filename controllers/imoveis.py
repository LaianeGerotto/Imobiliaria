from flask import abort, flash, redirect, render_template, request, url_for
from app import app, db
from models.imovel import Imovel
from models.proprietario import Proprietario
from flask_login import login_required

# Rotas API

@app.route('/imoveis', methods=['POST', 'GET'])
def handle_imoveis():
  if request.method == 'POST':
    if request.is_json:
      data = request.get_json()
      novo_imovel = Imovel(endereco=data['endereco'], cidade=data['cidade'], estado=data['estado'], cep=data['cep'], tipo_imovel=data['tipo_imovel'], descricao_imovel=data['descricao_imovel'], id_proprietario=data['id_proprietario'])
      db.session.add(novo_imovel)
      db.session.commit()
      return {'Mensagem': f"Imóvel {novo_imovel.id} foi criado com sucesso."}
    else:
      return {"Erro": "A requesição não foi carregada no formato JSON."}
  
  elif request.method == 'GET':
    imoveis = Imovel.query.all()
    results = [
      {          
        'endereco': imovel.endereco,
        'cidade': imovel.cidade,
        'estado': imovel.estado,
        'cep': imovel.cep,
        'tipo_imovel': imovel.tipo_imovel,
        'descricao_imovel': imovel.descricao_imovel,
        'id': imovel.id,
        'proprietario': {
          'nome': imovel.proprietario.nome,
          'cpf_cnpj': imovel.proprietario.cpf_cnpj,
          'id': imovel.proprietario.id
        }
      } for imovel in imoveis
    ]

    return {"Total de Imóveis": len(results), "Imóveis": results}

@app.route('/imoveis/<imovel_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_imovel(imovel_id):
  imovel = Imovel.query.get_or_404(imovel_id)
  if request.method == 'GET':
    response = {         
        'endereco': imovel.endereco,
        'cidade': imovel.cidade,
        'estado': imovel.estado,
        'cep': imovel.cep,
        'tipo_imovel': imovel.tipo_imovel,
        'descricao_imovel': imovel.descricao_imovel,
        'id': imovel.id,
        'proprietario': {
        'nome': imovel.proprietario.nome,
        'cpf_cnpj': imovel.proprietario.cpf_cnpj,
        'id': imovel.proprietario.id
        }
    }
    return {"Mensagem": "Sucesso", "imóvel": response}
  
  elif request.method == 'PUT':
    data = request.get_json()      
    imovel.endereco = data['endereco']
    imovel.cidade=data['cidade']
    imovel.estado=data['estado']
    imovel.cep=data['cep']
    imovel.tipo_imovel=data['tipo_imovel']
    imovel.descricao_imovel=data['descricao_imovel']
    imovel.id_proprietario=data['id_proprietario']
    db.session.add(imovel)
    db.session.commit()
    return {"Mensagem": f"Imóvel {imovel.id} atualizado com sucesso!"}
  
  elif request.method == 'DELETE':
    db.session.delete(imovel)
    db.session.commit()
    return {"Mensagem": f"Imóvel {imovel.id} deletado com sucesso!"}

# Páginas Web

@app.route('/imovel_menu', methods=['POST', 'GET'])
@login_required
def imovel_menu():
  return render_template('imovel/imovel_menu.html', imoveis = Imovel.query.all())

@app.route('/imovel_cadastro', methods = ['GET', 'POST'])
@login_required
def imovel_cadastro():
  if request.method == 'POST':
    if not request.form['endereco'] or not request.form['cidade'] or not request.form['estado'] or not request.form['cep'] or not request.form['id_proprietario'] or not request.form['tipo_imovel'] or not request.form['descricao_imovel']:
      flash('Por favor, insira todos os campos', 'error')
    else:
      imovel = Imovel(
        endereco=request.form['endereco'],
        cidade=request.form['cidade'],
        estado=request.form['estado'],
        cep=request.form['cep'],
        id_proprietario=request.form['id_proprietario'],
        tipo_imovel=request.form['tipo_imovel'],
        descricao_imovel=request.form['descricao_imovel']
      )
      db.session.add(imovel)
      db.session.commit()
      return redirect(url_for('imovel_menu'))
  proprietarios = Proprietario.query.all()
  return render_template('imovel/imovel_cadastro.html', proprietarios = proprietarios)

@app.route('/imovel_alterar/<imovel_id>', methods=['GET', 'POST'])
@login_required
def imovel_alterar(imovel_id):
  imovel = Imovel.query.get_or_404(imovel_id)
  if request.method == 'POST':    
      imovel.endereco = request.form['endereco']
      imovel.cidade = request.form['cidade']
      imovel.estado = request.form['estado']
      imovel.cep=request.form['cep']
      imovel.tipo_imovel=request.form['tipo_imovel']
      imovel.descricao_imovel=request.form['descricao_imovel']
      imovel.id_proprietario=request.form['id_proprietario']
      db.session.add(imovel)
      db.session.commit()
      return redirect(url_for('imovel_menu'))
  proprietarios = Proprietario.query.all()    
  return render_template('imovel/imovel_alterar.html',
   imovel = imovel,
   proprietarios = proprietarios)

@app.route('/imovel_visualizar/<imovel_id>', methods=['GET'])
@login_required
def imovel_visualizar(imovel_id):
  imovel = Imovel.query.get_or_404(imovel_id)          
  return render_template('imovel/imovel_visualizar.html', imovel = imovel)

@app.route('/imovel_menu/<imovel_id>/delete', methods=['GET','POST'])
@login_required
def imovel_delete(imovel_id):
  imovel = Imovel.query.get_or_404(imovel_id)
  if request.method == 'POST':
    if imovel:
      db.session.delete(imovel)
      db.session.commit()
      return redirect('/imovel_menu')
    abort(404)
  return render_template('delete.html', link_cancelar='imovel_menu')

