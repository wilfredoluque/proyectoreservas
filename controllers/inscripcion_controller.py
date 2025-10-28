from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.database import get_db_connection
from utils.helpers import login_required

bp = Blueprint('inscripcion_controller', __name__)

# --- Listar inscripciones ---
@bp.route('/')
@login_required
def index():
    conn = get_db_connection()
    inscripciones = conn.execute("""
        SELECT i.id, i.fecha,
               e.nombre || ' ' || e.apellidos AS nombre_estudiante,
               c.descripcion AS descripcion_curso
        FROM inscripcion i
        JOIN estudiantes e ON i.estudiante_id = e.id
        JOIN cursos c ON i.curso_id = c.id
    """).fetchall()
    conn.close()
    return render_template('inscripciones/list.html', inscripciones=inscripciones)

# --- Crear nueva inscripción ---
@bp.route('/nuevo', methods=['GET','POST'])
@login_required
def nueva():
    conn = get_db_connection()
    estudiantes = conn.execute("SELECT * FROM estudiantes").fetchall()
    cursos = conn.execute("SELECT * FROM cursos").fetchall()

    if request.method == 'POST':
        estudiante_id = request.form['id_estudiante']
        curso_id = request.form['id_curso']
        fecha = request.form['fecha']

        conn.execute(
            "INSERT INTO inscripcion (estudiante_id, curso_id, fecha) VALUES (?, ?, ?)",
            (estudiante_id, curso_id, fecha)
        )
        conn.commit()
        conn.close()
        flash('Inscripción creada correctamente.', 'success')
        return redirect(url_for('inscripcion_controller.index'))

    conn.close()
    return render_template('inscripciones/add.html', estudiantes=estudiantes, cursos=cursos)

# --- Editar inscripción ---
@bp.route('/edit/<int:id>', methods=['GET','POST'])
@login_required
def editar(id):
    conn = get_db_connection()
    inscripcion = conn.execute("SELECT * FROM inscripcion WHERE id = ?", (id,)).fetchone()
    estudiantes = conn.execute("SELECT * FROM estudiantes").fetchall()
    cursos = conn.execute("SELECT * FROM cursos").fetchall()

    if request.method == 'POST':
        estudiante_id = request.form['id_estudiante']
        curso_id = request.form['id_curso']
        fecha = request.form['fecha']

        conn.execute(
            "UPDATE inscripcion SET estudiante_id = ?, curso_id = ?, fecha = ? WHERE id = ?",
            (estudiante_id, curso_id, fecha, id)
        )
        conn.commit()
        conn.close()
        flash('Inscripción actualizada correctamente.', 'success')
        return redirect(url_for('inscripcion_controller.index'))

    conn.close()
    return render_template('inscripciones/edit.html', inscripcion=inscripcion, estudiantes=estudiantes, cursos=cursos)

# --- Eliminar inscripción ---
@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM inscripcion WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('Inscripción eliminada correctamente.', 'success')
    return redirect(url_for('inscripcion_controller.index'))
