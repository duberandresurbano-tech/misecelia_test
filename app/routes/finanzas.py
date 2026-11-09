from flask import Blueprint, render_template, request
from app.services.finanzas_manager import FinanzasManager

finanzas_bp = Blueprint('finanzas', __name__, url_prefix='/finanzas')

@finanzas_bp.route('/')
def index():
    # Captura el filtro que viene por la URL (?filtro=dia, mes, anios, etc.), por defecto 'meses'
    filtro_seleccionado = request.args.get('filtro', 'meses')
    
    # Extrae los datos reales calculados desde la base de datos con el manager
    macro_data = FinanzasManager.obtener_finanzas_macro(filtro_seleccionado)
    
    return render_template(
        'finanzas/index.html', 
        macro=macro_data, 
        filtro_actual=filtro_seleccionado
    )