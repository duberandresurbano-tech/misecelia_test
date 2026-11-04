from app import db

class Venta(db.Model):
    __tablename__ = 'ventas'
    
    id_venta = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    fecha_hora = db.Column(db.DateTime, server_default=db.func.now())
    total = db.Column(db.Numeric(10, 2), nullable=False)
    medio_pago = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.String(50), default='Completada')
    
    detalles = db.relationship('DetalleVenta', backref='venta', lazy=True, cascade="all, delete-orphan")
    historial = db.relationship('HistorialCorreccionVenta', backref='venta', lazy=True)

class DetalleVenta(db.Model):
    __tablename__ = 'detalles_venta'
    
    id_detalle_venta = db.Column(db.Integer, primary_key=True)
    id_venta = db.Column(db.Integer, db.ForeignKey('ventas.id_venta'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    id_presentacion = db.Column(db.Integer, db.ForeignKey('presentaciones_producto.id_presentacion'), nullable=True)
    cantidad = db.Column(db.Integer, nullable=False)
    unidades_por_presentacion_aplicadas = db.Column(db.Integer, nullable=False, default=1)
    precio_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)

class HistorialCorreccionVenta(db.Model):
    __tablename__ = 'historial_correccion_ventas'
    
    id_historial = db.Column(db.Integer, primary_key=True)
    id_venta = db.Column(db.Integer, db.ForeignKey('ventas.id_venta'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    fecha_hora = db.Column(db.DateTime, server_default=db.func.now())
    tipo_accion = db.Column(db.String(50), nullable=False)
    motivo = db.Column(db.String(255), nullable=False)
    datos_anteriores = db.Column(db.Text, nullable=True)
    datos_nuevos = db.Column(db.Text, nullable=True)