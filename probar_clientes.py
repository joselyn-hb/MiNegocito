from clientes_db import registrar_cliente, listar_clientes

print("=== PRUEBA DE CLIENTES ===")

nombre = input("Nombre del cliente de prueba: ").strip()
telefono = input("Teléfono (opcional): ").strip()
correo = input("Correo (opcional): ").strip()

resultado = registrar_cliente(
    nombre=nombre,
    telefono=telefono or None,
    correo=correo or None
)

if resultado:
    print("\n=== CLIENTES REGISTRADOS ===")

    clientes = listar_clientes()

    for cliente in clientes:
        print(
            f"ID: {cliente['id_cliente']} | "
            f"Nombre: {cliente['nombre']} | "
            f"Teléfono: {cliente['telefono']}"
        )
else:
    print("No se pudo registrar el cliente.")