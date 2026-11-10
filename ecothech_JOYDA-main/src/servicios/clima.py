import requests

from servicios.permisos import exigir_sesion
from servicios.api_dolar import ErrorApi

URL_CLIMA = "https://api.open-meteo.com/v1/forecast"
TIMEOUT_SEGUNDOS = 15

CIUDADES = {
    "1": ("Santiago", -33.45, -70.67),
    "2": ("Valparaíso", -33.05, -71.62),
    "3": ("Concepción", -36.83, -73.05),
}

CONDICIONES = {
    0: "Despejado", 1: "Mayormente despejado", 2: "Parcialmente nublado",
    3: "Nublado", 45: "Niebla", 48: "Niebla", 51: "Llovizna ligera",
    53: "Llovizna", 55: "Llovizna intensa", 61: "Lluvia ligera",
    63: "Lluvia", 65: "Lluvia fuerte", 80: "Chubascos ligeros",
    81: "Chubascos", 82: "Chubascos fuertes", 95: "Tormenta",
}


def consultar_clima(sesion, opcion):
    exigir_sesion(sesion)
    ciudad = CIUDADES.get(opcion)
    if ciudad is None:
        raise ValueError("Ciudad no disponible.")
    nombre, latitud, longitud = ciudad
    params = {"latitude": latitud, "longitude": longitud,"current": "temperature_2m,relative_humidity_2m,""weather_code,wind_speed_10m"}
    try:
        respuesta = requests.get(URL_CLIMA, params=params,timeout=TIMEOUT_SEGUNDOS)
    except requests.exceptions.Timeout:
        raise ErrorApi("El servicio del clima tardó demasiado en responder.")
    except requests.exceptions.RequestException:
        raise ErrorApi("No se pudo conectar con el servicio del clima.")
    if respuesta.status_code == 404:
        raise ErrorApi("El servicio del clima no encontró los datos.")
    if respuesta.status_code >= 500:
        raise ErrorApi("El servicio del clima presenta problemas. " "Intente más tarde.")
    if respuesta.status_code != 200:
        raise ErrorApi(f"El servicio del clima respondió con error "f"({respuesta.status_code}).")
    try:
        actual = respuesta.json()["current"]
        temperatura = float(actual["temperature_2m"])
        humedad = float(actual["relative_humidity_2m"])
        viento = float(actual["wind_speed_10m"])
        codigo = int(actual["weather_code"])
        hora = str(actual["time"])
    except (ValueError, KeyError, TypeError):
        raise ErrorApi("El servicio del clima entregó una respuesta inválida.")
    if not -80 <= temperatura <= 60 or not 0 <= humedad <= 100:
        raise ErrorApi("El servicio del clima entregó un valor no válido.")
    return {"ciudad": nombre, "temperatura": temperatura,
            "humedad": humedad, "viento": viento,
            "condicion": CONDICIONES.get(codigo, "Condición no clasificada"),
            "hora": hora}