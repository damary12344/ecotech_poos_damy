from .consultas import consultar, ejecutar


class AsignacionDAO:
    @staticmethod
    def asignar(id_empleado, id_proyecto):
        return ejecutar(
            "INSERT IGNORE INTO asignacion_proyecto (id_empleado, id_proyecto) "
            "VALUES (%s, %s)", (id_empleado, id_proyecto))

    @staticmethod
    def proyectos_de(id_empleado):
        return consultar(
            "SELECT p.id_proyecto, p.nombre, p.descripcion FROM proyecto p "
            "JOIN asignacion_proyecto a ON a.id_proyecto = p.id_proyecto "
            "WHERE a.id_empleado = %s ORDER BY p.nombre", (id_empleado,))

    @staticmethod
    def esta_asignado(id_empleado, id_proyecto):
        return bool(consultar(
            "SELECT 1 FROM asignacion_proyecto "
            "WHERE id_empleado = %s AND id_proyecto = %s",
            (id_empleado, id_proyecto)))

    @staticmethod
    def listar_proyectos():
        return consultar("SELECT id_proyecto, nombre FROM proyecto ORDER BY id_proyecto")

    @staticmethod
    def existe_proyecto(id_proyecto):
        return bool(consultar(
            "SELECT 1 FROM proyecto WHERE id_proyecto = %s", (id_proyecto,)))