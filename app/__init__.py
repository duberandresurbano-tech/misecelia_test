from flask import Flask, flash, redirect, request, session, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect  # <--- 1. Importa el protector CSRF

from config import Config

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

# Rutas que se pueden abrir sin iniciar sesión. Todo lo demás exige login.
RUTAS_PUBLICAS = {'auth.login', 'static'}


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    

    if not app.config.get('SECRET_KEY') or not app.config.get('SQLALCHEMY_DATABASE_URI'):
        raise RuntimeError(
            "Faltan SECRET_KEY o DATABASE_URL. Crea tu archivo .env a partir de .env.example."
        )

    # 1. Extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # 2. Modelos (necesarios para que Flask-Migrate los detecte)
    from app import models  # noqa: F401

    # 3. Blueprints
    from app.routes.auth import auth_bp
    from app.routes.finanzas import finanzas_bp
    from app.routes.inventario import inventario_bp
    from app.routes.main import main_bp
    from app.routes.pos import pos_bp
    from app.routes.qr_portal import qr_portal_bp
    from app.routes.pos import pos_bp
    from app.routes.proveedores import proveedores_bp
    from app.routes.corte_caja import corte_caja_bp

    for blueprint in (auth_bp, main_bp, finanzas_bp, inventario_bp, pos_bp, qr_portal_bp, proveedores_bp, corte_caja_bp):
        app.register_blueprint(blueprint)

    # 4. Protección global: sin sesión iniciada, todo redirige al login
    @app.before_request
    def exigir_login():
        if request.endpoint is None or request.endpoint in RUTAS_PUBLICAS:
            return None
        if 'usuario_id' not in session:
            flash('Inicia sesión para continuar.', 'warning')
            return redirect(url_for('auth.login'))
        return None
    # 5. proteccion de cierre de sesion con la flechita del navegador
    @app.after_request
    def add_header(response):
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response

    return app
