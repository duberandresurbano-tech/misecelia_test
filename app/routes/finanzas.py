from flask import Blueprint, render_template

from app.services.finanzas_manager import FinanzasManager

finanzas_bp = Blueprint('finanzas', __name__, url_prefix='/finanzas')


@finanzas_bp.route('/')
def index():
    return render_template(
        'finanzas/index.html',
        resumen=FinanzasManager.calcular_balance_diario(),
        movimientos=FinanzasManager.movimientos_del_dia(),
    )
