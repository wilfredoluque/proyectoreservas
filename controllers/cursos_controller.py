from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.database import get_db_connection
from utils.helpers import login_required

bp = Blueprint('cursos_controller', __name__)

# --- Listar cursos ---
@bp.route('/')
@login_required
def index():
    conn = get_db_connection()
    cursos = conn.execute("SELECT * FROM cursos").fetchall()
    conn.close()
    return render_template('cursos/list.html', cursos=cursos)

# --- Crear curso ---
@bp.route('/nuevo', methods=['GET','POST'])
@login_required
def nuevo():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        horas = request.form['horas']

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO cursos (descripcion, horas) VALUES (?, ?)",
            (descripcion, horas)
        )
        conn.commit()
        conn.close()
        flash('Curso creado correctamente.', 'success')
        return redirect(url_for('cursos_controller.index'))
    return render_template('cursos/add.html')


# --- Editar curso ---
@bp.route('/edit/<int:id>', methods=['GET','POST'])
@login_required
def editar(id):
    conn = get_db_connection()
    curso = conn.execute("SELECT * FROM cursos WHERE id = ?", (id,)).fetchone()

    if request.method == 'POST':
        descripcion = request.form['descripcion']
        conn.execute("UPDATE cursos SET descripcion = ? WHERE id = ?", (descripcion, id))
        conn.commit()
        conn.close()
        flash('Curso actualizado correctamente.', 'success')
        return redirect(url_for('cursos_controller.index'))

    conn.close()
    return render_template('cursos/edit.html', curso=curso)

# --- Eliminar curso ---
@bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def eliminar(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM cursos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash('Curso eliminado correctamente.', 'success')
    return redirect(url_for('cursos_controller.index'))
