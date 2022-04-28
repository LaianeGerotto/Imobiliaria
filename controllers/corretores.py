from flask import abort, flash, redirect, render_template, request, url_for
from app import app, db
from models.corretor import Corretor
from flask_login import login_required

# Rotas API

@app.route('/corretores', methods=['POST', 'GET'])
def handle_corretores():
  if request.method == 'POST':
    if request.is_json:
      data = request.get_json()
      novo_corretor = Corretor(nome=data['nome'], cpf_cnpj=data['cpf_cnpj'], tipo_pessoa=data['tipo_pessoa'], telefone=data['telefone'], email=data['email'])
      db.session.add(novo_corretor)
      db.session.commit()
      return {'Mensagem': f"Corretor {novo_corretor.nome} foi criado com sucesso."}
    else:
      return {"Erro": "A requesição não foi carregada no formato JSON."}
  
  elif request.method == 'GET':
    corretores = Corretor.query.all()
    results = [
      {
        'nome': corretor.nome,
        'cpf_cnpj': corretor.cpf_cnpj,
        'tipo_pessoa': corretor.tipo_pessoa,          
        'telefone': corretor.telefone,
        'email': corretor.email,
        'id': corretor.id
      } for corretor in corretores
    ]

    return {"Total de Corretores": len(results), "corretores": results}

@app.route('/corretores/<corretor_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_corretor(corretor_id):
  corretor = Corretor.query.get_or_404(corretor_id)
  if request.method == 'GET':
    response = {
        'nome': corretor.nome,
        'cpf_cnpj': corretor.cpf_cnpj,
        'tipo_pessoa': corretor.tipo_pessoa,
        'telefone': corretor.telefone,
        'email': corretor.email,
        'id': corretor.id
    }
    return {"Mensagem": "Sucesso", "corretor": response}
  
  elif request.method == 'PUT':
    data = request.get_json()
    corretor.nome = data['nome']
    corretor.cpf_cnpj = data['cpf_cnpj']
    corretor.tipo_pessoa = data['tipo_pessoa']
    corretor.telefone=data['telefone']
    corretor.email=data['email']
    db.session.add(corretor)
    db.session.commit()
    return {"Mensagem": f"Corretor {corretor.nome} atualizado com sucesso!"}
  
  elif request.method == 'DELETE':
    db.session.delete(corretor)
    db.session.commit()
    return {"Mensagem": f"Corretor {corretor.nome} deletado com sucesso!"}

# Páginas Web

@app.route('/corretor_menu', methods=['POST', 'GET'])
@login_required
def corretor_menu():
  corretores = Corretor.query.order_by("id").all()
  return render_template('corretor/corretor_menu.html', corretores = corretores)

@app.route('/corretor_cadastro', methods = ['GET', 'POST'])
@login_required
def corretor_cadastro():
  if request.method == 'POST':
    if not request.form['nome'] or not request.form['cpf_cnpj'] or not request.form['tipo_pessoa'] or not request.form['telefone'] or not request.form['email']:
      flash('Por favor, insira todos os campos', 'error')
    else:
      corretor = Corretor(request.form['nome'], request.form['cpf_cnpj'],request.form['tipo_pessoa'], request.form['telefone'], request.form['email'])
      db.session.add(corretor)
      db.session.commit()
      return redirect(url_for('corretor_menu'))
  return render_template('corretor/corretor_cadastro.html')

@app.route('/corretor_alterar/<corretor_id>', methods=['GET', 'POST'])
@login_required
def corretor_alterar(corretor_id):
  corretor = Corretor.query.get_or_404(corretor_id)
  if request.method == 'POST':    
      corretor.nome = request.form['nome']
      corretor.cpf_cnpj = request.form['cpf_cnpj']
      corretor.tipo_pessoa = request.form['tipo_pessoa']
      corretor.telefone=request.form['telefone']
      corretor.email=request.form['email']
      db.session.add(corretor)
      db.session.commit()
      return redirect(url_for('corretor_menu'))
  return render_template('corretor/corretor_alterar.html', corretor = corretor)

@app.route('/corretor_visualizar/<corretor_id>', methods=['GET'])
@login_required
def corretor_visualizar(corretor_id):
  corretor = Corretor.query.get_or_404(corretor_id)          
  return render_template('corretor/corretor_visualizar.html', corretor = corretor)  

@app.route('/corretor_menu/<corretor_id>/delete', methods=['POST'])
@login_required
def corretor_delete(corretor_id):
  corretor = Corretor.query.get_or_404(corretor_id)
  if request.method == 'POST':
    if corretor:
      db.session.delete(corretor)
      db.session.commit()
      return redirect('/corretor_menu')
    abort(404)
  return render_template('delete.html', link_cancelar='corretor_menu')
