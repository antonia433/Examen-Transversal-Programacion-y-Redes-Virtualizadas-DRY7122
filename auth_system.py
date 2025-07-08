#!/usr/bin/env python3
from flask import Flask, request, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
DATABASE = 'users.db'

# Plantilla HTML
LOGIN_TEMPLATE = """
<!doctype html>
<html>
<head><title>Login</title></head>
<body>
    <h2>Iniciar Sesión</h2>
    <form method="post">
        <input type="text" name="username" placeholder="Usuario" required><br>
        <input type="password" name="password" placeholder="Contraseña" required><br>
        <button type="submit">Ingresar</button>
    </form>
</body>
</html>
"""

# Configuración inicial de la base de datos
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password_hash TEXT
        )
    ''')
    # Agregar usuarios de ejemplo (nombres de integrantes)
    users = [
        ("Antonia", generate_password_hash("clave123")),
        ("Jorge", generate_password_hash("clave234"))
    ]
    for user, pwd_hash in users:
        cursor.execute("INSERT OR IGNORE INTO users (username, password_hash) VALUES (?, ?)", (user, pwd_hash))
    conn.commit()
    conn.close()

# Ruta de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        if user and check_password_hash(user[0], password):
            return f"¡Bienvenido {username}!"
        return "Credenciales inválidas"
    return render_template_string(LOGIN_TEMPLATE)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=7500, debug=True)
