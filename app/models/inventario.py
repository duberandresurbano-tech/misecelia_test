from app import db

class MovimientoInventario(db.Model):
    __tablename__ = 'movimientos_inventario'
    
    id_movimiento = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    tipo_movimiento = db.Column(db.String(50), nullable=False) # Entrada, Salida, Ajuste
    cantidad_base = db.Column(db.Integer, nullable=False)
    fecha_hora = db.Column(db.DateTime, server_default=db.func.now())
    motivo = db.Column(db.String(255), nullable=True)
    tipo_referencia = db.Column(db.String(50), nullable=True) # Compra, Venta, etc.
    id_referencia = db.Column(db.Integer, nullable=True)
    
    producto = db.relationship('Producto', backref='movimientos', lazy=True)