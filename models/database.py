import sqlite3
from werkzeug.security import generate_password_hash
from config import Config
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

def get_db_connection():
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabla estudiantes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS estudiantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellidos TEXT NOT NULL,
            correo TEXT NOT NULL,
            celular TEXT NOT NULL
        )
    """)

    # Tabla cursos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cursos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            horas INTEGER NOT NULL
        )
    """)

    # Tabla inscripciones
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inscripcion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            estudiante_id INTEGER NOT NULL,
            curso_id INTEGER NOT NULL,
            fecha DATE NOT NULL,
            FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id),
            FOREIGN KEY (curso_id) REFERENCES cursos(id)
        )
    """)

    # Tabla usuarios (coherente con controlador y vistas)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            rol TEXT NOT NULL
        )
    """)

    # Insertar usuario por defecto si no existe
    cursor.execute("SELECT * FROM usuarios WHERE nombre = ?", ('admin',))
    if not cursor.fetchone():
        hashed = generate_password_hash('admin123')
        cursor.execute("""
            INSERT INTO usuarios (nombre, email, password, rol)
            VALUES (?, ?, ?, ?)
        """, ('admin', 'admin@correo.com', hashed, 'admin'))

    conn.commit()
    conn.close()

# Crear tablas al ejecutar directamente este archivo
if __name__ == '__main__':
    create_tables()
    print("Tablas creadas y usuario por defecto listo.")
