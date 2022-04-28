from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from models.usuario import Usuario
from app import app, db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(usuario_id):
  return Usuario.query.get(int(usuario_id))

#Rotas de Login
@app.route('/')
def default_route():
    return redirect(url_for("login"))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    senha = request.form.get('senha')
    lembrar = True if request.form.get('lembrar') else False

    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario or not check_password_hash(usuario.senha, senha):
        flash('Senha ou email incorretos!')
        return redirect(url_for('login'))
    login_user(usuario, remember=lembrar) 
    return redirect(url_for('menuNavegacao'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    nome = request.form.get('nome')
    senha = request.form.get('senha')

    usuario = Usuario.query.filter_by(email=email).first() 

    if usuario:
        flash('Email já cadastrado') 
        return redirect(url_for('signup'))
    novo_usuario = Usuario(email=email, nome=nome, senha=generate_password_hash(senha, method='sha256'))

    
    db.session.add(novo_usuario)
    db.session.commit()

    return redirect(url_for('login'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


