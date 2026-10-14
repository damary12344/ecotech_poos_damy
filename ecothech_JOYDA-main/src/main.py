import sys
import os

# Asegura que el directorio raíz 'src' esté en el path de importaciones
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from persistencia.crear_bd import crear_tablas
from persistencia.empleados_dao import EmpleadoDAO

def mostrar_menu():
    print("\n" + "="*45)
    print(" SISTEMA DE GESTIÓN - ECOTECH SOLUTIONS")
    print("="*45)
    print("1. Registrar Empleado")
    print("2. Listar Empleados")
    print("3. Buscar Empleado por ID")
    print("4. Actualizar Empleado")
    print("5. Eliminar Empleado")
    print("6. Salir")
    print("="*45)

def main():
    # Inicializa y verifica la estructura de la base de datos al arrancar
    try:
        crear_tablas()
    except Exception as e:
        print(f"Error al inicializar la base de datos: {e}")

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-6): ").strip()

        if opcion == "1":
            print("\n--- Registrar Nuevo Empleado ---")
            nombre = input("Nombre completo: ").strip()
            if not nombre:
                print(" El nombre no puede estar vacío.")
                continue

            direccion = input("Dirección: ").strip()
            telefono = input("Teléfono: ").strip()
            correo = input("Correo electrónico: ").strip()
            if "@" not in correo:
                print(" Ingrese un correo electrónico válido.")
                continue

            fecha_inicio = input("Fecha de inicio (YYYY-MM-DD): ").strip()
            
            # Control de Excepciones para Entrada Numérica (Criterio 2.1.4)
            try:
                salario = float(input("Salario: "))
                if salario <= 0:
                    print(" El salario debe ser un número positivo mayor a 0.")
                    continue
            except ValueError:
                print(" Error de Entrada: El salario debe ser un valor numérico.")
                continue

            # Inserción mediante DAO
            EmpleadoDAO.insertar_empleado(nombre, direccion, telefono, correo, fecha_inicio, salario)

        elif opcion == "2":
            print("\n--- Listado de Empleados ---")
            empleados = EmpleadoDAO.listar_empleados()
            if empleados:
                for emp in empleados:
                    print(f"ID: {emp[0]} | Nombre: {emp[1]} | Correo: {emp[2]} | Teléfono: {emp[3]} | Salario: ${emp[4]:.2f}")
            else:
                print("No hay empleados registrados en la base de datos.")

        elif opcion == "3":
            print("\n--- Buscar Empleado ---")
            try:
                id_emp = int(input("Ingrese el ID del empleado: "))
                emp = EmpleadoDAO.buscar_por_id(id_emp)
                if emp:
                    print(f"\nID: {emp[0]}\nNombre: {emp[1]}\nDirección: {emp[2]}\nTeléfono: {emp[3]}\nCorreo: {emp[4]}\nFecha Inicio: {emp[5]}\nSalario: ${emp[6]:.2f}")
                else:
                    print(f"No se encontró un empleado con ID {id_emp}.")
            except ValueError:
                print(" Error: Debe ingresar un ID numérico válido.")

        elif opcion == "4":
            print("\n--- Actualizar Datos de Empleado ---")
            try:
                id_emp = int(input("Ingrese ID del empleado a actualizar: "))
                nueva_direccion = input("Nueva Dirección: ").strip()
                nuevo_telefono = input("Nuevo Teléfono: ").strip()
                nuevo_salario = float(input("Nuevo Salario: "))
                EmpleadoDAO.actualizar_empleado(id_emp, nueva_direccion, nuevo_telefono, nuevo_salario)
            except ValueError:
                print(" Error: Ingrese valores válidos para el ID y Salario.")

        elif opcion == "5":
            print("\n--- Eliminar Empleado ---")
            try:
                id_emp = int(input("Ingrese el ID del empleado a eliminar: "))
                EmpleadoDAO.eliminar_empleado(id_emp)
            except ValueError:
                print(" Error: El ID debe ser un número entero.")

        elif opcion == "6":
            print("\nSaliendo del sistema EcoTech Solutions...")
            break
        else:
            print(" Opción no válida. Por favor, seleccione un número del 1 al 6.")

if __name__ == "__main__":
    main()