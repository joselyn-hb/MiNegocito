import os
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error 

#cargar variables de entorno desde el archivo .env
load_dotenv()

def obtener_conexion():

    conexion = None
    try:
        conexion = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "mi_negocito")
        )
        if conexion.is_connected():         
         return conexion

        conexion.close()
    
    except Error as error:
        print(f"Error al conectar a la base de datos: {error}")
        return None