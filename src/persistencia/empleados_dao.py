import mysql.connector
from .conexion import abrir_conexion

class EmpleadoDAO:
    @staticmethod
    def insertar_empleado(nombre, direccion, telefono, correo, fecha_inicio, salario):
        sql = """
            INSERT INTO empleado (nombre, direccion, telefono, correo, fecha_inicio, salario)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        conexion = abrir_conexion()
        if not conexion:
            return False
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (nombre, direccion, telefono, correo, fecha_inicio, salario))
            conexion.commit()
            print(f"\n¡Empleado '{nombre}' registrado exitosamente en Wampserver!")
            return True
        except mysql.connector.Error as e:
            print(f"\nError en MySQL/MariaDB al registrar empleado: {e}")
            return False
        finally:
            if conexion and conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def listar_empleados():
        sql = "SELECT id_empleado, nombre, correo, telefono, salario FROM empleado"
        conexion = abrir_conexion()
        if not conexion:
            return []
        try:
            cursor = conexion.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"\nError al listar empleados: {e}")
            return []
        finally:
            if conexion and conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def buscar_por_id(id_empleado):
        sql = "SELECT id_empleado, nombre, direccion, telefono, correo, fecha_inicio, salario FROM empleado WHERE id_empleado = %s"
        conexion = abrir_conexion()
        if not conexion:
            return None
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (id_empleado,))
            return cursor.fetchone()
        except mysql.connector.Error as e:
            print(f"\nError al buscar empleado: {e}")
            return None
        finally:
            if conexion and conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def actualizar_empleado(id_empleado, direccion, telefono, salario):
        sql = "UPDATE empleado SET direccion = %s, telefono = %s, salario = %s WHERE id_empleado = %s"
        conexion = abrir_conexion()
        if not conexion:
            return False
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (direccion, telefono, salario, id_empleado))
            conexion.commit()
            if cursor.rowcount > 0:
                print(f"\nEmpleado ID {id_empleado} actualizado con éxito.")
                return True
            else:
                print(f"\nNo se encontró el empleado con ID {id_empleado}.")
                return False
        except mysql.connector.Error as e:
            print(f"\nError al actualizar empleado: {e}")
            return False
        finally:
            if conexion and conexion.is_connected():
                cursor.close()
                conexion.close()

    @staticmethod
    def eliminar_empleado(id_empleado):
        sql = "DELETE FROM empleado WHERE id_empleado = %s"
        conexion = abrir_conexion()
        if not conexion:
            return False
        try:
            cursor = conexion.cursor()
            cursor.execute(sql, (id_empleado,))
            conexion.commit()
            if cursor.rowcount > 0:
                print(f"\nEmpleado ID {id_empleado} eliminado con éxito.")
                return True
            else:
                print(f"\nNo existe un empleado con ID {id_empleado}.")
                return False
        except mysql.connector.Error as e:
            print(f"\nError al eliminar empleado: {e}")
            return False
        finally:
            if conexion and conexion.is_connected():
                cursor.close()
                conexion.close()