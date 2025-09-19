import os
from flask import Blueprint, current_app, jsonify, request, url_for
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from ..jwt_utils import generate_token
from ..utils.validate_email import validate_email
from ..common import get_db, mail

auth_bp = Blueprint('auth_bp', __name__)

def generate_verification_token(email):
    return current_app.config['SERIALIZER'].dumps(email, salt='email-verification-salt')

def send_verification_email(email, token):
    frontend_base_url = os.getenv('FRONTEND_URL')
    verification_path = f"/#/verify?token_email_verification={token}"
    verification_link = f"{frontend_base_url}{verification_path}"

    msg = Message(
        subject="Verifique seu e-mail",
        recipients=[email],
        html=f"Olá! Clique no link abaixo para verificar seu e-mail:<br><br>"
             f"<a href='{verification_link}'>{verification_link}</a>"
    )
    mail.send(msg)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'E-mail ou senha ausentes'}), 400
    
    if len(password) < 6:
        return jsonify({'message': 'Senha deve ter no mínimo 6 caracteres'}), 400

    if not validate_email(email):
        return jsonify({'message': 'Formato de e-mail inválido'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    
    if cursor.fetchone():
        return jsonify({'message': 'Usuário já existe'}), 409

    token = generate_verification_token(email)
    send_verification_email(email, token)

    hashed_pw = generate_password_hash(password)
    cursor.execute('INSERT INTO users (email, password, is_verified) VALUES (?, ?, ?)', (email, hashed_pw, False))
    conn.commit()

    return jsonify({'message': 'Sua conta foi criada! Verifique seu e-mail para ativá-la.'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'E-mail ou senha ausentes'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT password, is_verified FROM users WHERE email = ?', (email,))
    result = cursor.fetchone()

    if not result:
        return jsonify({'message': 'Credenciais inválidas'}), 401
    
    hashed_pw, is_verified = result

    if not check_password_hash(hashed_pw, password):
        return jsonify({'message': 'Credenciais inválidas'}), 401
        
    if not is_verified:
        return jsonify({'message': 'Sua conta não foi verificada. Por favor, cheque seu e-mail.'}), 403
    
    access_token = generate_token(email)
    return jsonify({'access_token': access_token}), 200

@auth_bp.route('/verify/<token>', methods=['GET'])
def verify_email(token):
    try:
        email = current_app.config['SERIALIZER'].loads(token, salt='email-verification-salt', max_age=3600)
    except Exception:
        return jsonify({'message': 'O token de verificação é inválido ou expirou'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT is_verified FROM users WHERE email = ?', (email,))
    result = cursor.fetchone()
    
    if not result or result[0] == 1:
        return jsonify({'message': 'A conta já foi verificada ou o usuário não existe'}), 409
    
    cursor.execute('UPDATE users SET is_verified = ? WHERE email = ?', (True, email))
    conn.commit()
    
    return jsonify({'message': 'Seu e-mail foi verificado com sucesso! Você pode fazer login.'}), 200
