from database import obtener_conexion
from mysql.connector import Error
from datetime import datetime



# Guarda una rifa nueva en la base de datos.
# Recibe el nombre, la descripción, el precio de cada número y la fecha del sorteo.
# Devuelve True y un mensaje si se guarda correctamente; si ocurre un error,
# devuelve False y una explicación.
def crear_rifa(nombre, descripcion, precio_numero, fecha_sorteo):
    # Abre la conexión necesaria para comunicarse con la base de datos.
    conexion = obtener_conexion()
    if conexion is None:
        return False, "No se pudo conectar con la base de datos"

    # Se prepara el cursor, que permite enviar instrucciones a la base de datos.
    cursor = None
    try:
        cursor  = conexion.cursor()
        # Instrucción para guardar los datos de la rifa.
        consulta = """
        INSERT INTO rifas
            (nombre, descripcion, precio_numero, fecha_sorteo, estado, fecha_creacion)
        VALUES (%s, %s, %s, %s, %s, %s)

                """

        # Guarda la rifa como activa y registra la fecha y hora de creación.
        cursor.execute(
             consulta, 
             (nombre, descripcion, precio_numero, fecha_sorteo, "activa", datetime.now()))

        # Confirma los cambios para que la nueva rifa quede guardada.
        conexion.commit()
        return True, "Rifa creada correctamente."

    except Error as error:
            # Deshace los cambios si no se pudo guardar y muestra el error.
            conexion.rollback()
            print(f"Error al crear la rifa:{error}")
                  
            return False, f"No se pudo crear la rifa: {error}"
                  
    finally:
        # Cierra el cursor y la conexión, incluso si ocurrió un error.
        if cursor is not None:
            cursor.close()
        conexion.close()


        # Busca las rifas que están activas y devuelve sus datos para mostrarlos en la app.
        # Si no hay conexión o ocurre un error, devuelve una lista vacía.
def listar_rifas_activas():
    conexion = obtener_conexion()# Abre la conexión con la base de datos.
    if conexion is None:
        return []

    cursor = None
    try:
        # Solicita los resultados como filas con nombres de columna.
        cursor  = conexion.cursor(dictionary=True)
        # Selecciona los datos de las rifas activas, de la más reciente a la más antigua.
        consulta = """
        SELECT id_rifa, nombre, descripcion, precio_numero, fecha_sorteo, estado
                    FROM rifas
                    WHERE estado = %s
                    ORDER BY id_rifa DESC

                """

        # Ejecuta la búsqueda usando "activa" como estado.
        cursor.execute(
             consulta, ["activa"])

        # Devuelve todas las rifas encontradas.
        return cursor.fetchall()

    except Error as error:
            # Informa el error y devuelve una lista vacía.
            print(f"Error al consultar rifas activas:{error}")
                  
            return []
                  
    finally:
        # Cierra los recursos utilizados para la consulta.
        if cursor is not None:
            cursor.close()
        conexion.close()


        # Busca los participantes y números registrados para una rifa específica.
        # Recibe el identificador de la rifa y devuelve una lista con sus participantes.
        # Si no hay conexión o ocurre un error, devuelve una lista vacía.

def listar_participantes_rifa (id_rifa):
    conexion = obtener_conexion()  # Abre la conexión con la base de datos.

    if conexion is None:
         return[]
    
    cursor = None   
    try:  
         # Solicita los resultados como filas con nombres de columna.
         cursor = conexion.cursor(dictionary=True)
         consulta = """SELECT numero, id_cliente, nombre_comprador, telefono_comprador, pagado, estado
         FROM participantes_rifa WHERE id_rifa = %s"""

         # Busca los participantes usando el identificador recibido.
         cursor.execute(consulta, [id_rifa])
         # Devuelve todos los participantes encontrados.
         return cursor.fetchall()
    except Error as error:
         print(f"Error al consultar los ´numeros de la rifa:{error}")
         return[]

    finally:
         # Cierra el cursor y la conexión al terminar.
         if cursor is not None:
              cursor.close()
              conexion.close()



def registrar_participante_rifa(
    id_rifa, numero, nombre_comprador, telefono_comprador, estado, pagado):
    conexion = obtener_conexion()

    if conexion is None:
        return False, "No se pudo conectar con MySQL."

    cursor = None

    try:
        cursor = conexion.cursor()

        consulta_verificar = """SELECT COUNT(*)
                            FROM participantes_rifa
                            WHERE id_rifa = %s AND numero = %s""" 

        cursor.execute(consulta_verificar,[id_rifa, numero])
        resultado = cursor.fetchone()

        if resultado[0] > 0:
            return False, "Este numero ya está registrado en la rifa."

        consulta_insertar = (
                "INSERT INTO participantes_rifa "
                "(id_rifa, numero, nombre_comprador, "
                "telefono_comprador, estado, pagado) "
                "VALUES (%s, %s, %s, %s, %s, %s)"
            )
        cursor.execute(
            consulta_insertar,
            [
                id_rifa,
                int(numero),
                nombre_comprador,
                telefono_comprador or None,
                estado,
                pagado
            ]
        )

        conexion.commit()
        return True, "Número registrado correctamente."

    except Error as error:
        conexion.rollback()
        print(f"ERROR REAL  DE MYSQL: {error}")
        return False, f"Error al guardar:{error}"

    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()


 # crea el historial de rifas finalizadas 
def listar_historial_rifas():
    conexion = obtener_conexion()

    if conexion is None:
        return []

    cursor = None

    try:
        cursor = conexion.cursor(dictionary=True)

        consulta = """
            SELECT
                id_rifa,
                nombre,
                descripcion,
                precio_numero,
                fecha_sorteo,
                estado
            FROM rifas
            WHERE estado <> %s
            ORDER BY id_rifa DESC
        """

        cursor.execute(consulta, ["activa"])
        return cursor.fetchall()

    except Error as error:
        print(f"Error al consultar el historial de rifas: {error}")
        return []

    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()

def liberar_numero_rifa(id_rifa, numero):
    conexion = obtener_conexion()

    if conexion is None:
        return False, "No se pudo conectar con MySQL."

    cursor = None

    try:
        cursor = conexion.cursor()

        consulta = """
            DELETE FROM participantes_rifa
            WHERE id_rifa = %s AND numero = %s
        """

        cursor.execute(consulta, [id_rifa, int(numero)])

        if cursor.rowcount == 0:
            conexion.rollback()
            return False, "Este número no tiene una asignación registrada."

        conexion.commit()
        return True, "Número liberado correctamente."

    except Error as error:
        conexion.rollback()
        print(f"Error al liberar número: {error}")
        return False, f"No se pudo liberar el número: {error}"

    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()



def actualizar_pago_rifa(id_rifa, numero, pagado):
    conexion = obtener_conexion()

    if conexion is None:
        return False, "No se pudo conectar con MySQL."

    cursor = None

    try:
        cursor = conexion.cursor()

        consulta = """
            UPDATE participantes_rifa
            SET pagado = %s
            WHERE id_rifa = %s AND numero = %s
        """

        cursor.execute(
            consulta,
            [pagado, id_rifa, int(numero)]
        )

        if cursor.rowcount == 0:
            conexion.rollback()
            return False, "No se encontró el número o no hubo cambios."

        conexion.commit()

        if pagado == 1:
            return True, "¡Pago registrado correctamente!"
        else:
            return True, "El número ahora está pendiente de pago."

    except Error as error:
        conexion.rollback()
        print(f"Error al actualizar el pago: {error}")
        return False, f"No se pudo actualizar el pago: {error}"

    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()


def finalizar_rifa(id_rifa):
    conexion = obtener_conexion()

    if conexion is None:
        return False, "No se pudo conectar con MySQL."

    cursor = None

    try:
        cursor = conexion.cursor()

        consulta = """
            UPDATE rifas
            SET estado = %s
            WHERE id_rifa = %s AND estado = %s
        """

        cursor.execute(
            consulta,
            ["finalizada", id_rifa, "activa"]
        )

        if cursor.rowcount == 0:
            conexion.rollback()
            return False, "La rifa no existe o ya fue finalizada."

        conexion.commit()
        return True, "La rifa se finalizó correctamente."

    except Error as error:
        conexion.rollback()
        print(f"Error al finalizar la rifa: {error}")
        return False, f"No se pudo finalizar la rifa: {error}"

    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()