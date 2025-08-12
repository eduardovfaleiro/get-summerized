import os
from flask import Blueprint, current_app, jsonify, redirect, url_for
from authlib.integrations.flask_client import OAuth
from backend.jwt_utils import generate_token

oauth = OAuth()
google_bp = Blueprint('google_bp', __name__)

def init_oauth(app):
    oauth.init_app(app)

    client_id = os.getenv('GOOGLE_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET')

    oauth.register(
        name='google',
        client_id=client_id,
        client_secret=client_secret,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        api_base_url='https://openidconnect.googleapis.com/v1/',
        client_kwargs={
            'scope': 'openid email profile',
            'prompt': 'consent',
            'access_type': 'offline'
        }
    )

@google_bp.route('/login/google/initiate')
def initiate_login_google():
    return jsonify({"status": "ok"}), 200

@google_bp.route('/login/google')
def login_google():
    redirect_uri = url_for('google_bp.authorize_google', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@google_bp.route('/login/google/callback')
def authorize_google():
    token = oauth.google.authorize_access_token()
    resp = oauth.google.get('userinfo')
    user_info = resp.json()

    # Aqui você pode criar ou buscar o usuário no seu banco
    # e gerar um token JWT ou sessão
    email = user_info['email']
    name = user_info['name']

    # Exemplo de resposta com redirecionamento + token
    access_token = generate_token(email)
    return redirect(f"http://localhost:8081/#/welcome?token={access_token}")