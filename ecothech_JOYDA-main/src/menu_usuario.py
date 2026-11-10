from getpass import getpass

from utilidades import limpiar_pantalla, pausar
from servicios.entradas import pedir_dato
from servicios.autenticacion import registrar_usuario_admin, autenticar
from servicios.mi_cuenta import ver_mi_ficha, actualizar_mis_datos
from servicios.indicadores import consultar_moneda, obtener_historial
from servicios.api_dolar import ErrorApi
from servicios.clima import consultar_clima
from servicios.pagos import calcular_pago
from dominio.usuario import Usuario

MONEDAS = {"1": ("dolar", "Dólar", "USD"), "2": ("euro", "Euro", "EUR")}


def solicitar_registro(sesion):
    try:
        empleado_id = pedir_dato("ID del empleado: ", int)
        nombre = pedir_dato("Nuevo usuario: ", Usuario.normalizar_usuario)
        clave = pedir_dato("Contraseña: ", Usuario.validar_clave, getpass)
        if clave != getpass("Repita la contraseña: "):
            print("Las contraseñas no coinciden. Vuelva al registro.")
            return None
        usuario_id = registrar_usuario_admin(sesion, empleado_id, nombre, clave)
    except (TypeError, ValueError, PermissionError) as error:
        print(error)
        return None
    if usuario_id is None:
        print("No se pudo crear la cuenta.")
        return None
    print(f"Cuenta creada correctamente. ID: {usuario_id}")
    return usuario_id


def solicitar_login():
    nombre = input("Usuario: ")
    clave = getpass("Contraseña: ")
    try:
        usuario = autenticar(nombre, clave)
    except (TypeError, ValueError):
        print("No se pudo validar el acceso.")
        return None
    if usuario is None:
        print("Usuario o contraseña incorrectos.")
    else:
        print("Sesión iniciada correctamente.")
    return usuario


def mostrar_perfil(usuario_actual):
    while True:
        try:
            emp = ver_mi_ficha(usuario_actual)
        except PermissionError as error:
            print(error)
            return
        if emp is None:
            print("No se encontró tu ficha de empleado.")
            return
        print("\n--- MI PERFIL ---")
        print(f"Usuario: {usuario_actual['nombre_usuario']} ({usuario_actual['rol']})")
        print(f"Nombre: {emp[1]}")
        print(f"Dirección: {emp[2]}")
        print(f"Teléfono: {emp[3]}")
        print(f"Correo: {emp[4]}")
        print(f"Fecha de inicio: {emp[5]}")
        print("1. Editar nombre y correo")
        print("0. Volver")
        opcion = input("Opción: ").strip()
        if opcion == "0":
            return
        if opcion == "1":
            nombre = input("Nuevo nombre: ")
            correo = input("Nuevo correo: ")
            try:
                actualizar_mis_datos(usuario_actual, nombre, correo)
                print("Datos actualizados correctamente.")
            except (ValueError, PermissionError) as error:
                print(error)
        else:
            print("Opción no válida.")


def _pedir_moneda():
    print("\nMonedas: 1. Dólar  2. Euro")
    opcion = input("Moneda: ").strip()
    if opcion not in MONEDAS:
        raise ValueError("Moneda no válida.")
    return MONEDAS[opcion]


def _mostrar_consulta(usuario_actual):
    codigo, nombre, _ = _pedir_moneda()
    resultado = consultar_moneda(usuario_actual, codigo)
    print(f"\n{resultado['mensaje']}")
    dato = resultado["dato"]
    if dato is None:
        return
    print(f"{nombre}: {dato.valor:,.2f} {dato.unidad}")
    print(f"Fecha del dato: {dato.fecha} · Origen: {resultado['origen']}")


def _mostrar_historial(usuario_actual):
    codigo, nombre, _ = _pedir_moneda()
    datos = obtener_historial(usuario_actual, codigo)
    if not datos:
        print("\nAún no existe historial.")
        return
    print(f"\nHistorial de {nombre} (BD local):")
    for dato in datos:
        print(f"{dato.fecha}: {dato.valor:.2f} {dato.unidad}")


def _mostrar_clima(usuario_actual):
    print("\nCiudades: 1. Santiago  2. Valparaíso  3. Concepción")
    opcion = input("Ciudad: ").strip()
    datos = consultar_clima(usuario_actual, opcion)
    print(f"\nClima en {datos['ciudad']} ({datos['hora']})")
    print(f"Temperatura: {datos['temperatura']:.1f} °C")
    print(f"Humedad: {datos['humedad']:.0f} %")
    print(f"Viento: {datos['viento']:.1f} km/h")
    print(f"Condición: {datos['condicion']}")
    print("Origen: API Open-Meteo")


def _calcular_pago(usuario_actual):
    try:
        id_empleado = int(input("ID del empleado: "))
    except ValueError:
        print("Ingrese un ID numérico válido.")
        return
    codigo, _, simbolo = _pedir_moneda()
    r = calcular_pago(usuario_actual, id_empleado, codigo)
    print(f"\nEmpleado: {r['empleado']}")
    print(f"Salario: {r['salario']:,.2f} CLP")
    print(f"Tipo de cambio: {r['tipo_cambio']:,.2f} {r['unidad']} "f"(fecha {r['fecha']}, origen {r['origen']})")
    print(f"Equivalente: {r['equivalente']:,.2f} {simbolo}")


def consultar_indicador(usuario_actual):
    print("ROL DETECTADO:", repr(usuario_actual.get("rol")))
    es_admin = usuario_actual.get("rol") == "admin"
    while True:
        limpiar_pantalla()
        print("--- CONSULTAR API ---")
        print("1. Valor actual de una moneda")
        print("2. Historial de una moneda")
        print("3. Clima")
        if es_admin:
            print("4. Calcular salario en moneda extranjera")
        print("0. Volver")
        opcion = input("Opción: ").strip()
        if opcion == "0":
            return
        try:
            if opcion == "1":
                _mostrar_consulta(usuario_actual)
            elif opcion == "2":
                _mostrar_historial(usuario_actual)
            elif opcion == "3":
                _mostrar_clima(usuario_actual)
            elif opcion == "4" and es_admin:
                _calcular_pago(usuario_actual)
            else:
                print("Opción no válida.")
        except PermissionError as error:
            print(error)
            pausar()
            return
        except (ErrorApi, ValueError) as error:
            print(f"No se pudo completar la consulta: {error}")
        pausar()