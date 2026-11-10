import math
from datetime import datetime

import requests

URL_BASE = "https://mindicador.cl/api/"
MONEDAS_PERMITIDAS = ("dolar", "euro")
TIMEOUT_SEGUNDOS = 15


class ErrorApi(Exception):
    pass


def obtener_datos(codigo="dolar"):
    if codigo not in MONEDAS_PERMITIDAS:
        raise ValueError("Moneda no permitida.")
    try:
        respuesta = requests.get(URL_BASE + codigo, timeout=TIMEOUT_SEGUNDOS)
    except requests.exceptions.Timeout:
        raise ErrorApi("El servicio tardó demasiado en responder.")
    except requests.exceptions.RequestException:
        raise ErrorApi("No se pudo conectar con el servicio.")

    if respuesta.status_code == 404:
        raise ErrorApi("El servicio no encontró el indicador solicitado.")
    if respuesta.status_code >= 500:
        raise ErrorApi("El servicio externo presenta problemas. " "Intente más tarde.")
    if respuesta.status_code != 200:
        raise ErrorApi(f"El servicio respondió con un estado inesperado "f"({respuesta.status_code}).")
    try:
        return respuesta.json()
    except ValueError:
        raise ErrorApi("El servicio entregó una respuesta inválida.")


def extraer_primero(datos):
    try:
        primero = datos["serie"][0]
        fecha = str(primero["fecha"])[:10]
        valor = float(primero["valor"])
        datetime.strptime(fecha, "%Y-%m-%d")
    except (KeyError, IndexError, TypeError, ValueError):
        raise ValueError("La respuesta de la API no tiene el formato esperado.")
    if not math.isfinite(valor) or valor <= 0:
        raise ValueError("El valor recibido no es válido.")
    return fecha, valor