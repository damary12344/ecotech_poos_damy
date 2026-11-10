from servicios.permisos import exigir_sesion
from servicios.api_dolar import obtener_datos, extraer_primero, ErrorApi
from dominio.indicador import Indicador
from persistencia.indicador_dao import IndicadorDAO

UNIDADES = {"dolar": "CLP/USD", "euro": "CLP/EUR"}


def consultar_moneda(sesion, codigo="dolar"):
    exigir_sesion(sesion)
    if codigo not in UNIDADES:
        raise ValueError("Moneda no permitida.")
    try:
        fecha, valor = extraer_primero(obtener_datos(codigo))
        dato = Indicador(fecha, valor, codigo=codigo, unidad=UNIDADES[codigo])
    except (ErrorApi, ValueError) as error:
        respaldo = IndicadorDAO.ultimo(codigo)
        if respaldo is None:
            return {"dato": None, "origen": None,
                    "mensaje": f"{error} No hay datos de respaldo."}
        return {"dato": respaldo, "origen": "BD local (respaldo)",
                "mensaje": f"Servicio no disponible: {error}"}
    guardado = IndicadorDAO.guardar(dato)
    mensaje = ("Dato guardado en la base de datos." if guardado
            else "Aviso: no se pudo guardar el dato.")
    return {"dato": dato, "origen": "API", "mensaje": mensaje}


def consultar_dolar(sesion):
    return consultar_moneda(sesion, "dolar")


def obtener_historial(sesion, codigo="dolar"):
    exigir_sesion(sesion)
    if codigo not in UNIDADES:
        raise ValueError("Moneda no permitida.")
    return IndicadorDAO.listar(codigo)