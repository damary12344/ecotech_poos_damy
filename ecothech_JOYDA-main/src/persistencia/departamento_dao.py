from .consultas import consultar, ejecutar


class DepartamentoDAO:
    @staticmethod
    def insertar(nombre, ubicacion):
        ok = ejecutar(
            "INSERT INTO departamento (nombre, ubicacion) VALUES (%s, %s)",
            (nombre, ubicacion))
        if ok:
            print("Departamento registrado exitosamente.")
        return ok

    @staticmethod
    def listar():
        return consultar(
            "SELECT id_departamento, nombre, ubicacion FROM departamento "
            "ORDER BY id_departamento")

    @staticmethod
    def buscar_por_id(id_dep):
        filas = consultar(
            "SELECT id_departamento, nombre, ubicacion FROM departamento "
            "WHERE id_departamento = %s", (id_dep,))
        return filas[0] if filas else None

    @staticmethod
    def actualizar(id_dep, nuevo_nombre, nueva_ubicacion):
        ok = ejecutar(
            "UPDATE departamento SET nombre = %s, ubicacion = %s "
            "WHERE id_departamento = %s",
            (nuevo_nombre, nueva_ubicacion, id_dep))
        if ok:
            print("Departamento actualizado con éxito.")
        return ok

    @staticmethod
    def eliminar(id_dep):
        ejecutar("UPDATE proyecto SET id_departamento = NULL " "WHERE id_departamento = %s", (id_dep,))
        ok = ejecutar("DELETE FROM departamento WHERE id_departamento = %s", (id_dep,))
        if ok:
            print("Departamento eliminado.")
        return ok

    @staticmethod
    def asignar_gerente(id_dep, id_empleado):
        return ejecutar(
            "UPDATE departamento SET gerente_id = %s WHERE id_departamento = %s",
            (id_empleado, id_dep))

    @staticmethod
    def listar_con_gerente():
        return consultar(
            "SELECT d.id_departamento, d.nombre, e.nombre "
            "FROM departamento d "
            "LEFT JOIN empleado e ON d.gerente_id = e.id_empleado "
            "ORDER BY d.id_departamento")