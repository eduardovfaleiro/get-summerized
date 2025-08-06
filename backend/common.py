import os
from flask import Flask, json
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