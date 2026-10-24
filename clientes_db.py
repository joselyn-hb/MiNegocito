from database import obtener_conexion
from mysql.connector import Error

# GUARDA UN CLIENTE NUEVO EN MYSQL
def registrar_cliente(nombre, telefono=None,correo=None,direccion=None, notas=None):
    nombre = nombre.strip()
    if not nombre:
        print("Error: el nombre del cliente es obligatorio")
        return False

    conexion = obtener_conexion()
    if conexion is None:
        print("No se pudo conectar con la base de datos")
        return False

    cursor = None
    try:  
        cursor = conexion.cursor()
        consulta = """
        INSERT INTO clientes(nombre, telefono, correo, direccion, notas)
                    VALUES (%s, %s, %s, %s, %s)"""

        valores = (nombre, telefono, correo, direccion, notas)
        cursor.execute(consulta, valores)
        conexion.commit()

        print(f"Cliente registrado exitosamente. ID: {cursor.lastrowid}")
        return cursor.lastrowid


    except Error as error: 
        conexion.rollback()
        print(f"Error al registrar el cliente:{error}")
        return False

    finally:
        if cursor is not None:
            cursor.close()




def listar_clientes():
    """Devuelve todos los clientes , del mas reciente al mas antiguo"""

    conexion = obtener_conexion()
    if conexion is None:
        return []
    cursor = None

    try:
        cursor = conexion.cursor(dictionary=True)

        consulta ="""SELECT id_cliente, nombre, telefono, correo, direccion, notas, fecha_registro
        FROM clientes
        ORDER BY id_cliente DESC"""

        cursor.execute(consulta)
        return cursor.fetchall()

    except Error as error:
        print(f"Erroro al consultar los clientes:{error}")
        return[]
    finally:
        if cursor is not None:
            cursor.close()
            conexion.close()


def buscar_clientes (texto):
    """Busca clientes por nombr eo telefono"""
    texto = texto.strip()
    if not texto:
        return[]
    conexion = obtener_conexion()
    if conexion is None:
        return []

    cursor = None

    try:
        cursor = conexion.cursor(dictionary=True)

        consulta = """SELECT id_cliente, nombre, telefono, correo, direccion, notas, fecha_registro
        FROM clientes
        WHERE nombre LIKE %s
           or telefono LIKE %s
           ORDER BY nombre"""


        termino = f"%{texto}%"
        cursor.execute(consulta, (termino, termino))

        return cursor.fetchall()
    except Error as error:
        print(f"Error al buscar clientes:{error}")
        return[]

    finally:
     if cursor is not None:
         cursor.close()

     conexion.close()
    
        



    