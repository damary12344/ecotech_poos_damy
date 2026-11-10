from datetime import datetime

from servicios.permisos import exigir_sesion, exigir_admin
from persistencia.asignacion_dao import AsignacionDAO
from persistencia.empleados_dao import EmpleadoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO


def mis_proyectos(sesion):
    exigir_sesion(sesion)
    return AsignacionDAO.proyectos_de(sesion["empleado_id"])


def mis_registros(sesion):
    exigir_sesion(sesion)
    return RegistroTiempoDAO.listar_por_empleado(sesion["empleado_id"])


def registrar_horas(sesion, id_proyecto, horas, fecha, descripcion=""):
    exigir_sesion(sesion)
    if type(id_proyecto) is not int or id_proyecto <= 0:
        raise ValueError("El ID del proyecto no es válido.")
    if not isinstance(horas, (int, float)) or not 0 < horas <= 24:
        raise ValueError("Las horas deben estar entre 0 y 24.")
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
    except (TypeError, ValueError):
        raise ValueError("La fecha debe tener el formato YYYY-MM-DD.")
    descripcion = descripcion.strip()[:200] if isinstance(descripcion, str) else ""
    if not AsignacionDAO.esta_asignado(sesion["empleado_id"], id_proyecto):
        raise PermissionError("Ese proyecto no está asignado a tu cuenta.")
    return RegistroTiempoDAO.insertar(
        sesion["empleado_id"], id_proyecto, horas, fecha, descripcion)


def listar_proyectos(sesion):
    exigir_admin(sesion)
    return AsignacionDAO.listar_proyectos()


def asignar_empleado(sesion, id_empleado, id_proyecto):
    exigir_admin(sesion)
    if EmpleadoDAO.buscar_por_id(id_empleado) is None:
        raise ValueError("No existe ese empleado.")
    if not AsignacionDAO.existe_proyecto(id_proyecto):
        raise ValueError("No existe ese proyecto.")
    return AsignacionDAO.asignar(id_empleado, id_proyecto)