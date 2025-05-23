from flask import Flask, request, jsonify
from models import Cliente
from database import db
import os

app = Flask(__name__)

# Configuração do banco de dados usando variáveis de ambiente
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('POSTGRES_DB')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/clientes', methods=['POST'])
def criar_cliente():
    data = request.json
    cliente = Cliente(nome=data['nome'], email=data['email'])
    db.session.add(cliente)
    db.session.commit()
    return jsonify(cliente.to_dict()), 201

@app.route('/clientes', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    return jsonify([c.to_dict() for c in clientes])

@app.route('/clientes/<int:id>', methods=['GET'])
def obter_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    return jsonify(cliente.to_dict())

@app.route('/clientes/<int:id>', methods=['PUT'])
def atualizar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    data = request.json
    cliente.nome = data.get('nome', cliente.nome)
    cliente.email = data.get('email', cliente.email)
    db.session.commit()
    return jsonify(cliente.to_dict())

@app.route('/clientes/<int:id>', methods=['DELETE'])
def deletar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({"message": "Cliente deletado com sucesso"})

import time
import psycopg2
from sqlalchemy.exc import OperationalError # type: ignore

# Retry para garantir que o banco esteja pronto
with app.app_context():
    connected = False
    attempts = 0
    while not connected and attempts < 10:
        try:
            db.create_all()
            print("✅ Conectado ao banco e tabelas criadas.")
            connected = True
        except OperationalError as e:
            attempts += 1
            print(f"⏳ Tentativa {attempts}: Banco ainda não está pronto...")
            time.sleep(2)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
