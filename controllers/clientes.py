from flask import abort, flash, redirect, render_template, request, url_for
from app import app, db
from models.cliente import Cliente
from flask_login import login_required

#Rotas API

@app.route('/clientes', methods=['POST', 'GET'])
def handle_clientes():
  if request.method == 'POST':
    if request.is_json:
      data = request.get_json()
      novo_cliente = Cliente(nome=data['nome'], cpf_cnpj=data['cpf_cnpj'], tipo_pessoa=data['tipo_pessoa'], endereco=data['endereco'], cidade=data['cidade'], estado=data['estado'], cep=data['cep'], telefone=data['telefone'], email=data['email'])
      db.session.add(novo_cliente)
      db.session.commit()
      return {'Mensagem': f"Cliente {novo_cliente.nome} foi criado com sucesso."}
    else:
      return {"Erro": "A requesição não foi carregada no formato JSON."}
  
  elif request.method == 'GET':
    clientes = Cliente.query.all()
    results = [
      {
        'nome': cliente.nome,
        'cpf_cnpj': cliente.cpf_cnpj,
        'tipo_pessoa': cliente.tipo_pessoa,
        'endereco': cliente.endereco,
        'cidade': cliente.cidade,
        'estado': cliente.estado,
        'cep': cliente.cep,
        'telefone': cliente.telefone,
        'email': cliente.email,
        'id': cliente.id
      } for cliente in clientes
    ]

    return {"Total de Cliente": len(results), "clientes": results}

@app.route('/clientes/<cliente_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_cliente(cliente_id):
  cliente = Cliente.query.get_or_404(cliente_id)
  if request.method == 'GET':
    response = {
        'nome': cliente.nome,
        'cpf_cnpj': cliente.cpf_cnpj,
        'tipo_pessoa': cliente.tipo_pessoa,
        'endereco': cliente.endereco,
        'cidade': cliente.cidade,
        'estado': cliente.estado,
        'cep': cliente.cep,
        'telefone': cliente.telefone,
        'email': cliente.email,
        'id': cliente.id
    }
    return {"Mensagem": "Sucesso", "cliente": response}
  
  elif request.method == 'PUT':
    data = request.get_json()
    cliente.nome = data['nome']
    cliente.cpf_cnpj = data['cpf_cnpj']
    cliente.tipo_pessoa = data['tipo_pessoa']
    cliente.endereco = data['endereco']
    cliente.cidade=data['cidade']
    cliente.estado=data['estado']
    cliente.cep=data['cep']
    cliente.telefone=data['telefone']
    cliente.email=data['email']
    db.session.add(cliente)
    db.session.commit()
    return {"Mensagem": f"Cliente {cliente.nome} atualizado com sucesso!"}
  
  elif request.method == 'DELETE':
    db.session.delete(cliente)
    db.session.commit()
    return {"Mensagem": f"Cliente {cliente.nome} deletado com sucesso!"}

# Páginas WEB

@app.route('/cliente_menu', methods=['POST', 'GET'])
@login_required
def cliente_menu():
  return render_template('cliente/cliente_menu.html', clientes = Cliente.query.all())

@app.route('/cliente_cadastro', methods = ['GET', 'POST'])
@login_required
def cliente_cadastro():
  if request.method == 'POST':
    if not request.form['nome'] or not request.form['cpf_cnpj'] or not request.form['tipo_pessoa'] or not request.form['endereco'] or not request.form['cidade'] or not request.form['estado'] or not request.form['cep']or not request.form['telefone'] or not request.form['email']:
      flash('Por favor, insira todos os campos', 'error')
    else:
      cliente = Cliente(request.form['nome'], request.form['cpf_cnpj'],request.form['tipo_pessoa'], request.form['endereco'], request.form['cidade'],request.form['estado'], request.form['cep'], request.form['telefone'], request.form['email'])
      db.session.add(cliente)
      db.session.commit()
      return redirect(url_for('cliente_menu'))
  return render_template('cliente/cliente_cadastro.html')

@app.route('/cliente_alterar/<cliente_id>', methods=['GET', 'POST'])
@login_required
def cliente_alterar(cliente_id):
  cliente = Cliente.query.get_or_404(cliente_id)
  if request.method == 'POST':    
      cliente.nome = request.form['nome']
      cliente.cpf_cnpj = request.form['cpf_cnpj']
      cliente.tipo_pessoa = request.form['tipo_pessoa']
      cliente.endereco = request.form['endereco']
      cliente.cidade = request.form['cidade']
      cliente.estado = request.form['estado']
      cliente.cep = request.form['cep']
      cliente.telefone=request.form['telefone']
      cliente.email=request.form['email']
      db.session.add(cliente)
      db.session.commit()
      return redirect(url_for('cliente_menu'))
  return render_template('cliente/cliente_alterar.html', cliente = cliente)

@app.route('/cliente_visualizar/<cliente_id>', methods=['GET'])
@login_required
def cliente_visualizar(cliente_id):
  cliente = Cliente.query.get_or_404(cliente_id)          
  return render_template('cliente/cliente_visualizar.html', cliente = cliente)

@app.route('/cliente_menu/<cliente_id>/delete', methods=['GET','POST'])
@login_required
def cliente_delete(cliente_id):
  cliente = Cliente.query.get_or_404(cliente_id)
  if request.method == 'POST':
    if cliente:
      db.session.delete(cliente)
      db.session.commit()
      return redirect('/cliente_menu')
    abort(404)
  return render_template('delete.html', link_cancelar='cliente_menu')
