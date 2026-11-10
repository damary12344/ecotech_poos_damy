import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from servicios.permisos import exigir_admin
from utilidades import limpiar_pantalla, pausar
from menu_empleados import menu_empleados
from menu_departamento import menu_departamentos
from menu_proyecto import menu_proyectos
from menu_registro_tiempo import menu_registro_tiempo
from menu_usuario import (solicitar_login, solicitar_registro,mostrar_perfil, consultar_indicador)
from menu_trabajo import (ver_mis_proyectos, registrar_mis_horas,ver_mis_registros, menu_asignaciones)


def _solo_admin(sesion, funcion):
    exigir_admin(sesion)
    funcion()


def _ciclo(usuario, titulos, acciones, con_pausa=()):
    while True:
        limpiar_pantalla()
        print("=" * 45)
        print(" SISTEMA DE GESTIÓN - ECOTECH SOLUTIONS")
        print(f" Sesión: {usuario['nombre_usuario']} ({usuario['rol']})")
        print("=" * 45)
        for titulo in titulos:
            print(titulo)
        print("9. Cerrar sesión")
        print("0. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion in ("0", "9"):
            return opcion
        accion = acciones.get(opcion)
        if accion is None:
            print("Opción no válida.")
            pausar()
            continue
        limpiar_pantalla()
        try:
            accion()
        except PermissionError as error:
            print(error)
            pausar()
            continue
        if opcion in con_pausa:
            pausar()


def menu_admin(u):
    titulos = ["1. Gestión de Empleados", "2. Gestión de Departamentos","3. Gestión de Proyectos", "4. Gestión de Registro de Tiempos","5. Registrar cuenta de usuario", "6. Mi perfil", "7. Consultar API (dólar / clima)", "8. Asignaciones (proyectos y gerentes)"]
    acciones = {
        "1": lambda: menu_empleados(u),
        "2": lambda: _solo_admin(u, menu_departamentos),
        "3": lambda: _solo_admin(u, menu_proyectos),
        "4": lambda: _solo_admin(u, menu_registro_tiempo),
        "5": lambda: solicitar_registro(u),
        "6": lambda: mostrar_perfil(u),
        "7": lambda: consultar_indicador(u),
        "8": lambda: menu_asignaciones(u),
    }
    return _ciclo(u, titulos, acciones, con_pausa=("5",))


def menu_empleado(u):
    titulos = ["1. Mi perfil", "2. Mis proyectos", "3. Registrar mis horas", "4. Mis registros de tiempo", "5. Consultar API (dólar / clima)"]
    acciones = {
        "1": lambda: mostrar_perfil(u),
        "2": lambda: ver_mis_proyectos(u),
        "3": lambda: registrar_mis_horas(u),
        "4": lambda: ver_mis_registros(u),
        "5": lambda: consultar_indicador(u),
    }
    return _ciclo(u, titulos, acciones, con_pausa=("2", "3", "4"))


def main():
    while True:
        limpiar_pantalla()
        usuario_actual = solicitar_login()
        if usuario_actual is None:
            if input("Enter para reintentar o 0 para salir: ").strip() == "0":
                return
            continue
        if usuario_actual["rol"] == "admin":
            opcion = menu_admin(usuario_actual)
        else:
            opcion = menu_empleado(usuario_actual)
        usuario_actual = None
        if opcion == "0":
            print("\nSaliendo del sistema EcoTech Solutions...")
            return
        print("Sesión cerrada. Ingrese nuevamente.")
        pausar()


if __name__ == "__main__":
    main()