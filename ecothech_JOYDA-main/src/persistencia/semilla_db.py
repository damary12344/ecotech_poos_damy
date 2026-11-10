import getpass

from persistencia.consultas import consultar
from persistencia.empleados_dao import EmpleadoDAO
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.asignacion_dao import AsignacionDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO
from persistencia.usuario_dao import UsuarioDAO
from servicios.autenticacion import registrar_usuario

DEPARTAMENTOS = [("Tecnología e Innovación", "Piso 3"),("Recursos Humanos", "Piso 1"),("Finanzas y Contabilidad", "Piso 2")]

EMPLEADOS = [
    ("Valeria Soto", "Av. Central 100", "555-1111", "valeria.soto@ecotech.com", "2023-01-01", 5500.0),
    ("Andrés Morales", "Calle Los Pinos 40", "555-2222", "andres.morales@ecotech.com", "2023-02-15", 5200.0),
    ("Carlos Rivas", "Calle Norte 45", "555-3333", "carlos.rivas@ecotech.com", "2023-03-10", 3000.0),
    ("Lucía Méndez", "Pasaje Sol 12", "555-4444", "lucia.mendez@ecotech.com", "2023-04-20", 3200.0),
]

PROYECTOS = [
    ("EcoPlataforma", "Sistema de monitoreo ambiental corporativo", "Tecnología e Innovación"),
    ("Portal de Reclutamiento", "Automatización de selección de personal", "Recursos Humanos"),
    ("Auditoría Fiscal 2026", "Revisión de estados financieros", "Finanzas y Contabilidad"),
]

ASIGNACIONES = [("carlos.rivas@ecotech.com", "EcoPlataforma"),
                ("carlos.rivas@ecotech.com", "Portal de Reclutamiento"),
                ("lucia.mendez@ecotech.com", "EcoPlataforma")]

CUENTAS = [("admin", "valeria.soto@ecotech.com", "admin"),("carlos_rivas", "carlos.rivas@ecotech.com", "empleado"),("lucia_mendez", "lucia.mendez@ecotech.com", "empleado")]


def _id(sql, valor):
    filas = consultar(sql, (valor,))
    return filas[0][0] if filas else None


def _id_empleado(correo):
    return _id("SELECT id_empleado FROM empleado WHERE correo = %s", correo)


def _id_proyecto(nombre):
    return _id("SELECT id_proyecto FROM proyecto WHERE nombre = %s", nombre)


def _id_departamento(nombre):
    return _id("SELECT id_departamento FROM departamento WHERE nombre = %s", nombre)


def ejecutar_semilla():
    print("--- SEMILLA (puede ejecutarse varias veces) ---")

    for nombre, ubicacion in DEPARTAMENTOS:
        if _id_departamento(nombre) is None:
            DepartamentoDAO.insertar(nombre, ubicacion)

    for datos in EMPLEADOS:
        if _id_empleado(datos[3]) is None:
            EmpleadoDAO.insertar_empleado(*datos)

    for nombre, descripcion, departamento in PROYECTOS:
        if _id_proyecto(nombre) is None:
            ProyectoDAO.insertar(nombre, descripcion, _id_departamento(departamento))

    for correo, proyecto in ASIGNACIONES:
        id_emp, id_proy = _id_empleado(correo), _id_proyecto(proyecto)
        if id_emp and id_proy:
            AsignacionDAO.asignar(id_emp, id_proy)

    if not consultar("SELECT 1 FROM registro_tiempo LIMIT 1"):
        id_carlos = _id_empleado("carlos.rivas@ecotech.com")
        id_lucia = _id_empleado("lucia.mendez@ecotech.com")
        id_eco = _id_proyecto("EcoPlataforma")
        if id_carlos and id_lucia and id_eco:
            RegistroTiempoDAO.insertar(id_carlos, id_eco, 8.0, "2026-10-20", "Desarrollo")
            RegistroTiempoDAO.insertar(id_lucia, id_eco, 7.5, "2026-10-20", "Pruebas")

    for usuario, correo, rol in CUENTAS:
        if UsuarioDAO.buscar_por_nombre(usuario) is not None:
            print(f"La cuenta {usuario} ya existe. No se modifica.")
            continue
        id_emp = _id_empleado(correo)
        if id_emp is None:
            continue
        clave = getpass.getpass(f"Contraseña para la cuenta {usuario}: ")
        try:
            id_usuario = registrar_usuario(id_emp, usuario, clave)
        except ValueError as error:
            print(error)
            continue
        if id_usuario and rol == "admin":
            UsuarioDAO.asignar_rol(id_usuario, "admin")

    print("--- SEMILLA TERMINADA ---")


if __name__ == "__main__":
    ejecutar_semilla()