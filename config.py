import os

from dotenv import load_dotenv

load_dotenv()


def _normalizar_url_db(url):
    """Asegura que SQLAlchemy use el driver psycopg 3 (el que está en requirements)."""
    if not url:
        return url
    if url.startswith('postgres://'):
        url = 'postgresql://' + url[len('postgres://'):]
    if url.startswith('postgresql://'):
        url = 'postgresql+psycopg://' + url[len('postgresql://'):]
    return url


class Config:
    # Sin valores por defecto: si faltan en el .env, create_app() avisa con un error claro.
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = _normalizar_url_db(os.getenv('DATABASE_URL'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
