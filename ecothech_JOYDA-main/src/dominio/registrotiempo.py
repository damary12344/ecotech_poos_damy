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
