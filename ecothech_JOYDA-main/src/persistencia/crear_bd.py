from sqlite3 import Cursor
from .conexion import abrir_conexion, obtener_motor


def crear_tablas():
    conexion = abrir_conexion()
    cursor = conexion.cursor()

    if obtener_motor() == "sqlite":
        # Habilitar soporte para llaves foráneas en SQLite
        cursor.execute("PRAGMA foreign_keys = ON;")

        # 1. Tabla Departamento
        sql_departamento = """
            CREATE TABLE IF NOT EXISTS departamento (
                id_departamento INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                gerente_id INTEGER,
                FOREIGN KEY (gerente_id) REFERENCES empleado (id_empleado)
            )
        """

        # 2. Tabla Empleado
        sql_empleado = """
            CREATE TABLE IF NOT EXISTS empleado (
                id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                direccion TEXT,
                telefono TEXT,
                correo TEXT NOT NULL,
                fecha_inicio TEXT,
                salario REAL,
                id_departamento INTEGER,
                FOREIGN KEY (id_departamento) REFERENCES departamento (id_departamento)
            )
        """

        # 3. Tabla Proyecto
        sql_proyecto = """
            CREATE TABLE IF NOT EXISTS proyecto (
                id_proyecto INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                fecha_inicio TEXT
            )
        """

        # 4. Tabla RegistroTiempo
        sql_registro_tiempo = """
            CREATE TABLE IF NOT EXISTS registro_tiempo (
                id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                horas_trabajadas REAL NOT NULL,
                descripcion TEXT,
                id_empleado INTEGER NOT NULL,
                id_proyecto INTEGER NOT NULL,
                FOREIGN KEY (id_empleado) REFERENCES empleado (id_empleado),
                FOREIGN KEY (id_proyecto) REFERENCES proyecto (id_proyecto)
            )
        """

        cursor.execute(sql_departamento)
        cursor.execute(sql_empleado)
        cursor.execute(sql_proyecto)
        cursor.execute(sql_registro_tiempo)

    else:
        # 1. Tabla Departamento (sin FK inicial para evitar error de tabla inexistente)
        sql_departamento = """
            CREATE TABLE IF NOT EXISTS departamento (
                id_departamento INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                gerente_id INT
            )
        """

        # 2. Tabla Empleado
        sql_empleado = """
            CREATE TABLE IF NOT EXISTS empleado (
                id_empleado INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                direccion VARCHAR(255),
                telefono VARCHAR(20),
                correo VARCHAR(150) NOT NULL,
                fecha_inicio DATE,
                salario FLOAT,
                id_departamento INT,
                FOREIGN KEY (id_departamento) REFERENCES departamento (id_departamento)
            )
        """

        # 3. Tabla Proyecto
        sql_proyecto = """
            CREATE TABLE IF NOT EXISTS proyecto (
                id_proyecto INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                descripcion TEXT,
                fecha_inicio DATE
            )
        """

        # 4. Tabla RegistroTiempo
        sql_registro_tiempo = """
            CREATE TABLE IF NOT EXISTS registro_tiempo (
                id_registro INT AUTO_INCREMENT PRIMARY KEY,
                fecha DATE NOT NULL,
                horas_trabajadas FLOAT NOT NULL,
                descripcion TEXT,
                id_empleado INT NOT NULL,
                id_proyecto INT NOT NULL,
                FOREIGN KEY (id_empleado) REFERENCES empleado (id_empleado),
                FOREIGN KEY (id_proyecto) REFERENCES proyecto (id_proyecto)
            )
        """

        cursor.execute(sql_departamento)
        cursor.execute(sql_empleado)
        cursor.execute(sql_proyecto)
        cursor.execute(sql_registro_tiempo)

        # Se añade la relación de gerente a departamento una vez creada la tabla empleado
        sql_alter_departamento = """
            ALTER TABLE departamento
            ADD CONSTRAINT fk_departamento_gerente
            FOREIGN KEY (gerente_id) REFERENCES empleado (id_empleado)
        """

        # Se intenta añadir la FK si no existe la restricción previa
        try:
            cursor.execute(sql_alter_departamento)
        except Exception:
            pass  # Evita errores si la FK ya estaba creada

    conexion.commit()
    cursor.close()
    conexion.close()


if __name__ == "__main__":
    crear_tablas()
    print("Base de datos preparada correctamente.")