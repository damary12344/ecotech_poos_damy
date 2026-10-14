from datetime import date

class Usuario:
    def __init__(self, id_usuario: int, nombre_usuario: str, contrasena: str, rol: str):
        self._id_usuario = id_usuario
        self._nombre_usuario = nombre_usuario
        self._contrasena = contrasena
        self._rol = rol

    def iniciar_sesion(self) -> bool:
        print(f"Iniciando sesión como {self._nombre_usuario}...")
        return True

    def cerrar_sesion(self) -> None:
        print(f"Sesión cerrada para {self._nombre_usuario}.")

    def validar_acceso(self) -> bool:
        return self._rol in ["Administrador", "Empleado"]


class Administrador(Usuario):
    def __init__(self, id_usuario: int, nombre_usuario: str, contrasena: str, permisos: str):
        super().__init__(id_usuario, nombre_usuario, contrasena, rol="Administrador")
        self._permisos = permisos

    def gestionar_empleados(self) -> None:
        print("Gestionando empleados desde el panel de administración...")

    def gestionar_departamentos(self) -> None:
        print("Gestionando departamentos...")

    def gestionar_proyectos(self) -> None:
        print("Gestionando proyectos...")

    def generar_informes(self) -> None:
        print("Generando informe general...")


class Empleado:
    def __init__(self, id_empleado: int, nombre: str, direccion: str, telefono: str, correo: str, fecha_inicio: str, salario: float, id_departamento: int = None):
        self._id_empleado = id_empleado
        self._nombre = nombre
        self._direccion = direccion
        self._telefono = telefono
        self._correo = correo
        self._fecha_inicio = fecha_inicio
        self._salario = salario
        self._id_departamento = id_departamento

    def registrar(self) -> None:
        print(f"Empleado {self._nombre} registrado correctamente.")

    def actualizar_datos(self, direccion: str, telefono: str) -> None:
        self._direccion = direccion
        self._telefono = telefono
        print(f"Datos de {self._nombre} actualizados.")

    def asignar_departamento(self, id_departamento: int) -> None:
        self._id_departamento = id_departamento

    def registrar_horas(self, horas: float, id_proyecto: int, descripcion: str) -> None:
        print(f"Registradas {horas} hrs para {self._nombre} en el proyecto ID {id_proyecto}.")


class Departamento:
    def __init__(self, id_departamento: int, nombre: str, gerente_id: int = None):
        self._id_departamento = id_departamento
        self._nombre = nombre
        self._gerente_id = gerente_id

    def crear(self) -> None:
        print(f"Departamento {self._nombre} creado.")

    def editar(self, nuevo_nombre: str) -> None:
        self._nombre = nuevo_nombre

    def buscar(self) -> str:
        return f"Departamento: {self._nombre}"

    def eliminar(self) -> None:
        print(f"Departamento {self._nombre} eliminado.")

    def asignar_empleado(self, empleado: Empleado) -> None:
        print(f"Empleado {empleado._nombre} asignado al departamento {self._nombre}.")


class Proyecto:
    def __init__(self, id_proyecto: int, nombre: str, descripcion: str, fecha_inicio: str):
        self._id_proyecto = id_proyecto
        self._nombre = nombre
        self._descripcion = descripcion
        self._fecha_inicio = fecha_inicio

    def crear(self) -> None:
        print(f"Proyecto {self._nombre} creado.")

    def editar(self, descripcion: str) -> None:
        self._descripcion = descripcion

    def eliminar(self) -> None:
        print(f"Proyecto {self._nombre} eliminado.")

    def asignar_empleado(self, empleado: Empleado) -> None:
        print(f"Empleado {empleado._nombre} asignado al proyecto {self._nombre}.")

    def desasignar_empleado(self, empleado: Empleado) -> None:
        print(f"Empleado {empleado._nombre} removido del proyecto {self._nombre}.")


class RegistroTiempo:
    def __init__(self, id_registro: int, fecha: str, horas_trabajadas: float, descripcion: str, id_empleado: int, id_proyecto: int):
        self._id_registro = id_registro
        self._fecha = fecha
        self._horas_trabajadas = horas_trabajadas
        self._descripcion = descripcion
        self._id_empleado = id_empleado
        self._id_proyecto = id_proyecto

    def registrar_horas(self) -> None:
        print(f"Horas registradas con éxito: {self._horas_trabajadas} hrs.")

    def modificar_registro(self, nuevas_horas: float) -> None:
        self._horas_trabajadas = nuevas_horas

    def consultar_registro(self) -> str:
        return f"Registro #{self._id_registro}: {self._horas_trabajadas} hrs el {self._fecha}"


class Informe:
    def __init__(self, tipo: str, fecha_generacion: str):
        self._tipo = tipo
        self._fecha_generacion = fecha_generacion

    def generar_informe(self) -> None:
        print(f"Generando informe de tipo: {self._tipo}")

    def exportar_pdf(self) -> None:
        print(f"Informe {self._tipo} exportado a PDF.")

    def exportar_excel(self) -> None:
        print(f"Informe {self._tipo} exportado a Excel.")
