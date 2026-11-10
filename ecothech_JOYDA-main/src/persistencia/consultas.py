import mysql.connector
from .conexion import abrir_conexion


def consultar(sql, params=()):
    conexion = abrir_conexion()
    if not conexion:
        return []
    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()
    except mysql.connector.Error:
        print("\nError al consultar la base de datos.")
        return []
    finally:
        if cursor:
            cursor.close()
        if conexion.is_connected():
            conexion.close()


def ejecutar(sql, params=()):
    conexion = abrir_conexion()
    if not conexion:
        return False
    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute(sql, params)
        conexion.commit()
        return True
    except mysql.connector.Error:
        print("\nError al guardar en la base de datos.")
        return False
    finally:
        if cursor:
            cursor.close()
        if conexion.is_connected():
            conexion.close()