from flask import Blueprint, render_template

inventario_bp = Blueprint('inventario', __name__, url_prefix='/inventario')


@inventario_bp.route('/')
def index():
    return render_template(
        'en_construccion.html',
        modulo='Inventario', icono='📦', descripcion='Gestión de productos, bodega y stock',
    )
