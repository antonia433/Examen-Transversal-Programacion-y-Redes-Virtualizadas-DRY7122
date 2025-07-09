from flask import Flask, render_template_string, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

# Inicialización de la aplicación Flask
app = Flask(__name__)
app.secret_key = 'clave_secreta_examen'
app.config['DATABASE'] = 'integrantes.db'
app.config['PORT'] = 7500  # Puerto obligatorio 7500

# Función para conexión a la base de datos
def get_db_connection():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

# Inicialización de la base de datos
def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS integrantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        ''')
        conn.commit()

# Función para agregar integrante
def add_integrante(nombre, password):
    password_hash = generate_password_hash(password)
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO integrantes (nombre, password_hash) VALUES (?, ?)',
                         (nombre, password_hash))
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

# Función para verificar integrante
def verify_integrante(nombre, password):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT password_hash FROM integrantes WHERE nombre = ?', (nombre,))
        result = cursor.fetchone()
        if result and check_password_hash(result['password_hash'], password):
            return True
    return False

# Función para obtener todos los integrantes
def get_all_integrantes():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT nombre, password_hash FROM integrantes')
        return cursor.fetchall()

# Rutas del sitio web
@app.route('/')
def home():
    if 'nombre' in session:
        return render_template_string('''
            <h1>Sistema de Integrantes</h1>
            <h2>Bienvenido, {{ nombre }}!</h2>
            <p><a href="/logout">Cerrar sesión</a></p>
            <p><a href="/ver_integrantes">Ver integrantes registrados</a></p>
        ''', nombre=session['nombre'])
    return render_template_string('''
        <h1>Sistema de Integrantes del Examen</h1>
        <p><a href="/login">Iniciar sesión</a></p>
    ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']
        if verify_integrante(nombre, password):
            session['nombre'] = nombre
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Credenciales incorrectas.', 'danger')
    return render_template_string('''
        <h2>Inicio de sesión</h2>
        <form method="post">
            Nombre: <input type="text" name="nombre" required><br>
            Contraseña: <input type="password" name="password" required><br>
            <button type="submit">Iniciar sesión</button>
        </form>
    ''')

@app.route('/logout')
def logout():
    session.pop('nombre', None)
    flash('Has cerrado sesión correctamente.', 'info')
    return redirect(url_for('home'))

@app.route('/ver_integrantes')
def ver_integrantes():
    if 'nombre' not in session:
        return redirect(url_for('login'))
    
    integrantes = get_all_integrantes()
    lista_integrantes = ''.join([f'<li>{integrante["nombre"]} - Hash: {integrante["password_hash"]}</li>' 
                               for integrante in integrantes])
    
    return render_template_string('''
        <h2>Integrantes Registrados</h2>
        <ul>{{ lista_integrantes }}</ul>
        <p><a href="/">Volver al inicio</a></p>
    ''', lista_integrantes=lista_integrantes)

# Configuración inicial
if __name__ == '__main__':
    # Crear la base de datos si no existe
    if not os.path.exists(app.config['DATABASE']):
        init_db()
    
    # Agregar integrantes (Antonia y Jorge)
    integrantes_examen = [
        ('Antonia', 'clave1'),
        ('Jorge', 'clave2')
    ]
    
    for nombre, password in integrantes_examen:
        if not verify_integrante(nombre, password):
            add_integrante(nombre, password)
    
    # Ejecutar la aplicación en el puerto 7500
    app.run(port=7500, debug=True)
