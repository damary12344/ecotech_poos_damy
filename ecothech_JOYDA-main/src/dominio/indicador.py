import math
from datetime import datetime


class Indicador:
    def __init__(self, fecha, valor, verificado_en=None,fuente="mindicador", codigo="dolar", unidad="CLP/USD"):
        datetime.strptime(str(fecha), "%Y-%m-%d")
        valor = float(valor)
        if not math.isfinite(valor) or valor <= 0:
            raise ValueError("El valor del indicador no es válido.")
        self.fecha = str(fecha)
        self.valor = valor
        self.verificado_en = verificado_en
        self.fuente = fuente
        self.codigo = codigo
        self.unidad = unidad