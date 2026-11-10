import mysql.connector
from .conexion import abrir_conexion
from dominio.indicador import Indicador

SQL_GUARDAR = """
    INSERT INTO indicador_api
        (fuente, codigo, fecha, valor, unidad, verificado_en)
    VALUES (%s, %s, %s, %s, %s, NOW())
    ON DUPLICATE KEY UPDATE
        valor = VALUES(valor),
        unidad = VALUES(unidad),
        verificado_en = NOW()
"""
SQL_SELECT = ("SELECT fuente, codigo, fecha, valor, unidad, verificado_en ""FROM indicador_api WHERE codigo = %s ORDER BY fecha DESC")


def _a_objeto(f):
    return Indicador(str(f[2]), f[3], verificado_en=f[5], fuente=f[0], codigo=f[1], unidad=f[4])


class IndicadorDAO:
    @staticmethod
    def guardar(ind):
        conexion = abrir_conexion()
        if not conexion:
            return False
        try:
            cursor = conexion.cursor()
            cursor.execute(SQL_GUARDAR, (ind.fuente, ind.codigo, ind.fecha, ind.valor, ind.unidad))
            conexion.commit()
            return True
        except mysql.connector.Error:
            print("\nError al guardar el indicador.")
            return False
        finally:
            if conexion and conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def listar(codigo="dolar"):
        conexion = abrir_conexion()
        if not conexion:
            return []
        try:
            cursor = conexion.cursor()
            cursor.execute(SQL_SELECT, (codigo,))
            return [_a_objeto(f) for f in cursor.fetchall()]
        except mysql.connector.Error:
            print("\nError al leer el historial.")
            return []
        finally:
            if conexion and conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def ultimo(codigo="dolar"):
        datos = IndicadorDAO.listar(codigo)
        return datos[0] if datos else None