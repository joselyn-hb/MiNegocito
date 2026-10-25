from database import obtener_conexion
from mysql.connector import Error

def crear_rifa(nombre, descripcion, precio_numero, fecha_sorteo):
    conexion = obtener_conexion()
    if conexion is None:
        return False, "No se pudo conectar con la base de datos"

    cursor = None
    try:
        cursor  = conexion.cursor()
        consulta = """
        INSERT INTO rifas
            (nombre, descripcion, precio_numero, fecha_sorteo, estado, fecha_creacion)
        VALUES (%s, %s, %s, %s, %s
        NOW())
                """

        cursor.execute(
             consulta, 
             (nombre, descripcion, precio_numero, fecha_sorteo, "activa"))

        conexion.commit()
        return True, "Rifa creada correctamente."

    except Error as error:
            conexion.rollback()
            print(f"Error al crear la rifa:{error}")
                  
            return False, f"No se pudo crear la rifa: {error}"
                  
    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()
        