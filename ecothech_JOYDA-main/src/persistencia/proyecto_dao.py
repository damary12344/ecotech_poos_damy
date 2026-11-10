from .consultas import consultar, ejecutar


class ProyectoDAO:
    @staticmethod
    def insertar(nombre, descripcion, id_departamento):
        ok = ejecutar(
            "INSERT INTO proyecto (nombre, descripcion, id_departamento) "
            "VALUES (%s, %s, %s)", (nombre, descripcion, id_departamento))
        if ok:
            print("Proyecto registrado exitosamente.")
        return ok

    @staticmethod
    def listar():
        return consultar(
            "SELECT p.id_proyecto, p.nombre, p.descripcion, d.nombre "
            "FROM proyecto p "
            "LEFT JOIN departamento d ON p.id_departamento = d.id_departamento "
            "ORDER BY p.id_proyecto")

    @staticmethod
    def buscar_por_id(id_proy):
        filas = consultar(
            "SELECT id_proyecto, nombre, descripcion, id_departamento "
            "FROM proyecto WHERE id_proyecto = %s", (id_proy,))
        return filas[0] if filas else None

    @staticmethod
    def eliminar(id_proy):
        ejecutar("DELETE FROM asignacion_proyecto WHERE id_proyecto = %s", (id_proy,))
        ok = ejecutar("DELETE FROM proyecto WHERE id_proyecto = %s", (id_proy,))
        if ok:
            print("Proyecto eliminado.")
        return ok