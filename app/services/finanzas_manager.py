from datetime import date, datetime, time, timedelta
from decimal import Decimal
from sqlalchemy import func
from app import db
from app.models import Compra, Gasto, Venta

ESTADO_COMPLETADA = 'Completada'


# --- Rangos de fechas (inicio incluido, fin excluido) ---

def rango_dia(dia: date):
    inicio = datetime.combine(dia, time.min)
    return inicio, inicio + timedelta(days=1)


def rango_mes(anio: int, mes: int):
    inicio = datetime(anio, mes, 1)
    fin = datetime(anio + 1, 1, 1) if mes == 12 else datetime(anio, mes + 1, 1)
    return inicio, fin


def rango_anio(anio: int):
    return datetime(anio, 1, 1), datetime(anio + 1, 1, 1)


class FinanzasManager:

    @staticmethod
    def _sumar(columna_valor, columna_fecha, inicio, fin, *filtros):
        """Suma una columna dentro de un rango de fechas."""
        total = db.session.query(func.coalesce(func.sum(columna_valor), 0)).filter(
            columna_fecha >= inicio, columna_fecha < fin, *filtros
        ).scalar()
        return Decimal(str(total))

    @staticmethod
    def calcular_balance(inicio: datetime, fin: datetime) -> dict:
        """Balance del rango: ventas - (gastos + compras). Ignora ventas/compras no completadas."""
        ventas = FinanzasManager._sumar(
            Venta.total, Venta.fecha_hora, inicio, fin, Venta.estado == ESTADO_COMPLETADA)
        gastos = FinanzasManager._sumar(Gasto.valor, Gasto.fecha_hora, inicio, fin)
        compras = FinanzasManager._sumar(
            Compra.total, Compra.fecha_hora, inicio, fin, Compra.estado == ESTADO_COMPLETADA)

        return {
            "ventas": float(ventas),
            "gastos": float(gastos),
            "compras": float(compras),
            "balance_neto": float(ventas - (gastos + compras)),
        }

    @staticmethod
    def calcular_balance_diario(fecha_objetivo: date = None) -> dict:
        """Balance de un día (por defecto, hoy)."""
        fecha_objetivo = fecha_objetivo or date.today()
        resultado = FinanzasManager.calcular_balance(*rango_dia(fecha_objetivo))
        return {"fecha": str(fecha_objetivo), **resultado}

    @staticmethod
    def calcular_balance_mensual(anio: int, mes: int) -> dict:
        """Balance de un mes y año específicos."""
        resultado = FinanzasManager.calcular_balance(*rango_mes(anio, mes))
        return {"anio": anio, "mes": mes, **resultado}

    @staticmethod
    def calcular_balance_anual(anio: int) -> dict:
        """Balance global de todo un año."""
        resultado = FinanzasManager.calcular_balance(*rango_anio(anio))
        return {"anio": anio, **resultado}

    @staticmethod
    def movimientos_del_dia(fecha_objetivo: date = None) -> list:
        """Lista unificada de ventas, compras y gastos del día, ordenada por hora."""
        fecha_objetivo = fecha_objetivo or date.today()
        inicio, fin = rango_dia(fecha_objetivo)
        movimientos = []

        ventas = Venta.query.filter(
            Venta.fecha_hora >= inicio, Venta.fecha_hora < fin,
            Venta.estado == ESTADO_COMPLETADA).all()
        for v in ventas:
            movimientos.append({
                "fecha_hora": v.fecha_hora, "id": v.id_venta, "tipo": "Venta",
                "descripcion": f"Venta #{v.id_venta}", "metodo": v.medio_pago,
                "monto": float(v.total),
            })

        compras = Compra.query.filter(
            Compra.fecha_hora >= inicio, Compra.fecha_hora < fin,
            Compra.estado == ESTADO_COMPLETADA).all()
        for c in compras:
            movimientos.append({
                "fecha_hora": c.fecha_hora, "id": c.id_compra, "tipo": "Compra",
                "descripcion": f"Compra #{c.id_compra}", "metodo": "—",
                "monto": -float(c.total),
            })

        gastos = Gasto.query.filter(Gasto.fecha_hora >= inicio, Gasto.fecha_hora < fin).all()
        for g in gastos:
            movimientos.append({
                "fecha_hora": g.fecha_hora, "id": g.id_gasto, "tipo": "Gasto",
                "descripcion": g.concepto, "metodo": "—",
                "monto": -float(g.valor),
            })

        return sorted(movimientos, key=lambda m: m["fecha_hora"])

    @staticmethod
    def obtener_finanzas_macro(filtro: str = 'meses') -> dict:
        """
        Calcula el balance global según el botón de filtro seleccionado en la interfaz macro:
        'dia', 'dias', 'mes', 'meses', 'anio', 'anios'
        """
        hoy = date.today()
        
        if filtro == 'dia':
            inicio, fin = rango_dia(hoy)
        elif filtro == 'dias':
            # Últimos 7 días
            inicio = datetime.combine(hoy - timedelta(days=7), time.min)
            fin = datetime.combine(hoy, time.max)
        elif filtro == 'mes':
            inicio, fin = rango_mes(hoy.year, hoy.month)
        elif filtro == 'meses':
            # Últimos 6 meses
            inicio = datetime(hoy.year, hoy.month, 1) - timedelta(days=180)
            fin = datetime.combine(hoy, time.max)
        elif filtro == 'anio':
            inicio, fin = rango_anio(hoy.year)
        elif filtro == 'anios':
            # Últimos 2 años
            inicio = datetime(hoy.year - 2, 1, 1)
            fin = datetime.combine(hoy, time.max)
        else:
            inicio, fin = rango_mes(hoy.year, hoy.month)

        balance = FinanzasManager.calcular_balance(inicio, fin)

        return {
            "periodo_activo": filtro.capitalize(),
            "ingresos_totales": balance["ventas"],
            "gastos_totales": balance["gastos"] + balance["compras"], # Sumamos gastos + compras a proveedores
            "utilidad_neta": balance["balance_neto"],
            "historial": []  # Preparado para listar los movimientos agrupados próximamente
        }