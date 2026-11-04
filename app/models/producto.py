from app import db

class Categoria(db.Model):
    __tablename__ = 'categorias'
    
    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    estado = db.Column(db.Boolean, default=True)
    
    productos = db.relationship('Producto', backref='categoria', lazy=True)

class Producto(db.Model):
    __tablename__ = 'productos'
    
    id_producto = db.Column(db.Integer, primary_key=True)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias.id_categoria'), nullable=False)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.String(255), nullable=True)
    tipo = db.Column(db.String(50), nullable=False) # Físico o Servicio
    precio_venta = db.Column(db.Numeric(10, 2), nullable=False)
    stock_actual = db.Column(db.Integer, nullable=False, default=0)
    stock_minimo = db.Column(db.Integer, nullable=False, default=5)
    publicado = db.Column(db.Boolean, default=True)
    estado = db.Column(db.Boolean, default=True)

class PresentacionProducto(db.Model):
    __tablename__ = 'presentaciones_producto'
    
    id_presentacion = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos.id_producto'), nullable=False)
    nombre_presentacion = db.Column(db.String(100), nullable=False)
    unidades_por_presentacion = db.Column(db.Integer, nullable=False, default=1)
    precio_venta = db.Column(db.Numeric(10, 2), nullable=False)
    estado = db.Column(db.Boolean, default=True)
    
    producto = db.relationship('Producto', backref='presentaciones', lazy=True)