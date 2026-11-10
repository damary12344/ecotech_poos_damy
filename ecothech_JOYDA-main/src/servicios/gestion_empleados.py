from servicios.permisos import exigir_admin
from persistencia.empleados_dao import EmpleadoDAO


def registrar_empleado(sesion, nombre, direccion, telefono, correo, fecha_inicio, salario):
    exigir_admin(sesion)
    return EmpleadoDAO.insertar_empleado(nombre, direccion, telefono, correo, fecha_inicio, salario)


def listar_empleados(sesion):
    exigir_admin(sesion)
    return EmpleadoDAO.listar_empleados()


def buscar_empleado(sesion, id_empleado):
    exigir_admin(sesion)
    return EmpleadoDAO.buscar_por_id(id_empleado)


def actualizar_empleado(sesion, id_empleado, direccion, telefono, salario):
    exigir_admin(sesion)
    return EmpleadoDAO.actualizar_empleado(id_empleado, direccion, telefono, salario)


def eliminar_empleado(sesion, id_empleado):
    exigir_admin(sesion)
    return EmpleadoDAO.eliminar_empleado(id_empleado)