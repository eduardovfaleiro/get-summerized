from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from backend.jwt_utils import generate_token
from backend.common import db_path

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'message': 'E-mail ou senha ausentes'}), 400

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    if cursor.fetchone():
        conn.close()
        return jsonify({'message': 'Usuário já existe'}), 409

    # Criptografa a senha antes de salvar
    hashed_pw = generate_password_hash(password)
    cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_pw))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Usuário criado com sucesso'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'message': 'E-mail ou senha ausentes'}), 400

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE email = ?', (email,))
    result = cursor.fetchone()
    conn.close()
    if result and check_password_hash(result[0], password):
        # Gera token JWT com o username
        access_token = generate_token(email)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Credenciais inválidas'}), 401