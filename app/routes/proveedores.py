from flask import Blueprint, render_template

proveedores_bp = Blueprint('proveedores', __name__, url_prefix='/proveedores')

@proveedores_bp.route('/')
def index():
    return render_template('proveedores/index.html')