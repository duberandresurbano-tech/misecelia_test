from app import db

class Proveedor(db.Model):
    __tablename__ = 'proveedores'
    
    id_proveedor = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    contacto = db.Column(db.String(100), nullable=True)
    telefono = db.Column(db.String(50), nullable=True)
    direccion = db.Column(db.String(200), nullable=True)
    estado = db.Column(db.Boolean, default=True)
    
    compras = db.relationship('Compra', backref='proveedor', lazy=True)

class Compra(db.Model):
    __tablename__ = 'compras'
    
    id_compra = db.Column(db.Integer, primary_key=True)
    id_proveedor = db.Column(db.Integer, db.ForeignKey('proveedores.id_proveedor'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    fecha_hora = db.Column(db.DateTime, server_default=db.func.now())
    total = db.Column(db.Numeric(10, 2), nullable=False)
    estado = db.Column(db.String(50), default='Completada')
    
    detalles = db.relationship('DetalleCompra', backref='compra', lazy=True, cascade="all, delete-orphan")

class DetalleCompra(db.Model):
    __tablename__ = 'detalles_compra'
    
    id_detalles_compra = db.Column(db.Integer, primary_key=True)
    id_compra = db.Column(db.Integer, db.ForeignKey('compras.id_compra'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    id_presentacion = db.Column(db.Integer, db.ForeignKey('presentaciones_producto.id_presentacion'), nullable=True)
    cantidad = db.Column(db.Integer, nullable=False)
    unidades_por_presentacion_aplicadas = db.Column(db.Integer, nullable=False, default=1)
    costo_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)