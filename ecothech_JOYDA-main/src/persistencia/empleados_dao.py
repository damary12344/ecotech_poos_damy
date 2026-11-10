from .consultas import consultar, ejecutar


class EmpleadoDAO:
    @staticmethod
    def insertar_empleado(nombre, direccion, telefono, correo, fecha_inicio, salario):
        ok = ejecutar(
            "INSERT INTO empleado (nombre, direccion, telefono, correo, "
            "fecha_inicio, salario) VALUES (%s, %s, %s, %s, %s, %s)",
            (nombre, direccion, telefono, correo, fecha_inicio, salario))
        if ok:
            print(f"\n¡Empleado '{nombre}' registrado exitosamente!")
        return ok

    @staticmethod
    def listar_empleados():
        return consultar(
            "SELECT id_empleado, nombre, correo, telefono, salario "
            "FROM empleado ORDER BY id_empleado")

    @staticmethod
    def buscar_por_id(id_empleado):
        filas = consultar(
            "SELECT id_empleado, nombre, direccion, telefono, correo, "
            "fecha_inicio, salario FROM empleado WHERE id_empleado = %s",
            (id_empleado,))
        return filas[0] if filas else None

    @staticmethod
    def actualizar_empleado(id_empleado, direccion, telefono, salario):
        if EmpleadoDAO.buscar_por_id(id_empleado) is None:
            print(f"\nNo se encontró el empleado con ID {id_empleado}.")
            return False
        ok = ejecutar(
            "UPDATE empleado SET direccion = %s, telefono = %s, salario = %s "
            "WHERE id_empleado = %s",
            (direccion, telefono, salario, id_empleado))
        if ok:
            print(f"\nEmpleado ID {id_empleado} actualizado con éxito.")
        return ok

    @staticmethod
    def actualizar_perfil(id_empleado, nombre, correo):
        return ejecutar(
            "UPDATE empleado SET nombre = %s, correo = %s "
            "WHERE id_empleado = %s", (nombre, correo, id_empleado))

    @staticmethod
    def eliminar_empleado(id_empleado):
        if EmpleadoDAO.buscar_por_id(id_empleado) is None:
            print(f"\nNo existe un empleado con ID {id_empleado}.")
            return False
        if (consultar("SELECT 1 FROM usuarios WHERE empleado_id = %s", (id_empleado,))
                or consultar("SELECT 1 FROM registro_tiempo " "WHERE id_empleado = %s", (id_empleado,))):
            print("\nNo se puede eliminar: tiene una cuenta o registros " "de tiempo asociados.")
            return False
        ejecutar("DELETE FROM asignacion_proyecto WHERE id_empleado = %s",(id_empleado,))
        ejecutar("UPDATE departamento SET gerente_id = NULL " "WHERE gerente_id = %s", (id_empleado,))
        ok = ejecutar("DELETE FROM empleado WHERE id_empleado = %s", (id_empleado,))
        if ok:
            print(f"\nEmpleado ID {id_empleado} eliminado con éxito.")
        return ok