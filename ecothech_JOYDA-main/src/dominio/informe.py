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