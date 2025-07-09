from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
DATABASE = 'users.db'

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
    # Usuarios de prueba (nombres de integrantes)
    users = [
        ("Antonia", generate_password_hash("clave1")),
        ("Jorge", generate_password_hash("clave2"))
    ]
    for user, pwd_hash in users:
        cursor.execute("INSERT OR IGNORE INTO users (username, password_hash) VALUES (?, ?)", (user, pwd_hash))
    conn.commit()
    conn.close()

# Endpoint de autenticación
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user[0], password):
        return jsonify({"status": "success", "message": f"Bienvenido {username}"})
    return jsonify({"status": "error", "message": "Credenciales inválidas"}), 401

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=7500, debug=True)
