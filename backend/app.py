import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from google import genai
from werkzeug.utils import secure_filename
import PyPDF2
from dotenv import load_dotenv
import os
from pathlib import Path

# Carrega .env da raiz do projeto
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# def extrair_texto_pdf(caminho_pdf):
#     doc = fitz.open(caminho_pdf)
#     texto = ""
#     for pagina in doc:
#         texto += pagina.get_text()
#     return texto

# def extrair_texto_txt(caminho_txt):
#     with open(caminho_txt, 'r', encoding='utf-8') as f:
#         return f.read()

def extrair_texto_pdf(file_stream):
    """
    Lê o fluxo PDF direto da memória e retorna todo o texto.
    """
    # Garante que começamos do início
    file_stream.seek(0)
    reader = PyPDF2.PdfReader(file_stream)
    texto = ''
    for page in reader.pages:
        texto += page.extract_text() or ''
    return texto

def extrair_texto_txt(file_stream):
    """
    Lê o fluxo TXT direto da memória e retorna o conteúdo como string.
    """
    file_stream.seek(0)
    # file_stream.read() devolve bytes
    return file_stream.read().decode('utf-8')

app = Flask(__name__)
CORS(app)  # permite chamadas de fora (frontend)

app.config['JWT_SECRET_KEY'] = 'senha-secreta-trocanaforma-segura'
jwt = JWTManager(app)

# Criar (ou conectar) ao banco de dados SQLite e criar tabela de usuários
conn = sqlite3.connect('users.db')
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

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'message': 'E-mail ou senha ausentes'}), 400

    conn = sqlite3.connect('users.db')
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

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'message': 'E-mail ou senha ausentes'}), 400

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT password FROM users WHERE email = ?', (email,))
    result = cursor.fetchone()
    conn.close()
    if result and check_password_hash(result[0], password):
        # Gera token JWT com o username
        access_token = create_access_token(identity=email)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Credenciais inválidas'}), 401

@app.route('/welcome', methods=['GET'])
@jwt_required()
def welcome():
    current_user = get_jwt_identity()
    return jsonify({'message': f'Bem-vindo, {current_user}!'}), 200

@app.route('/summary', methods=['POST'])
@jwt_required()
def summary():
    # data = request.get_json()

    file = request.files.get('file')
    text = request.form.get('text')
    summary_type = request.form.get('summaryType')

    match summary_type:
        case 'short':
            prompt = 'Faça um pequeno resumo do texto abaixo:'
        case 'regular':
            prompt = 'Faça um resumo médio do texto abaixo:'
        case 'topics':
            prompt = 'Faça um resumo em tópicos do texto abaixo:'
        case _:
            return jsonify({'message': 'Tipo de resumo não existe.'}), 400

    if not text and not file:
        return jsonify({'message': 'Texto ou arquivo são obrigatórios.'}), 400

    if file:
        filename = secure_filename(file.filename)
        file_ext = filename.lower().rsplit('.', 1)[-1]

        if file_ext == 'pdf':
            text = extrair_texto_pdf(file.stream)
        elif file_ext == 'txt':
            text = extrair_texto_txt(file.stream)
        else:
            return jsonify({'error': 'Tipo de arquivo não suportado'}), 400

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=f'{prompt}\n\n"{text}"\n\nO resumo do texto deve estar em português brasileiro.'
        )
        summary_text = response.text
        
    except Exception as e:
        print('Erro Gemini:', e)
        return jsonify({'message': 'Falha ao gerar resumo'}), 500

    return jsonify({'summary': summary_text}), 200
@app.route('/extract-text', methods=['POST'])
@jwt_required()
def extract_text():
    file = request.files.get('file')

    if not file:
        return jsonify({'message': 'Nenhum arquivo enviado.'}), 400

    filename = secure_filename(file.filename)
    file_ext = filename.lower().rsplit('.', 1)[-1]

    if file_ext == 'pdf':
        text = extrair_texto_pdf(file.stream)
    elif file_ext == 'txt':
        text = extrair_texto_txt(file.stream)
    else:
        return jsonify({'error': 'Tipo de arquivo não suportado'}), 400

    return jsonify({'text': text}), 200

if __name__ == '__main__':
    app.run(debug=True)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8080)