from servicios.permisos import exigir_sesion
from persistencia.empleados_dao import EmpleadoDAO


def ver_mi_ficha(sesion):
    exigir_sesion(sesion)
    return EmpleadoDAO.buscar_por_id(sesion["empleado_id"])


def actualizar_mis_datos(sesion, nombre, correo):
    exigir_sesion(sesion)
    nombre = nombre.strip() if isinstance(nombre, str) else ""
    correo = correo.strip() if isinstance(correo, str) else ""
    if not nombre:
        raise ValueError("El nombre no puede estar vacío.")
    if "@" not in correo or " " in correo:
        raise ValueError("Ingrese un correo electrónico válido.")
    if EmpleadoDAO.buscar_por_id(sesion["empleado_id"]) is None:
        raise ValueError("Empleado no encontrado.")
    return EmpleadoDAO.actualizar_perfil(sesion["empleado_id"], nombre, correo)