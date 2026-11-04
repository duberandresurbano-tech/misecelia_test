"""Carga los datos iniciales de Miscelia (se puede ejecutar varias veces sin duplicar nada).

Uso:  python seed.py
Variables opcionales en el .env: ADMIN_USER, ADMIN_PASSWORD
(si no defines ADMIN_PASSWORD, se genera una clave aleatoria y se muestra una sola vez).
"""
import os
import secrets

from app import create_app, db
from app.models import Categoria, Rol, Usuario

ROLES = [
    ('Administrador', 'Acceso total al sistema'),
    ('Vendedor', 'Opera el punto de venta'),
]

CATEGORIAS = ['Bebidas', 'Snacks', 'Aseo', 'Servicios']


def crear_roles():
    for nombre, descripcion in ROLES:
        if not Rol.query.filter_by(nombre=nombre).first():
            db.session.add(Rol(nombre=nombre, descripcion=descripcion))
    db.session.flush()


def crear_categorias():
    for nombre in CATEGORIAS:
        if not Categoria.query.filter_by(nombre=nombre).first():
            db.session.add(Categoria(nombre=nombre))


def crear_admin():
    usuario_acceso = os.getenv('ADMIN_USER', 'admin')
    if Usuario.query.filter_by(usuario_acceso=usuario_acceso).first():
        print(f"El usuario '{usuario_acceso}' ya existe; no se modificó.")
        return

    password = os.getenv('ADMIN_PASSWORD') or secrets.token_urlsafe(12)
    generada = not os.getenv('ADMIN_PASSWORD')

    admin = Usuario(nombre='Administrador', usuario_acceso=usuario_acceso)
    admin.establecer_password(password)
    admin.roles.append(Rol.query.filter_by(nombre='Administrador').one())
    db.session.add(admin)

    print(f"Usuario creado: {usuario_acceso}")
    if generada:
        print(f"Contraseña generada (guárdala, no se mostrará de nuevo): {password}")


def main():
    app = create_app()
    with app.app_context():
        crear_roles()
        crear_categorias()
        crear_admin()
        db.session.commit()
    print("Datos iniciales listos.")


if __name__ == '__main__':
    main()
