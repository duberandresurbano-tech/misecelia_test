from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError

from app import db

ph = PasswordHasher()

# Tabla intermedia UsuarioRol (Muchos a Muchos según tu MER)
usuario_rol = db.Table(
    'usuario_rol',
    db.Column('id_usuario', db.Integer, db.ForeignKey('usuarios.id_usuario'), primary_key=True),
    db.Column('id_rol', db.Integer, db.ForeignKey('roles.id_rol'), primary_key=True),
)


class Rol(db.Model):
    __tablename__ = 'roles'

    id_rol = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.String(200), nullable=True)


class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    usuario_acceso = db.Column(db.String(50), unique=True, nullable=False)
    hash_contrasena = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.Boolean, default=True)

    # --- NUEVOS CAMPOS CLAVE PARA ROLES Y SEGURIDAD ---
    rol = db.Column(db.String(20), default='Vendedor', nullable=False)  # 'Administrador' o 'Vendedor'
    activo = db.Column(db.Boolean, default=True, nullable=False)        # Para poder desactivarlos al vuelo

    roles = db.relationship('Rol', secondary=usuario_rol, backref=db.backref('usuarios', lazy='dynamic'))

    def establecer_password(self, password):
        self.hash_contrasena = ph.hash(password)

    def verificar_password(self, password):
        try:
            return ph.verify(self.hash_contrasena, password)
        except (VerificationError, InvalidHashError):
            return False
