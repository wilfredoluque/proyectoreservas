from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.database import get_db_connection
import sqlite3

bp = Blueprint('auth_controller', __name__)

# --- Página de login ---
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']

        conn = get_db_connection()
        usuario = conn.execute("SELECT * FROM usuarios WHERE nombre = ?", (nombre,)).fetchone()
        conn.close()

        if usuario and check_password_hash(usuario['password'], password):
            session['user_id'] = usuario['id']
            session['user_nombre'] = usuario['nombre']
            session['user_rol'] = usuario['rol']
            flash(f'Bienvenido {usuario["nombre"]}', 'success')
            return redirect(url_for('dashboard_controller.index'))
        else:
            flash('Usuario o contraseña incorrectos.', 'danger')

    return render_template('auth/login.html')


# --- Página de registro ---
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        confirmar = request.form['confirmar']
        rol = request.form.get('rol', 'usuario')  # opcional, por defecto usuario

        if password != confirmar:
            flash('Las contraseñas no coinciden.', 'danger')
            return render_template('auth/register.html')
        
        conn = get_db_connection()
        try:
            hashed = generate_password_hash(password)
            conn.execute('''
                INSERT INTO usuarios (nombre, email, password, rol)
                VALUES (?, ?, ?, ?)
            ''', (nombre, email, hashed, rol))
            conn.commit()
            flash('Usuario registrado correctamente.', 'success')
            return redirect(url_for('auth_controller.login'))
        except sqlite3.IntegrityError:
            flash('El nombre de usuario o correo ya existe.', 'danger')
        finally:
            conn.close()

    return render_template('auth/register.html')


# --- Cerrar sesión ---
@bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('auth_controller.login'))
