from servicios.gestion_empleados import (
    registrar_empleado, listar_empleados, buscar_empleado,
    actualizar_empleado, eliminar_empleado,
)



def menu_empleados(sesion):
    while True:
        print("\n--- MÓDULO DE EMPLEADOS ---")
        print("1. Registrar Empleado")
        print("2. Listar Empleados")
        print("3. Buscar Empleado por ID")
        print("4. Actualizar Empleado")
        print("5. Eliminar Empleado")
        print("6. Volver al Menú Principal")
        
        opcion = input("Seleccione una opción (1-6): ").strip()
        
        if opcion == "1":
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
            try:
                salario = float(input("Salario: "))
                if salario <= 0:
                    print(" El salario debe ser mayor a 0.")
                    continue
            except ValueError:
                print(" Error: El salario debe ser numérico.")
                continue
            registrar_empleado(sesion,nombre, direccion, telefono, correo, fecha_inicio, salario)

        elif opcion == "2":
            empleados = listar_empleados(sesion)
            if empleados:
                for emp in empleados:
                    print(f"ID: {emp[0]} | Nombre: {emp[1]} | Correo: {emp[2]} | Salario: ${emp[4]:.2f}")
            else:
                print("No hay empleados registrados.")

        elif opcion == "3":
            try:
                id_emp = int(input("Ingrese el ID del empleado: "))
                emp = buscar_empleado(sesion,id_emp)
                if emp:
                    print(f"\nID: {emp[0]}\nNombre: {emp[1]}\nDirección: {emp[2]}\nTeléfono: {emp[3]}\nCorreo: {emp[4]}\nFecha: {emp[5]}\nSalario: ${emp[6]:.2f}")
                else:
                    print(f"No se encontró empleado con ID {id_emp}.")
            except ValueError:
                print(" Error: ID inválido.")

        elif opcion == "4":
            try:
                id_emp = int(input("Ingrese ID del empleado a actualizar: "))
                nueva_dir = input("Nueva Dirección: ").strip()
                nuevo_tel = input("Nuevo Teléfono: ").strip()
                nuevo_sal = float(input("Nuevo Salario: "))
                actualizar_empleado(sesion,id_emp, nueva_dir, nuevo_tel, nuevo_sal)
            except ValueError:
                print(" Error en los datos ingresados.")

        elif opcion == "5":
            try:
                id_emp = int(input("Ingrese ID del empleado a eliminar: "))
                eliminar_empleado(sesion,id_emp)
            except ValueError:
                print(" Error: ID inválido.")

        elif opcion == "6":
            break
        else:
            print(" Opción no válida.")
