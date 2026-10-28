from database import obtener_conexion
from mysql.connector import Error
from datetime import datetime

def crear_lista_ventas(nombre):
    
    conexion = obtener_conexion()

    if conexion is None:
        return False, "No se pudo conectar con la base de datos"


    cursor = None

    try:
        cursor  = conexion.cursor()

        consulta = """
        INSERT INTO listas_ventas
            (nombre, fecha_creacion, estado)
        VALUES (%s, %s, %s)
         """


        cursor.execute(
             consulta, 
             [nombre, datetime.now(),"ACTIVA"])

       
        conexion.commit()
        return True, "Lista de ventas creada correctamente."

    except Error as error:
           
            conexion.rollback()
            print(f"Error al crear la lista de venta:{error}")
                  
            return False, f"No se pudo crear la lista de ventas: {error}"
                  
    finally:

       
        if cursor is not None:
            cursor.close()
        conexion.close()
        