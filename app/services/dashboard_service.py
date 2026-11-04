from datetime import date

from sqlalchemy import func

from app import db
from app.models import PedidoQR, Producto, Venta
from app.services.finanzas_manager import ESTADO_COMPLETADA, rango_dia


class DashboardService:

    @staticmethod
    def resumen_hoy() -> dict:
        """Datos operativos del día para el panel principal."""
        inicio, fin = rango_dia(date.today())

        filas = db.session.query(
            Venta.medio_pago, func.coalesce(func.sum(Venta.total), 0)
        ).filter(
            Venta.fecha_hora >= inicio, Venta.fecha_hora < fin,
            Venta.estado == ESTADO_COMPLETADA,
        ).group_by(Venta.medio_pago).order_by(Venta.medio_pago).all()
        ventas_por_medio = [(medio, float(total)) for medio, total in filas]

        productos_agotados = Producto.query.filter(
            Producto.estado.is_(True),
            Producto.tipo == 'Físico',
            Producto.stock_actual <= 0,
        ).count()

        pedidos_pendientes = PedidoQR.query.filter_by(estado='Pendiente').count()
        pedidos_atendidos = PedidoQR.query.filter(
            PedidoQR.estado == 'Atendido',
            PedidoQR.fecha_hora >= inicio, PedidoQR.fecha_hora < fin,
        ).count()

        return {
            "ventas_por_medio": ventas_por_medio,
            "productos_agotados": productos_agotados,
            "pedidos_pendientes": pedidos_pendientes,
            "pedidos_atendidos": pedidos_atendidos,
        }
