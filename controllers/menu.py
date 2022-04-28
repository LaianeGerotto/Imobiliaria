from flask import render_template
from flask_login import login_required
from app import app

# Página Web

@app.route('/menuNavegacao', methods=['POST', 'GET'])
@login_required
def menuNavegacao():
  return render_template('menuNavegacao.html')
