from flask import Flask, render_template_string, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta_7500'
app.config['DATABASE'] = 'integrantes.db'
app.config['PORT'] = 7500

def init_db():
    with sqlite3.connect(app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS integrantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        ''')
        conn.commit()

def add_integrante(nombre, password):
    password_hash = generate_password_hash(password)
    try:
        with sqlite3.connect(app.config['DATABASE']) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO integrantes (nombre, password_hash) VALUES (?, ?)',
                         (nombre, password_hash))
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def verify_integrante(nombre, password):
    with sqlite3.connect(app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT password_hash FROM integrantes WHERE nombre = ?', (nombre,))
        result = cursor.fetchone()
        if result and check_password_hash(result[0], password):
            return True
    return False

@app.route('/')
def home():
    if 'nombre' in session:
        return f"Bienvenido {session['nombre']}! <a href='/logout'>Salir</a>"
    return "<a href='/login'>Login</a>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if verify_integrante(request.form['nombre'], request.form['password']):
            session['nombre'] = request.form['nombre']
            return redirect('/')
    return '''
        <form method="post">
            Nombre: <input type="text" name="nombre"><br>
            Password: <input type="password" name="password"><br>
            <button type="submit">Login</button>
        </form>
    '''

@app.route('/logout')
def logout():
    session.pop('nombre', None)
    return redirect('/')

if __name__ == '__main__':
    init_db()
    add_integrante("Antonia", "clave1")
    add_integrante("Jorge", "clave2")
    app.run(port=7500)
