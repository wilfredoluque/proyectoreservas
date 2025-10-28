from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.database import get_db_connection
from utils.helpers import login_required

bp = Blueprint('estudiantes_controller', __name__, template_folder='../views/estudiantes')


# --- Listar estudiantes ---
@bp.route('/')
@login_required
def index():
    conn = get_db_connection()
    estudiantes = conn.execute("SELECT * FROM estudiantes").fetchall()
    conn.close()
    return render_template('estudiantes/list.html', estudiantes=estudiantes)


# --- Crear estudiante ---
@bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        correo = request.form['correo']
        celular = request.form['celular']

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO estudiantes (nombre, apellidos, correo, celular) VALUES (?, ?, ?, ?)",
            (nombre, apellidos, correo, celular)
        )
        conn.commit()
        conn.close()
        flash('Estudiante creado correctamente.', 'success')
        return redirect(url_for('estudiantes_controller.index'))
    return render_template('estudiantes/add.html')


# --- Editar estudiante ---
@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    conn = get_db_connection()
    estudiante = conn.execute("SELECT * FROM estudiantes WHERE id = ?", (id,)).fetchone()

    if not estudiante:
        flash('Estudiante no encontrado.', 'danger')
        conn.close()
        return redirect(url_for('estudiantes_controller.index'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        correo = request.form['correo']
        celular = request.form['celular']

        conn.execute(
            "UPDATE estudiantes SET nombre = ?, apellidos = ?, correo = ?, celular = ? WHERE id = ?",
            (nombre, apellidos, correo, celular, id)
        )
        conn.commit()
        conn.close()
        flash('Estudiante actualizado correctamente.', 'success')
        return redirect(url_for('estudiantes_controller.index'))

    conn.close()
    return render_template('estudiantes/edit.html', estudiante=estudiante)


# --- Eliminar estudiante ---
@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM estudiantes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('Estudiante eliminado correctamente.', 'success')
    return redirect(url_for('estudiantes_controller.index'))
