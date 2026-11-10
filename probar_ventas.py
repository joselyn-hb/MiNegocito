from ventas_db import listar_ventas_individuales

ventas = listar_ventas_individuales()

print("\n===== HISTORIAL DE VENTAS =====")

if ventas:
    for venta in ventas:
        print("-----------------------------")
        print("Número:", venta["id_ventas"])
        print("Cliente:", venta["nombre_cliente"])
        print("Fecha:", venta["fecha_venta"])
        print("Total: B/.", venta["total"])
else:
    print("No hay ventas registradas.")