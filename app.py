from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:root@localhost:5432/imobiliaria"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.config['SECRET_KEY'] = "random string"

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

from controllers.sessoes import *
from controllers.clientes import *
from controllers.contratos import *
from controllers.corretores import *
from controllers.imoveis import *
from controllers.proprietarios import *
from controllers.menu import *


if __name__ == '__main__':
  app.run(debug=True)


