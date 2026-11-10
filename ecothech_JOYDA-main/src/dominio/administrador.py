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