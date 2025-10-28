from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.database import get_db_connection
from utils.helpers import login_required
from werkzeug.security import generate_password_hash

bp = Blueprint('usuarios_controller', __name__)

# --- Listar usuarios ---
@bp.route('/')
@login_required
def index():
    conn = get_db_connection()
    usuarios = conn.execute("SELECT * FROM usuarios").fetchall()
    conn.close()
    return render_template('usuarios/list.html', usuarios=usuarios)

# --- Crear usuario ---
@bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        rol = request.form['rol']

        hashed = generate_password_hash(password)

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO usuarios (nombre, email, password, rol) VALUES (?, ?, ?, ?)",
            (nombre, email, hashed, rol)
        )
        conn.commit()
        conn.close()
        flash('Usuario creado correctamente.', 'success')
        return redirect(url_for('usuarios_controller.index'))

    return render_template('usuarios/add.html')

# --- Editar usuario ---
@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    conn = get_db_connection()
    usuario = conn.execute("SELECT * FROM usuarios WHERE id = ?", (id,)).fetchone()

    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']
        rol = request.form['rol']

        if password:  # si el usuario cambia la contraseña
            hashed = generate_password_hash(password)
            conn.execute(
                "UPDATE usuarios SET nombre = ?, email = ?, password = ?, rol = ? WHERE id = ?",
                (nombre, email, hashed, rol, id)
            )
        else:
            conn.execute(
                "UPDATE usuarios SET nombre = ?, email = ?, rol = ? WHERE id = ?",
                (nombre, email, rol, id)
            )

        conn.commit()
        conn.close()
        flash('Usuario actualizado correctamente.', 'success')
        return redirect(url_for('usuarios_controller.index'))

    conn.close()
    return render_template('usuarios/edit.html', usuario=usuario)

# --- Eliminar usuario ---
@bp.route('/delete/<int:id>')
@login_required
def eliminar(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM usuarios WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('Usuario eliminado correctamente.', 'success')
    return redirect(url_for('usuarios_controller.index'))
