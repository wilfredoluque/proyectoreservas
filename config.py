import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mi_clave_ultra_secreta_123'
    DATABASE = os.path.join(BASE_DIR, 'centrocap.db')
