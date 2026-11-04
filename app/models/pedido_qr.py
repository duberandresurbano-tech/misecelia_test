from app import db

class PedidoQR(db.Model):
    __tablename__ = 'pedidos_qr'
    
    id_pedido = db.Column(db.Integer, primary_key=True)
    fecha_hora = db.Column(db.DateTime, server_default=db.func.now())
    estado = db.Column(db.String(50), default='Pendiente')
    codigo_publico = db.Column(db.String(100), unique=True, nullable=False)
    
    detalles = db.relationship('DetallePedidoQR', backref='pedido', lazy=True, cascade="all, delete-orphan")

class DetallePedidoQR(db.Model):
    __tablename__ = 'detalles_pedido_qr'
    
    id_detalle_pedido = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedidos_qr.id_pedido'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    cantidad_solicitada = db.Column(db.Integer, nullable=False)
