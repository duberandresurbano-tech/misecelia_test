from flask import Blueprint, render_template
from app.services.finanzas_manager import FinanzasManager

corte_caja_bp = Blueprint('corte_caja', __name__, url_prefix='/corte-caja')

@corte_caja_bp.route('/')
def index():
    return render_template(
        'corte_caja/index.html',
        resumen=FinanzasManager.calcular_balance_diario(),
        movimientos=FinanzasManager.movimientos_del_dia(),
    )