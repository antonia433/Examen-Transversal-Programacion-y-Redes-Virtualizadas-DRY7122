#!/usr/bin/env python3
from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3
import hashlib
import os

app = Flask(__name__)
DATABASE = '/home/devasc/labs/devnet-src/Examen-DRV7122/users.db'

# HTML template
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Autenticación DRV7122</title>
</head>
<body>
    <h2>Login - Examen DRV7122</h2>
    {% if error %}
    <p style="color:red">{{ error }}</p>
    {% endif %}
    <form method="POST">
        <label>Usuario:</label><br>
        <input type="text" name="username" required><br>
        <label>Contraseña:</label><br>
        <input type="password" name="password" required><br><br>
        <input type="submit" value="Ingresar">
    </form>
</body>
</html>
"""

def init_db():
    """Initialize the database"""
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        conn.commit()

def create_user(username, password):
    """Create a new user with hashed password"""
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    try:
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', 
                         (username, password_hash))
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def verify_user(username, password):
    """Verify user credentials"""
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        return result is not None and result[0] == password_hash

@app.route('/', methods=['GET', 'POST'])
def login():
    """Login route"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verify_user(username, password):
            return f"<h1>Bienvenido {username}! - Examen DRV7122</h1>"
        else:
            return render_template_string(LOGIN_TEMPLATE, error="Credenciales incorrectas")
    return render_template_string(LOGIN_TEMPLATE)

if __name__ == '__main__':
    init_db()
    
    # Agregar usuarios iniciales 
    integrantes = [
        ("Antonia", "clave1"),
        ("Jorge", "clave2"),
    ]
    
    for user, pwd in integrantes:
        create_user(user, pwd)
    
    print("Servidor iniciado en http://localhost:7500")
    app.run(host='0.0.0.0', port=7500, debug=True)
