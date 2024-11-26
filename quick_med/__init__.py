from flask import Flask
from .extensions import db, migrate
from .routes.bP import bP
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Diretório base do projeto
INSTANCE_DIR = os.path.join(BASE_DIR, '..', 'instance')  # Caminho para a pasta instance

def create_app():
    app = Flask(__name__)

    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(INSTANCE_DIR, 'db.sqlite3')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(bP)

    

    return app