from flask import Blueprint, render_template

pos_bp = Blueprint('pos', __name__, url_prefix='/pos')

@pos_bp.route('/')
def index():
    # Por ahora solo renderizamos la interfaz visual estática
    return render_template('pos/index.html')