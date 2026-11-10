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



from ventas_db import editar_lista_ventas

exito, mensaje = editar_lista_ventas(1, "Arroz com leche actualizado", 2.50)
print(exito)
print(mensaje)

from ventas_db import eliminar_lista_ventas

exito, mensaje = eliminar_lista_ventas(3)
print(exito)
print(mensaje)

from ventas_db import eliminar_lista_ventas

resultado = eliminar_lista_ventas(1)
print(resultado)

from ventas_db import actualizar_estado_entrega

exito, mensaje = actualizar_estado_entrega(4, "PENDIENTE")

print(exito)
print(mensaje)



exito, mensaje = actualizar_estado_entrega(1, "PENDIENTE")

print("SEGUNDA PRUEBA:")
print(exito)
print(mensaje)


from ventas_db import editar_lista_ventas

exito, mensaje = editar_lista_ventas(
    6,
    "CheesCake",
    3.00
)

print("PRUEBA DE EDICIÓN:")
print(exito)
print(mensaje)



from ventas_db import registrar_pedido

exito, mensaje = registrar_pedido(
    6,
    "Prueba Decimal",
    3,
    2.50,
    2.50
)

print("PRUEBA DE REGISTRO DE PEDIDO:")
print(exito)
print(mensaje)

from ventas_db import registrar_abono

exito, mensaje = registrar_abono(7, 2.00, "YAPPY")

print("PRUEBA DE SEGUNDO ABONO:")
print(exito)
print(mensaje)


from ventas_db import consultar_resumen_pago

exito, resultado = consultar_resumen_pago(7)

print("PRUEBA DE RESUMEN DE PAGO:")
print(exito)
print(resultado)