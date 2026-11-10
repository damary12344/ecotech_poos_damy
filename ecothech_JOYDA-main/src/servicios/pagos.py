from servicios.permisos import exigir_admin
from servicios.indicadores import consultar_moneda
from servicios.api_dolar import ErrorApi
from persistencia.empleados_dao import EmpleadoDAO


def calcular_pago(sesion, id_empleado, moneda):
    exigir_admin(sesion)
    if type(id_empleado) is not int or id_empleado <= 0:
        raise ValueError("El ID del empleado no es válido.")
    empleado = EmpleadoDAO.buscar_por_id(id_empleado)
    if empleado is None:
        raise ValueError("No existe ese empleado.")
    resultado = consultar_moneda(sesion, moneda)
    dato = resultado["dato"]
    if dato is None:
        raise ErrorApi("No hay un tipo de cambio disponible en este momento.")
    salario = float(empleado[6])
    return {"empleado": empleado[1], "salario": salario,
            "tipo_cambio": dato.valor, "unidad": dato.unidad,
            "fecha": dato.fecha, "origen": resultado["origen"],
            "equivalente": salario / dato.valor}