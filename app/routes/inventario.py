from flask import Blueprint, render_template

inventario_bp = Blueprint('inventario', __name__, url_prefix='/inventario')

@inventario_bp.route('/')
def index():
    # Por ahora renderizamos la interfaz visual del catálogo de productos
    return render_template('inventario/index.html')