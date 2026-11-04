from flask import Blueprint, redirect, render_template, url_for

from app.services.dashboard_service import DashboardService
from app.services.finanzas_manager import FinanzasManager

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return redirect(url_for('main.dashboard'))


@main_bp.route('/dashboard')
def dashboard():
    return render_template(
        'admin/dashboard.html',
        resumen=FinanzasManager.calcular_balance_diario(),
        **DashboardService.resumen_hoy(),
    )
