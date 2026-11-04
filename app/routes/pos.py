from flask import Blueprint, render_template

pos_bp = Blueprint('pos', __name__, url_prefix='/pos')


@pos_bp.route('/')
def index():
    return render_template(
        'en_construccion.html',
        modulo='Punto de Venta (POS)', icono='🛒', descripcion='Venta rápida en mostrador',
    )
