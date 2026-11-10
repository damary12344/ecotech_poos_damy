
from persistencia.registro_tiempo_dao import RegistroTiempoDAO



def menu_registro_tiempo():
    while True:
        print("\n--- MÓDULO DE REGISTRO DE TIEMPO ---")
        print("1. Registrar Horas Trabajadas")
        print("2. Listar Registros")
        print("3. Eliminar Registro")
        print("4. Volver al Menú Principal")
        
        opcion = input("Seleccione una opción (1-4): ").strip()
        
        if opcion == "1":
            try:
                id_emp = int(input("ID del Empleado: "))
                id_proy = int(input("ID del Proyecto: "))
                horas = float(input("Horas trabajadas: "))
                fecha = input("Fecha (YYYY-MM-DD): ").strip()
                RegistroTiempoDAO.insertar(id_emp, id_proy, horas, fecha)
            except ValueError:
                print(" Error: Ingrese valores numéricos válidos para IDs y horas.")
        elif opcion == "2":
            regs = RegistroTiempoDAO.listar()
            for r in regs:
                print(f"ID: {r[0]} | Empleado: {r[1]} | Proyecto: {r[2]} | Horas: {r[3]}h | Fecha: {r[4]}")
        elif opcion == "3":
            try:
                id_reg = int(input("ID del registro a eliminar: "))
                RegistroTiempoDAO.eliminar(id_reg)
            except ValueError:
                print(" ID inválido.")
        elif opcion == "4":
            break