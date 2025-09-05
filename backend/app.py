import os
from flask import Flask, json, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from itsdangerous import URLSafeTimedSerializer
import sqlite3
from pathlib import Path
from dotenv import load_dotenv
from .common import close_db, get_db, mail, config

# Importe os Blueprints
from .api.auth import auth_bp
from .api.google import google_bp, init_oauth
from .api.summary import summary_bp

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

def create_app():
    """Cria e configura a aplicação Flask."""
    app = Flask(__name__)
    init_oauth(app)

    # --- Configurações da Aplicação ---
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

    # Adicione a chave secreta para o URLSafeTimedSerializer
    app.secret_key = os.getenv('SECRET_KEY')

    # --- Inicializa as extensões do Flask ---
    CORS(app)
    JWTManager(app)
    Limiter(get_remote_address, app=app, default_limits=["10/minute"])
    
    # Inicializa o Flask-Mail e o serializador com o aplicativo
    mail.init_app(app)
    app.config['SERIALIZER'] = URLSafeTimedSerializer(app.secret_key)


    # --- Registro de Blueprints ---
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(google_bp, url_prefix='/api')
    app.register_blueprint(summary_bp, url_prefix='/api')

    # --- Rotas da API (se houverem) ---
    @app.route('/api/config')
    def get_config():
        """Retorna as configurações da aplicação."""
        return jsonify(config)

    # Adicione o teardown para fechar o banco de dados
    app.teardown_appcontext(close_db)

    return app

def init_db(app):
    """Inicializa o banco de dados, criando as tabelas se não existirem."""
    with app.app_context():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        try:
            cursor.execute("SELECT is_verified FROM users")
        except sqlite3.OperationalError:
            cursor.execute("ALTER TABLE users ADD COLUMN is_verified BOOLEAN NOT NULL DEFAULT 0")

        conn.commit()
    # A conexão é fechada automaticamente pelo teardown do app_context

if __name__ == "__main__":
    app = create_app()
    init_db(app) # Inicializa o banco de dados
    app.run(host="0.0.0.0", port=8080)