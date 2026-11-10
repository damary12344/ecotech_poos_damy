from .consultas import consultar, ejecutar

SQL_BASE = (
    "SELECT rt.id_registro, e.nombre, p.nombre, rt.horas_trabajadas, rt.fecha "
    "FROM registro_tiempo rt "
    "JOIN empleado e ON rt.id_empleado = e.id_empleado "
    "JOIN proyecto p ON rt.id_proyecto = p.id_proyecto "
)


class RegistroTiempoDAO:
    @staticmethod
    def insertar(id_empleado, id_proyecto, horas, fecha, descripcion=""):
        ok = ejecutar(
            "INSERT INTO registro_tiempo "
            "(fecha, horas_trabajadas, descripcion, id_empleado, id_proyecto) "
            "VALUES (%s, %s, %s, %s, %s)",
            (fecha, horas, descripcion, id_empleado, id_proyecto))
        if ok:
            print("Registro de tiempo guardado exitosamente.")
        return ok

    @staticmethod
    def listar():
        return consultar(SQL_BASE + "ORDER BY rt.fecha DESC")

    @staticmethod
    def listar_por_empleado(id_empleado):
        return consultar(
            "SELECT rt.id_registro, p.nombre, rt.horas_trabajadas, rt.fecha, "
            "rt.descripcion FROM registro_tiempo rt "
            "JOIN proyecto p ON rt.id_proyecto = p.id_proyecto "
            "WHERE rt.id_empleado = %s ORDER BY rt.fecha DESC", (id_empleado,))

    @staticmethod
    def eliminar(id_reg):
        ok = ejecutar("DELETE FROM registro_tiempo WHERE id_registro = %s", (id_reg,))
        if ok:
            print("Registro de tiempo eliminado.")
        return ok