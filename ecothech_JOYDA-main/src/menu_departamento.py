from persistencia.departamento_dao import DepartamentoDAO



def menu_departamentos():
    while True:
        print("\n--- MÓDULO DE DEPARTAMENTOS ---")
        print("1. Registrar Departamento")
        print("2. Listar Departamentos")
        print("3. Eliminar Departamento")
        print("4. Volver al Menú Principal")
        
        opcion = input("Seleccione una opción (1-4): ").strip()
        
        if opcion == "1":
            nombre = input("Nombre del Departamento: ").strip()
            ubicacion = input("Ubicación: ").strip()
            if nombre:
                DepartamentoDAO.insertar(nombre, ubicacion)
            else:
                print(" El nombre no puede estar vacío.")
        elif opcion == "2":
            deps = DepartamentoDAO.listar()
            for d in deps:
                print(f"ID: {d[0]} | Nombre: {d[1]} | Ubicación: {d[2]}")
        elif opcion == "3":
            try:
                id_dep = int(input("ID del departamento a eliminar: "))
                DepartamentoDAO.eliminar(id_dep)
            except ValueError:
                print(" ID inválido.")
        elif opcion == "4":
            break