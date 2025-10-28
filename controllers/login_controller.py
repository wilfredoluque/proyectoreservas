from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.database import get_db_connection
from werkzeug.security import check_password_hash

bp = Blueprint('login_controller', __name__)

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
            flash('Bienvenido ' + usuario['nombre'], 'success')
            return redirect(url_for('dashboard_controller.index'))
        else:
            flash('Usuario o contraseña incorrecta', 'danger')
            return redirect(url_for('login_controller.login'))

    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente', 'success')
    return redirect(url_for('login_controller.login'))
