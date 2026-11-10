import bcrypt

from dominio.usuario import Usuario
from persistencia.usuario_dao import UsuarioDAO
from persistencia.empleados_dao import EmpleadoDAO
from servicios.permisos import exigir_admin

MAX_BYTES_BCRYPT = 72


def crear_hash(clave):
    clave = Usuario.validar_clave(clave)
    clave_bytes = clave.encode("utf-8")
    if len(clave_bytes) > MAX_BYTES_BCRYPT:
        raise ValueError("Máximo 72 bytes UTF-8 para bcrypt.")
    return bcrypt.hashpw(clave_bytes, bcrypt.gensalt()).decode("utf-8")


def registrar_usuario(empleado_id, nombre, clave):
    nombre = Usuario.normalizar_usuario(nombre)
    if type(empleado_id) is not int or empleado_id <= 0:
        raise ValueError("El ID del empleado debe ser positivo.")
    if EmpleadoDAO.buscar_por_id(empleado_id) is None:
        raise ValueError("No existe un empleado con ese ID.")
    if (UsuarioDAO.buscar_por_nombre(nombre) is not None
            or UsuarioDAO.buscar_por_empleado(empleado_id) is not None):
        raise ValueError("No se pudo crear esa cuenta.")
    hash_guardado = crear_hash(clave)
    usuario = Usuario(nombre, hash_guardado, empleado_id)
    return UsuarioDAO.insertar(usuario)


def registrar_usuario_admin(sesion, empleado_id, nombre, clave):
    exigir_admin(sesion)
    return registrar_usuario(empleado_id, nombre, clave)


def autenticar(nombre, clave):
    try:
        nombre = Usuario.normalizar_usuario(nombre)
    except (TypeError, ValueError):
        return None
    if not isinstance(clave, str):
        return None
    datos = clave.encode("utf-8")
    if not 0 < len(datos) <= MAX_BYTES_BCRYPT:
        return None
    cuenta = UsuarioDAO.buscar_por_nombre(nombre)
    if cuenta is None:
        return None
    if not bcrypt.checkpw(datos, cuenta.password_hash.encode("utf-8")):
        return None
    return {"id": cuenta.id, "empleado_id": cuenta.empleado_id,
            "nombre_usuario": cuenta.nombre_usuario, "rol": cuenta.rol}