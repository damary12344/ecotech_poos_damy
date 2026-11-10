
from persistencia.proyecto_dao import ProyectoDAO



def menu_proyectos():
    while True:
        print("\n--- MÓDULO DE PROYECTOS ---")
        print("1. Registrar Proyecto")
        print("2. Listar Proyectos")
        print("3. Eliminar Proyecto")
        print("4. Volver al Menú Principal")
        
        opcion = input("Seleccione una opción (1-4): ").strip()
        
        if opcion == "1":
            nombre = input("Nombre del Proyecto: ").strip()
            descripcion = input("Descripción: ").strip()
            try:
                id_dep = int(input("ID del Departamento responsable: "))
                ProyectoDAO.insertar(nombre, descripcion, id_dep)
            except ValueError:
                print(" ID de departamento inválido.")
        elif opcion == "2":
            proys = ProyectoDAO.listar()
            for p in proys:
                print(f"ID: {p[0]} | Proyecto: {p[1]} | Desc: {p[2]} | Depto: {p[3]}")
        elif opcion == "3":
            try:
                id_proy = int(input("ID del proyecto a eliminar: "))
                ProyectoDAO.eliminar(id_proy)
            except ValueError:
                print(" ID inválido.")
        elif opcion == "4":
            break
