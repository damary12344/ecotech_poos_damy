from servicios.gestion_trabajo import (
    mis_proyectos, mis_registros, registrar_horas,
    listar_proyectos, asignar_empleado,
)
from servicios.gestion_departamentos import (
    listar_departamentos, asignar_gerente,
)


def ver_mis_proyectos(sesion):
    proyectos = mis_proyectos(sesion)
    if not proyectos:
        print("\nNo tienes proyectos asignados.")
        return
    print("\n--- MIS PROYECTOS ---")
    for p in proyectos:
        print(f"ID: {p[0]} | {p[1]} | {p[2] or ''}")


def registrar_mis_horas(sesion):
    if not mis_proyectos(sesion):
        print("\nNo tienes proyectos asignados.")
        return
    ver_mis_proyectos(sesion)
    try:
        id_proyecto = int(input("ID del proyecto: "))
        horas = float(input("Horas trabajadas: "))
    except ValueError:
        print("Ingrese valores numéricos válidos.")
        return
    fecha = input("Fecha (YYYY-MM-DD): ").strip()
    descripcion = input("Descripción (opcional): ")
    try:
        registrar_horas(sesion, id_proyecto, horas, fecha, descripcion)
    except (ValueError, PermissionError) as error:
        print(error)


def ver_mis_registros(sesion):
    registros = mis_registros(sesion)
    if not registros:
        print("\nAún no tienes registros de tiempo.")
        return
    print("\n--- MIS REGISTROS DE TIEMPO ---")
    for r in registros:
        print(f"{r[3]} | {r[1]} | {r[2]}h | {r[4] or ''}")


def _asignar_a_proyecto(sesion):
    print("\n--- PROYECTOS ---")
    for p in listar_proyectos(sesion):
        print(f"ID: {p[0]} | {p[1]}")
    try:
        id_empleado = int(input("ID del empleado: "))
        id_proyecto = int(input("ID del proyecto: "))
    except ValueError:
        print("Ingrese valores numéricos válidos.")
        return
    try:
        if asignar_empleado(sesion, id_empleado, id_proyecto):
            print("Empleado asignado al proyecto.")
    except ValueError as error:
        print(error)


def _asignar_gerente(sesion):
    print("\n--- DEPARTAMENTOS ---")
    for d in listar_departamentos(sesion):
        print(f"ID: {d[0]} | {d[1]} | Gerente: {d[2] or 'sin asignar'}")
    try:
        id_dep = int(input("ID del departamento: "))
        id_emp = int(input("ID del empleado gerente: "))
    except ValueError:
        print("Ingrese valores numéricos válidos.")
        return
    try:
        if asignar_gerente(sesion, id_dep, id_emp):
            print("Gerente asignado.")
    except ValueError as error:
        print(error)


def menu_asignaciones(sesion):
    while True:
        print("\n--- ASIGNACIONES ---")
        print("1. Asignar empleado a proyecto")
        print("2. Asignar gerente a departamento")
        print("0. Volver")
        opcion = input("Opción: ").strip()
        if opcion == "0":
            return
        try:
            if opcion == "1":
                _asignar_a_proyecto(sesion)
            elif opcion == "2":
                _asignar_gerente(sesion)
            else:
                print("Opción no válida.")
        except PermissionError as error:
            print(error)
            return