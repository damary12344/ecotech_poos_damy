import mysql.connector
from mysql.connector import Error

def abrir_conexion():
    """
    Establece la conexión a la base de datos MariaDB en Wampserver.
    Se prueba el puerto 3306 primero y 3307 como respaldo (puerto habitual de MariaDB en WAMP).
    """
    puertos = [3306, 3307]
    
    for puerto in puertos:
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                port=puerto,
                user="root",
                password="",          # En WampServer la clave de root va vacía por defecto
                database="ecotech"    # Asegúrate de crear la base de datos 'ecotech' en phpMyAdmin
            )
            if conexion.is_connected():
                return conexion
        except Error:
            continue
            
    print("Error: No se pudo conectar a MariaDB en Wampserver (revisa phpMyAdmin y que el servicio esté en verde).")
    return None

def obtener_motor() -> str:
    """Retorna 'mysql' para que crear_bd.py ejecute la estructura MariaDB/MySQL."""
    return "mysql"