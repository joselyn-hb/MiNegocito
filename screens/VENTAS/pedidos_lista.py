from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

from ventas_db import (registrar_pedido, listar_pedidos_lista, consultar_resumen_pago, registrar_abono, actualizar_estado_entrega)

class PedidosListaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.pantalla = BoxLayout(orientation='vertical', padding=20, spacing=10)

        #encabezado de la pantalla
        self.titulo = Label(text='Nombre de la Lista', font_size=26, size_hint_y=None, height=50)

        self.estado = Label(text='Estado: ACTIVA', size_hint_y=None, height=35)

        self.total_pedidos = Label(text='Pedidos Registrados: 0', size_hint_y=None, height=40)

        self.pantalla.add_widget(self.titulo)
        self.pantalla.add_widget(self.estado)   
        self.pantalla.add_widget(self.total_pedidos)

        #ESPACIO DONDE APARECERÁN LOS PEDIDOS REGISTRADOS
        desplazamiento = ScrollView()
        self.contenedor_pedidos = BoxLayout(orientation="vertical", spacing=10, size_hint_y=None)
        self.contenedor_pedidos.bind(minimum_height=self.contenedor_pedidos.setter("height"))
        desplazamiento.add_widget(self.contenedor_pedidos)

        self.pantalla.add_widget(desplazamiento)

        #BOTÓN PARA REGISTRAR UN NUEVO PEDIDO
        self.boton_registrar = Button(text="+ Registrar Nuevo Pedido", size_hint_y=None, height=50)
        self.boton_registrar.bind(on_press=self.abrir_formulario_pedido )
        self.pantalla.add_widget(self.boton_registrar)

        #BOTÓN PARA VOLVER A LA PANTALLA ANTERIOR
        boton_volver = Button(text="Volver a Listas", size_hint_y=None, height=50)
        boton_volver.bind(on_press=lambda instancia: setattr(self.manager, "current", "mis_ventas"))

        self.pantalla.add_widget(boton_volver)

        self.add_widget(self.pantalla)

    def cargar_lista(self, lista):

        self.id_lista = lista["id_lista"]
        self.precio_lista = float(lista["precio_unitario"])

        self.titulo.text = lista["nombre"]
        self.estado.text = f"Estado: {lista['estado']}"

        # Limpiar pedidos anteriores
        self.contenedor_pedidos.clear_widgets()

        # Consultar pedidos guardados en MySQL
        exito, pedidos = listar_pedidos_lista(self.id_lista)

        if not exito:
            self.total_pedidos.text = "No se pudieron cargar los pedidos"
            self.mostrar_mensaje(pedidos)
            return

        self.total_pedidos.text = f"Pedidos Registrados: {len(pedidos)}"

        if not pedidos:
            self.contenedor_pedidos.add_widget(
                Label(
                    text="Todavía no hay pedidos registrados",
                    size_hint_y=None,
                    height=50
                )
            )
            return

        # Crear una tarjeta para cada pedido
        for id_venta, nombre, cantidad, total, estado in pedidos:

            tarjeta = BoxLayout(
                orientation="vertical",
                padding=12,
                spacing=5,
                size_hint_y=None,
                height=180
            )

            tarjeta.add_widget(
                Label(
                    text=str(nombre),
                    bold=True,
                    size_hint_y=None,
                    height=30
                )
            )

            tarjeta.add_widget(
                Label(
                    text=f"Cantidad: {cantidad} unidades",
                    size_hint_y=None,
                    height=25
                )
            )

            tarjeta.add_widget(
                Label(
                    text=f"Total: B/. {float(total):.2f}",
                    size_hint_y=None,
                    height=30
                )
            )

            boton_abrir = Button(
                text="Ver detalles del pedido",
                            size_hint_y=None,
                            height=40)

            boton_abrir.bind(on_press=lambda instancia,
                            id=id_venta: self.abrir_pedido(id) )

            tarjeta.add_widget(boton_abrir)

            self.contenedor_pedidos.add_widget(tarjeta)


    def abrir_pedido(self, id_venta):
        self.pantalla = self.manager.get_screen("detalle_pedido")

        self.pantalla.cargar_pedido(id_venta)

        self.manager.current ="detalle_pedido"




    def abrir_formulario_pedido(self, instancia):
        # Aquí puedes abrir un popup o una nueva pantalla para registrar un nuevo pedido
        contenido = BoxLayout(orientation='vertical', padding=15, spacing=10)

        # Agrega campos de entrada para el nuevo pedido
        entrada_cliente= TextInput(hint_text="Nombre del Cliente", multiline=False,size_hint_y=None, height=45)
        entrada_cantidad = TextInput(hint_text="Cantidad", multiline=False, input_filter="int", size_hint_y=None, height=45)
        entrada_precio = TextInput(text=str(self.precio_lista), hint_text="Precio unitario", multiline=False, input_filter="float", size_hint_y=None, height=45)
        entrada_abono = TextInput(hint_text="Abono (opcional)", multiline=False, input_filter="float", size_hint_y=None, height=45)

        total = Label(text="Total: B/. 0.00")
        saldo = Label(text="Saldo Pendiente: B/. 0.00")

        def actualizar_totales(instancia=None):
            try:
                cantidad = int(entrada_cantidad.text or 0) 
                precio = float(entrada_precio.text or 0) 
                abono = float(entrada_abono.text or 0)

                importe = cantidad * precio
                pendiente = importe - abono

                total.text = f"Total: B/. {importe:.2f}"
                saldo.text = f"Saldo Pendiente: B/. {pendiente:.2f}"

            except ValueError:
                total.text = "Total: B/. 0.00"
                saldo.text = "Saldo Pendiente: B/. 0.00"


        entrada_cantidad.bind(on_text=actualizar_totales)
        entrada_precio.bind(on_text=actualizar_totales)
        entrada_abono.bind(on_text=actualizar_totales)


        contenido.add_widget(Label(text="Nombre del Cliente"))
        contenido.add_widget(entrada_cliente)

        contenido.add_widget(Label(text="Cantidad"))
        contenido.add_widget(entrada_cantidad)

        contenido.add_widget(Label(text="Precio unitario"))
        contenido.add_widget(entrada_precio)

        contenido.add_widget(Label(text="Abono (opcional)"))
        contenido.add_widget(entrada_abono)

        contenido.add_widget(total)
        contenido.add_widget(saldo)



        ventana = Popup(title="Registrar Nuevo Pedido", content=contenido, size_hint=(0.9, 0.85))

        boton_guardar = Button(text="Guardar Pedido", size_hint_y=None, height=50)
        contenido.add_widget(boton_guardar)

        boton_cancelar = Button(text="Cancelar", size_hint_y=None, height=50)
        contenido.add_widget(boton_cancelar)


        def guardar_pedido(instancia):
            nombre = entrada_cliente.text.strip()
            if not nombre:
                self.mostrar_mensaje("El nombre del cliente no puede estar vacío.")
                return
            try:
                cantidad = int(entrada_cantidad.text)
                precio = float(entrada_precio.text)
                abono = float(entrada_abono.text or 0)

                if cantidad <= 0 or precio <= 0:
                    raise ValueError
                if abono < 0 or abono > cantidad * precio:
                    self.mostrar_mensaje("El abono no puede ser mayor al total.")
                    return
            except ValueError:
                self.mostrar_mensaje("revisa la cantidad, el precio y el abono")

                return

            exito, mensaje = registrar_pedido(self.id_lista, nombre, cantidad, precio, abono)
            self.mostrar_mensaje(mensaje)
            if exito:
                ventana.dismiss()

            self.cargar_lista({"id_lista": self.id_lista, "precio_unitario": self.precio_lista, "nombre": self.titulo.text, "estado": self.estado.text.replace("Estado: ", "")})

        boton_guardar.bind(on_press=guardar_pedido)
        boton_cancelar.bind(on_press=ventana.dismiss)
        ventana.open()


    def mostrar_mensaje(self, mensaje):

        contenido = BoxLayout(
        orientation="vertical",
        padding=15,
        spacing=10
    )

        texto = Label(text=mensaje)

        boton_cerrar = Button(
            text="Aceptar",
            size_hint_y=None,
            height=45
        )

        contenido.add_widget(texto)
        contenido.add_widget(boton_cerrar)

        ventana = Popup(
            title="Información",
            content=contenido,
            size_hint=(0.85, 0.45)
        )

        boton_cerrar.bind(on_press=ventana.dismiss)

        ventana.open()