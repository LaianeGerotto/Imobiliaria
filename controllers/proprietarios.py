from flask import abort, flash, redirect, render_template, request, url_for
from app import app, db
from models.proprietario import Proprietario
from flask_login import login_required

# Rotas API

@app.route('/proprietarios', methods=['POST', 'GET'])
def handle_proprietarios():
  if request.method == 'POST':
    if request.is_json:
      data = request.get_json()
      novo_proprietario = Proprietario(nome=data['nome'], cpf_cnpj=data['cpf_cnpj'], tipo_pessoa=data['tipo_pessoa'], endereco=data['endereco'], cidade=data['cidade'], estado=data['estado'], cep=data['cep'], telefone=data['telefone'], email=data['email'])
      db.session.add(novo_proprietario)
      db.session.commit()
      return {'Mensagem': f"Proprietário {novo_proprietario.nome} foi criado com sucesso."}
    else:
      return {"Erro": "A requesição não foi carregada no formato JSON."}
  
  elif request.method == 'GET':
    proprietarios = Proprietario.query.all()
    results = [
      {
        'nome': proprietario.nome,
        'cpf_cnpj': proprietario.cpf_cnpj,
        'tipo_pessoa': proprietario.tipo_pessoa,
        'endereco': proprietario.endereco,
        'cidade': proprietario.cidade,
        'estado': proprietario.estado,
        'cep': proprietario.cep,
        'telefone': proprietario.telefone,
        'email': proprietario.email,
        'id': proprietario.id,
        'imoveis': [
          {
            'descricao_imovel': imovel.descricao_imovel,
            'id': imovel.id,
          } for imovel in proprietario.imoveis
        ]
      } for proprietario in proprietarios
    ]

    return {"Total de Proprietarios": len(results), "proprietarios": results}

@app.route('/proprietarios/<proprietario_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_proprietario(proprietario_id):
  proprietario = Proprietario.query.get_or_404(proprietario_id)
  if request.method == 'GET':
    response = {
        'nome': proprietario.nome,
        'cpf_cnpj': proprietario.cpf_cnpj,
        'tipo_pessoa': proprietario.tipo_pessoa,
        'endereco': proprietario.endereco,
        'cidade': proprietario.cidade,
        'estado': proprietario.estado,
        'cep': proprietario.cep,
        'telefone': proprietario.telefone,
        'email': proprietario.email,
        'id': proprietario.id
    }
    return {"Mensagem": "Sucesso", "proprietario": response}
  
  elif request.method == 'PUT':
    data = request.get_json()
    proprietario.nome = data['nome']
    proprietario.cpf_cnpj = data['cpf_cnpj']
    proprietario.tipo_pessoa = data['tipo_pessoa']
    proprietario.endereco = data['endereco']
    proprietario.cidade=data['cidade']
    proprietario.estado=data['estado']
    proprietario.cep=data['cep']
    proprietario.telefone=data['telefone']
    proprietario.email=data['email']
    db.session.add(proprietario)
    db.session.commit()
    return {"Mensagem": f"Proprietário {proprietario.nome} atualizado com sucesso!"}
  
  elif request.method == 'DELETE':
    db.session.delete(proprietario)
    db.session.commit()
    return {"Mensagem": f"Proprietário {proprietario.nome} deletado com sucesso!"}

# Páginas Web

@app.route('/proprietario_menu', methods=['POST', 'GET'])
@login_required
def proprietario_menu():
  return render_template('proprietario/proprietario_menu.html', proprietarios = Proprietario.query.all())

@app.route('/proprietario_cadastro', methods = ['GET', 'POST'])
@login_required
def proprietario_cadastro():
  if request.method == 'POST':
    if not request.form['nome'] or not request.form['cpf_cnpj'] or not request.form['tipo_pessoa'] or not request.form['endereco'] or not request.form['cidade'] or not request.form['estado'] or not request.form['cep']or not request.form['telefone'] or not request.form['email']:
      flash('Por favor, insira todos os campos', 'error')
    else:
      proprietario = Proprietario(request.form['nome'], request.form['cpf_cnpj'],request.form['tipo_pessoa'], request.form['endereco'], request.form['cidade'],request.form['estado'], request.form['cep'], request.form['telefone'], request.form['email'])
      db.session.add(proprietario)
      db.session.commit()
      return redirect(url_for('proprietario_menu'))
  return render_template('proprietario/proprietario_cadastro.html')

@app.route('/proprietario_alterar/<proprietario_id>', methods=['GET', 'POST'])
@login_required
def proprietario_alterar(proprietario_id):
  proprietario = Proprietario.query.get_or_404(proprietario_id)
  if request.method == 'POST':    
      proprietario.nome = request.form['nome']
      proprietario.cpf_cnpj = request.form['cpf_cnpj']
      proprietario.tipo_pessoa = request.form['tipo_pessoa']
      proprietario.endereco = request.form['endereco']
      proprietario.cidade = request.form['cidade']
      proprietario.estado = request.form['estado']
      proprietario.cep = request.form['cep']
      proprietario.telefone=request.form['telefone']
      proprietario.email=request.form['email']
      db.session.add(proprietario)
      db.session.commit()
      return redirect(url_for('proprietario_menu'))
  return render_template('proprietario/proprietario_alterar.html', proprietario = proprietario)

@app.route('/proprietario_visualizar/<proprietario_id>', methods=['GET'])
@login_required
def proprietario_visualizar(proprietario_id):
  proprietario = Proprietario.query.get_or_404(proprietario_id)          
  return render_template('proprietario/proprietario_visualizar.html', proprietario = proprietario)


@app.route('/proprietario_menu/<proprietario_id>/delete', methods=['GET','POST'])
@login_required
def proprietario_delete(proprietario_id):
  proprietario = Proprietario.query.get_or_404(proprietario_id)
  if request.method == 'POST':
    if proprietario:
      db.session.delete(proprietario)
      db.session.commit()
      return redirect('/proprietario_menu')
    abort(404)
  return render_template('delete.html', link_cancelar='proprietario_menu')

