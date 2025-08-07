import os
import sqlite3
from flask import Flask, g, json
from pathlib import Path
from dotenv import load_dotenv

app = Flask(__name__)

basedir = os.path.dirname(os.path.abspath(__file__))

# Carrega .env
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Carrega config.json
config_path = os.path.join(basedir, 'config.json')

with open(config_path) as f:
    config = json.load(f)

# Carrega caminho do database
db_path = os.path.join(basedir, 'users.db')

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(db_path)
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()