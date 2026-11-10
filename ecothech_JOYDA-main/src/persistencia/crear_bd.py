import sqlite3

def conectar():
    return sqlite3.connect("ecotech.db")

def crear_tablas():
    conexion = conectar()
    cursor = conexion.cursor()

    # Tabla Empleados (Ya existente)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            direccion TEXT,
            telefono TEXT,
            correo TEXT,
            fecha_inicio TEXT,
            salario REAL
        )
    """)

    # 1. Tabla Departamentos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            ubicacion TEXT
        )
    """)

    # 2. Tabla Proyectos (Relacionada opcionalmente con un departamento)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS proyectos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            id_departamento INTEGER,
            FOREIGN KEY (id_departamento) REFERENCES departamentos(id)
        )
    """)

    # 3. Tabla Registro de Tiempo (Relaciona Empleados y Proyectos)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registro_tiempo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_empleado INTEGER NOT NULL,
            id_proyecto INTEGER NOT NULL,
            horas REAL NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY (id_empleado) REFERENCES empleados(id),
            FOREIGN KEY (id_proyecto) REFERENCES proyectos(id)
        )
    """)

    conexion.commit()
    conexion.close()