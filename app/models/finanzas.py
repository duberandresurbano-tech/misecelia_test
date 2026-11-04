from app import db


class Gasto(db.Model):
    __tablename__ = 'gastos'

    id_gasto = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    concepto = db.Column(db.String(150), nullable=False)
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_hora = db.Column(db.DateTime, server_default=db.func.now())
    categoria_gasto = db.Column(db.String(100), nullable=False)
