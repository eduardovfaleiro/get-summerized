
import os
import sqlite3

from flask import g


basedir = os.path.dirname(os.path.abspath(__file__))
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