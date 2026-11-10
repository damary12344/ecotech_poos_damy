import os


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPresione Enter para continuar...")