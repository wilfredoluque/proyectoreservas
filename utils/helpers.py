# utils/helpers.py
from functools import wraps
from flask import session, redirect, url_for, flash

# ---------------------------
# Decoradores de autorización
# ---------------------------

def login_required(f):
    """
    Protege rutas que requieren inicio de sesión.
    Si no hay sesión activa, redirige al login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debe iniciar sesión para acceder a esta página.', 'warning')
            return redirect(url_for('auth_controller.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Protege rutas que requieren rol de administrador.
    Redirige a dashboard si el usuario no es admin.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('rol') != 'admin':
            flash('No tiene permisos para acceder a esta página.', 'danger')
            return redirect(url_for('dashboard_controller.index'))
        return f(*args, **kwargs)
    return decorated_function

# ---------------------------
# Funciones de utilidad
# ---------------------------

def is_logged_in():
    """Devuelve True si el usuario ha iniciado sesión."""
    return 'user_id' in session

def is_admin():
    """Devuelve True si el usuario es administrador."""
    return session.get('rol') == 'admin'

def get_current_user():
    """Devuelve la información básica del usuario en sesión."""
    if 'user_id' in session:
        return {
            'id': session.get('user_id'),
            'nombre': session.get('nombre'),
            'rol': session.get('rol')
        }
    return None

def clear_session():
    """Limpia toda la sesión del usuario."""
    session.clear()
