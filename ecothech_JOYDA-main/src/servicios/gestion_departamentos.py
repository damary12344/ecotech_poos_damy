from servicios.permisos import exigir_admin
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleados_dao import EmpleadoDAO


def listar_departamentos(sesion):
    exigir_admin(sesion)
    return DepartamentoDAO.listar_con_gerente()


def asignar_gerente(sesion, id_departamento, id_empleado):
    exigir_admin(sesion)
    if DepartamentoDAO.buscar_por_id(id_departamento) is None:
        raise ValueError("No existe ese departamento.")
    if EmpleadoDAO.buscar_por_id(id_empleado) is None:
        raise ValueError("No existe ese empleado.")
    return DepartamentoDAO.asignar_gerente(id_departamento, id_empleado)