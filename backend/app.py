import os
from flask import jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import sqlite3
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer

from backend.common import app, config, db_path, get_db
from backend.api.auth import auth_bp
from backend.api.google import google_bp
from backend.api.summary import summary_bp

app.secret_key = os.getenv('SECRET_KEY')
CORS(app)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)
jwt = JWTManager(app)

s = URLSafeTimedSerializer(app.secret_key)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10/minute"]
)

conn = get_db()
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

@app.route('/api/config')
def get_config():
    return jsonify(config)

app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(google_bp, url_prefix='/api')
app.register_blueprint(summary_bp, url_prefix='/api')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)