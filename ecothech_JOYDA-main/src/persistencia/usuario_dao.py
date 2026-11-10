import mysql.connector
from .conexion import abrir_conexion
from .consultas import ejecutar
from dominio.usuario import Usuario

COLUMNAS = "id, nombre_usuario, password_hash, empleado_id, rol"


def _buscar(sql, parametro):
    conexion = abrir_conexion()
    if not conexion:
        return None
    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute(sql, (parametro,))
        fila = cursor.fetchone()
        if fila is None:
            return None
        return Usuario(fila[1], fila[2], fila[3], id=fila[0], rol=fila[4])
    except (mysql.connector.Error, ValueError, TypeError):
        print("\nError al consultar usuarios.")
        return None
    finally:
        if cursor:
            cursor.close()
        if conexion.is_connected():
            conexion.close()


class UsuarioDAO:
    @staticmethod
    def buscar_por_nombre(nombre):
        return _buscar(f"SELECT {COLUMNAS} FROM usuarios " "WHERE nombre_usuario = %s", nombre)

    @staticmethod
    def buscar_por_empleado(empleado_id):
        return _buscar(f"SELECT {COLUMNAS} FROM usuarios " "WHERE empleado_id = %s", empleado_id)

    @staticmethod
    def insertar(usuario):
        sql = ("INSERT INTO usuarios " "(nombre_usuario, password_hash, empleado_id, rol) " "VALUES (%s, %s, %s, %s)")
        conexion = abrir_conexion()
        if not conexion:
            return None
        cursor = None
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (usuario.nombre_usuario, usuario.password_hash, usuario.empleado_id, usuario.rol))
            conexion.commit()
            return cursor.lastrowid
        except mysql.connector.Error:
            print("\nError al guardar la cuenta.")
            return None
        finally:
            if cursor:
                cursor.close()
            if conexion.is_connected():
                conexion.close()

    @staticmethod
    def asignar_rol(id_usuario, rol):
        rol = Usuario.validar_rol(rol)
        return ejecutar("UPDATE usuarios SET rol = %s WHERE id = %s",
                        (rol, id_usuario))