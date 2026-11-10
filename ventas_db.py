
from database import obtener_conexion
from mysql.connector import Error
from datetime import datetime
from decimal import Decimal, InvalidOperation


def crear_lista_ventas(nombre, precio_unitario):
    
    conexion = obtener_conexion()

    if conexion is None:
        return False, "No se pudo conectar con la base de datos"


    cursor = None

    try:
        cursor  = conexion.cursor()

        consulta = """
        INSERT INTO listas_ventas
            (nombre, fecha_creación, estado, precio_unitario)
        VALUES (%s, %s, %s, %s)
         """


        cursor.execute(
             consulta, 
             [nombre, datetime.now(),"ACTIVA", precio_unitario])

       
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

def listar_listas_ventas():
    conexion = obtener_conexion()

    if conexion is None:
        return[]

    cursor = None

    try:
         print("BASE DE DATOS CONECTADA:", conexion.database)

         cursor = conexion.cursor(dictionary=True)

         consulta= """SELECT id_lista, nombre, fecha_creación, estado, precio_unitario
                FROM listas_ventas
                ORDER BY id_lista DESC"""

         cursor.execute(consulta)
         listas = cursor.fetchall()
         print("Listas de ventas obtenidas:", listas)
         return listas

    except Error as error:
        print(f"Error al consultar las listas de ventas: {error}")
        return []


    finally:
        if cursor is not None:
           cursor.close()
           conexion.close()



def editar_lista_ventas(id_lista, nombre, precio_unitario):
    conexion = obtener_conexion()

    if conexion is None:
        return False, "No se pudo conectar con la base de datos"

    cursor = None

    try:
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT id_lista FROM listas_ventas" \
            " WHERE id_lista = %s", [id_lista]
        )

        lista = cursor.fetchone()

        if lista is None:
            return False, "no se encontró la lista de ventas con el ID proporcionado." 

        consulta = """
        UPDATE listas_ventas
        SET nombre = %s, precio_unitario = %s
        WHERE id_lista = %s
        """

        cursor.execute(consulta, [nombre, precio_unitario, id_lista])

        conexion.commit()
        return True, "Lista de ventas actualizada correctamente."

    except Error as error:
        conexion.rollback()
        print(f"Error al editar la lista de ventas: {error}")
        return False, f"No se pudo actualizar la lista de ventas: {error}"

    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()




def eliminar_lista_ventas(id_lista):
    conexion = obtener_conexion()

    if conexion is None:
        return False, "No se pudo conectar con la base de datos"

    cursor = None

    try:
        cursor = conexion.cursor()

        consulta = """
        SELECT COUNT(*) FROM ventas
        WHERE id_lista = %s
        """

        cursor.execute(consulta, [id_lista])
        cantidad_ventas = cursor.fetchone()[0]

        if cantidad_ventas > 0:
            consulta = """UPDATE listas_ventas SET estado = 'INACTIVA
                        WHERE id_lista' = %s"""

            cursor.execute(consulta, [id_lista])
            conexion.commit()
            return True, "la lista ha sido marcada como inactiva."

    
        else:
            consulta = """DELETE FROM listas_ventas
            WHERE id_lista = %s
            """

            cursor.execute(consulta, [id_lista])

            if cursor.rowcount == 0:
                conexion.rollback()
                return False, "No se encontró la lista de ventas con el ID proporcionado."
        mensaje = "La lista de ventas ha sido eliminada correctamente."

        conexion.commit()
        return True, mensaje

    except Error as error:
        conexion.rollback()
        print(f"Error al eliminar la lista de ventas: {error}")
        return False, f"No se pudo eliminar la lista de ventas: {error}"

    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()



def registrar_pedido(id_lista, nombre_cliente, cantidad, precio_unitario, abono):
    conexion = obtener_conexion()

    if conexion is None:
        return False, "No se pudo conectar con la base de datos"

    cursor = None

    try:
        cursor = conexion.cursor()
        nombre_cliente = nombre_cliente.strip()
        cantidad = int (cantidad)
        precio_unitario = Decimal(str(precio_unitario)).quantize(Decimal("0.01"))
        abono = Decimal(str(abono or 0)).quantize(Decimal("0.01"))

        if not nombre_cliente:
            return False, "El nombre del cliente no puede estar vacío."

        if cantidad <= 0 or precio_unitario <= 0:
            return False, "La cantidad y el precio unitario deben ser mayor a 0."

        total = (Decimal(cantidad) * precio_unitario).quantize(Decimal("0.01"))

        

        if abono < 0 or abono > total:
            return False, "El abono no puede ser negativo ni mayor al total."

        saldo= (total - abono).quantize(Decimal("0.01"))

        #obtener el nombre de la lista 
        cursor.execute("SELECT nombre FROM listas_ventas WHERE id_lista = %s", [id_lista])
        resultado = cursor.fetchone()

        if resultado is None:
            return False, "No se encontró la lista de ventas con el ID proporcionado."

        nombre_producto = resultado[0]

        #registrar la venta
        consulta_venta = """ INSERT INTO ventas (id_lista, nombre_cliente, tipo_venta, fecha_venta, total)
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(consulta_venta, [id_lista, nombre_cliente, "PEDIDO", datetime.now(), total])

        id_venta = cursor.lastrowid

        #registrar el detalle del pedido
        consulta_detalle = """ INSERT INTO detalle_ventas (id_ventas,producto, cantidad, precio_unitario, subtotal)
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(consulta_detalle, [id_venta, nombre_producto, cantidad, precio_unitario, total])

        #registrar el abono inicial, si existe
        if abono > 0:
            consulta_pago = """ INSERT INTO pagos (id_ventas, monto, fecha_pago)
            VALUES (%s, %s, %s)
            """
            cursor.execute(consulta_pago, [id_venta, abono, datetime.now()])

        conexion.commit()
        return True, (f"Pedido registrado correctamente.\n"
        f"Total: B/. {total:.2f}\n" f"Abono: B/. {abono:.2f}\n" f"Saldo Pendiente: B/. {saldo:.2f}")

    except Exception as error:
        conexion.rollback()
        print(f"Error al registrar el pedido: {error}")
        return False, f"No se pudo registrar el pedido: {error}"
    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()



def listar_pedidos_lista(id_lista):

    conexion = obtener_conexion()

    if conexion is None:
        return False, "No se pudo conectar con la base de datos."

    cursor = None

    try:
        cursor = conexion.cursor()

        consulta = """
            SELECT
                v.id_ventas,
                v.nombre_cliente,
                d.cantidad,
                d.subtotal,
                v.estado_entrega
            FROM ventas v
            INNER JOIN detalle_ventas d
                ON v.id_ventas = d.id_ventas
            WHERE v.id_lista = %s
            AND v.tipo_venta = 'PEDIDO'
            ORDER BY v.fecha_venta DESC
        """

        cursor.execute(consulta, [id_lista])

        pedidos = cursor.fetchall()

        return True, pedidos

    except Error as error:
        print(f"Error al consultar los pedidos: {error}")
        return False, f"No se pudieron consultar los pedidos: {error}"

    finally:
        if cursor is not None:
            cursor.close()

        conexion.close()

def actualizar_estado_entrega(id_venta, nuevo_estado):
    estados_validos = ('PENDIENTE', 'ENTREGADO', 'CANCELADO')

    if nuevo_estado not in estados_validos:
        return False, "Estado inválido."

    conexion = obtener_conexion()
    if conexion is None:
        return False, "No se pudo conectar con la base de datos."

    cursor = None
    try:
        cursor = conexion.cursor()

        consulta = """
            SELECT id_ventas FROM ventas
            WHERE id_ventas = %s AND tipo_venta = 'PEDIDO'
        """

        cursor.execute(consulta, [id_venta])
        pedido = cursor.fetchone()

        if pedido is None:
            return False, "No se encontró el pedido."

        consulta = """
            UPDATE ventas
            SET estado_entrega = %s
            WHERE id_ventas = %s
            AND tipo_venta = 'PEDIDO'
        """

        cursor.execute(consulta, [nuevo_estado, id_venta])
        conexion.commit()
        return True, "Estado de entrega actualizado correctamente."

    except Error as error:
        conexion.rollback()
        print(f"Error al actualizar el estado: {error}")
        return False, f"Error al actualizar el estado: {error}"

    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()

def registrar_abono(id_venta, monto, metodo_pago):
    conexion = obtener_conexion()

    if conexion is None:
        return False, "No se pudo conectar con la base de datos."

    cursor = None

    try:
        cursor = conexion.cursor()

        #validar el monto
        monto = Decimal(str(monto)).quantize(Decimal("0.01"))

        if monto <= 0:
            return False, " El abono debe ser mayor que cero."

        # validar el metodo de pago
        metodos_validos = ("EFECTIVO", "YAPPY", "TRANSFERENCIA", "TARJETA", "OTRO")

        if not metodo_pago:
            return False, "No se pueden registrar abonos a pedidos"

        metodo_pago = metodo_pago.strip().upper()

        if metodo_pago not in metodos_validos:
            return False, "El método de pago no es válido"


        # Consultar el pedido y bloquearlo durante la operación

        cursor.execute(""" SELECT total, estado_entrega  FROM ventas WHERE id_ventas =%s
                        AND tipo_venta = 'PEDIDO' FOR UPDATE """, [id_venta])

        pedido = cursor.fetchone()

        if pedido is None:
            return False, "No se encontró el pedido."

        total = Decimal(str(pedido[0]))
        estado_entrega = pedido[1]

        if estado_entrega == "CANCELADO":
            return False, "No se pueden registrar abonos  apedidos cancelados."

        # Consultar los abonos anterores
        cursor.execute("""SELECT COALESCE(SUM(monto), 0)
                       from pagos WHERE id_ventas = %s""", [id_venta])

        abonado = Decimal(str(cursor.fetchone()[0]))
        saldo = total - abonado

        if monto > saldo:
            return False, (f"El abono supera el saldo pendiente de B/. {saldo:.2f}.")

        # registrar el nuevo abono
        cursor.execute(""" INSERT INTO pagos (id_ventas, monto, fecha_pago, metodo_pago)
        VALUES (%s, %s, %s, %s)""", [id_venta, monto, datetime.now(), metodo_pago])

        conexion.commit()

        nuevo_abonado = abonado + monto
        nuevo_saldo = total - nuevo_abonado

        return True, (
            "Abono registrado correctamente.\n " f"Total del pedido: B/. {total:.2f}\n"
            f"Total abonado: B/. {nuevo_abonado:.2f}\n"
            f"saldo pendiente: B/. {nuevo_saldo:.2f}\n"
        )

    except (Error, ValueError, InvalidOperation) as error:
        conexion.rollback()
        print (f"Error al registrar el abono: {error}")
        return False, f"no se pudo registrar el abono: {error}"


    finally:
        if cursor is not None:
            cursor.close()

        conexion.close()


def consultar_resumen_pago(id_venta):

    conexion = obtener_conexion()

    if conexion is None:
        return False, "No se pudo conectar con la base de datos."

    cursor = None

    try:
        cursor = conexion.cursor()

        consulta = """
            SELECT
                v.total,
                COALESCE(SUM(p.monto), 0) AS abonado
            FROM ventas v
            LEFT JOIN pagos p
                ON v.id_ventas = p.id_ventas
            WHERE v.id_ventas = %s
            AND v.tipo_venta = 'PEDIDO'
            GROUP BY v.id_ventas, v.total
        """

        cursor.execute(consulta, [id_venta])

        resultado = cursor.fetchone()

        if resultado is None:
            return False, "No se encontró el pedido."

        total = Decimal(str(resultado[0]))
        abonado = Decimal(str(resultado[1]))

        saldo = total - abonado
        saldo = saldo.quantize(Decimal("0.01"))

        if abonado > total:
            return False, "Error: los abonos registrados superan el total del pedido"

        if saldo <= 0:
            estado_pago = "PAGADO"
        else:
            estado_pago = "PENDIENTE DE PAGO"

        return True, {
            "total": total,
            "abonado": abonado,
            "saldo": saldo,
            "estado_pago": estado_pago
        }

    except Error as error:
        print(f"Error al consultar el pago: {error}")
        return False, f"No se pudo consultar el pago: {error}"

    finally:
        if cursor is not None:
            cursor.close()

        conexion.close()


def consultar_detalle_pedido(id_venta):

    conexion = obtener_conexion()

    if conexion is None:
        return False, "No se pudo conectar con la base de datos."

    cursor = None

    try:
        cursor = conexion.cursor()

        consulta = """
            SELECT
                v.nombre_cliente,
                d.cantidad,
                d.precio_unitario,
                v.total,
                v.estado_entrega
            FROM ventas v
            INNER JOIN detalle_ventas d
                ON v.id_ventas = d.id_ventas
            WHERE v.id_ventas = %s
            AND v.tipo_venta = 'PEDIDO'
        """

        cursor.execute(consulta, [id_venta])

        resultado = cursor.fetchone()

        if resultado is None:
            return False, "No se encontró el pedido."

        return True, {
            "nombre_cliente": resultado[0],
            "cantidad": resultado[1],
            "precio_unitario": Decimal(str(resultado[2])),
            "total": Decimal(str(resultado[3])),
            "estado_entrega": resultado[4]
        }

    except Error as error:
        print(f"Error al consultar el detalle del pedido: {error}")
        return False, f"No se pudo consultar el pedido: {error}"

    finally:
        if cursor is not None:
            cursor.close()

        conexion.close()

def registrar_venta_individual(nombre_cliente, productos):

    conexion = obtener_conexion()

    if conexion is None:
        return False, "No se pudo conectar con la base de datos."

    cursor = None

    try:
        nombre_cliente= nombre_cliente.strip()

        if not nombre_cliente:
            return False, "Debes ingresar el nombre del cliente"

        if not productos:
            return False, "Debes agregar al menos un producto"

        detalles = []
        total= Decimal("0.00")

        for producto in productos:
            nombre = producto["producto"].strip()
            cantidad = int (producto["cantidad"])
            precio = Decimal(str(producto["precio_unitario"])).quantize(Decimal("0.01"))

            if not nombre:
                return False, "Hay un producto sin nombre."

            if cantidad <= 0 or precio <= 0:
                return False, "La cantidad y el precio deben ser mayores que cero."

            subtotal = (Decimal(cantidad) * precio).quantize(Decimal("0.01"))

            total += subtotal
            detalles.append((nombre, cantidad, precio, subtotal))

        total = total.quantize(Decimal("0.01"))

        cursor = conexion.cursor()

        consulta_venta = """INSERT INTO ventas(nombre_cliente, tipo_venta, fecha_venta, total)
        VALUES (%s, 'VENTA', NOW(), %s)"""

        cursor.execute(consulta_venta, (nombre_cliente, total))

        id_venta = cursor.lastrowid
        consulta_detalle ="""INSERT INTO detalle_ventas(id_ventas, producto, cantidad, precio_unitario, subtotal)
        VALUES (%s, %s, %s, %s, %s)"""

        for detalle in detalles:
            cursor.execute(consulta_detalle, (id_venta, *detalle))

        conexion.commit()

        return True, (f"Venta registrada corroectamente."
                      f"ID: {id_venta}. Total: B/. {total:.2f}")

    except (Error, ValueError, InvalidOperation, KeyError) as error:

        conexion.rollback()

        print(f"Error al registrar la venta individual: {error}")

        return False, f"No se pudo registrar la venta: {error}"

    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()


    # HISTORIAL DE VENTAS INDIVIDUALES
def listar_ventas_individuales():

    conexion = obtener_conexion()

    if conexion is None:
        return []

    cursor = None

    try:
        cursor = conexion.cursor(dictionary=True)

        consulta = """
            SELECT
                id_ventas,
                nombre_cliente,
                fecha_venta,
                total
            FROM ventas
            WHERE tipo_venta = 'VENTA'
            ORDER BY fecha_venta DESC
        """

        cursor.execute(consulta)

        ventas = cursor.fetchall()

        return ventas

    except Error as e:
        print("Error al consultar las ventas:", e)
        return []

    finally:
        if cursor:
            cursor.close()

        conexion.close()

# Recupera todos los productos correspondientes a una venta.
def consultar_detalle_venta(id_venta):

    conexion = obtener_conexion()

    if conexion is None:
        return []

    cursor = None

    try:
        cursor = conexion.cursor(dictionary=True)

        consulta = """
        SELECT
            v.nombre_cliente,
            v.fecha_venta,
            v.total,
            d.producto,
            d.cantidad,
            d.precio_unitario,
            d.subtotal
        FROM ventas v
        INNER JOIN detalle_ventas d
            ON v.id_ventas = d.id_ventas
        WHERE v.id_ventas = %s
    """

        cursor.execute(consulta, (id_venta,))

        return cursor.fetchall()

    except Error as e:
        print("Error al consultar el detalle de la venta:", e)
        return []

    finally:
        if cursor:
            cursor.close()

        conexion.close()

    # FUNCION PARA ELIMINAR VENTAS
def eliminar_venta_individual(id_venta):

    conexion = obtener_conexion()

    if conexion is None:
        return False, "No se pudo conectar con la base de datos."

    cursor = None

    try:
        cursor = conexion.cursor(dictionary=True)

        # Comprobar que la venta existe
        cursor.execute(
            """
            SELECT id_ventas
            FROM ventas
            WHERE id_ventas = %s
            FOR UPDATE
            """,
            (id_venta,)
        )

        venta = cursor.fetchone()

        if not venta:
            return False, "La venta no existe."

        # Comprobar si tiene pagos registrados
        cursor.execute(
            """
            SELECT id_pago
            FROM pagos
            WHERE id_ventas = %s
            LIMIT 1
            """,
            (id_venta,)
        )

        pago = cursor.fetchone()

        if pago:
            conexion.rollback()
            return False, (
                "Esta venta tiene pagos registrados. "
                "No se puede eliminar."
            )

        # Eliminar la venta
        cursor.execute(
            """
            DELETE FROM ventas
            WHERE id_ventas = %s
            """,
            (id_venta,)
        )

        conexion.commit()

        return True, "La venta se eliminó correctamente."

    except Error as e:
        conexion.rollback()
        print("Error al eliminar la venta:", e)
        return False, "Ocurrió un error al eliminar la venta."

    finally:
        if cursor:
            cursor.close()

        conexion.close()




               
