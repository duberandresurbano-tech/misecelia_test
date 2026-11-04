from flask import Blueprint, render_template

qr_portal_bp = Blueprint('qr_portal', __name__, url_prefix='/qr')


@qr_portal_bp.route('/')
def index():
    return render_template(
        'en_construccion.html',
        modulo='Portal QR', icono='📱', descripcion='Gestión de pedidos hechos por código QR',
    )
