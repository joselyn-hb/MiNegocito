from database import obtener_conexion

conexion = obtener_conexion()

if conexion is not None:
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT DATABASE()")
        resultado = cursor.fetchone()

        print("¡Conexión exitosa!")
        print("Base de datos:", resultado[0])

        cursor.close()

    finally:
        conexion.close()
        print("Conexión cerrada correctamente.")

else:
    print("No se pudo conectar. Revisa el error anterior.")