from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from ventas_db import (consultar_detalle_pedido,
    consultar_resumen_pago,
    registrar_abono,
    actualizar_estado_entrega
)

class DetallePedidoScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.id_venta = None
        self.pantalla = BoxLayout(orientation="vertical",padding=20,spacing=10)

        self.titulo = Label(text="Detalle del Pedido", font_size=26, size_hint_y=None, height=50)

        self.pantalla.add_widget(self.titulo)

        self.cliente = Label(text="Cliente: ",font_size=18,size_hint_y=None,height=40)

        self.cantidad = Label(text="Cantidad: ", font_size=18, size_hint_y=None,height=40)

        self.precio = Label(text="Precio unitario:", font_size=18, size_hint_y=None, height=40)

        self.total = Label(text="Total: B/. 0.00", font_size=18, size_hint_y=None, height=40
        )

        self.abonado = Label(text="Abonado: B/. 0.00", font_size=18, size_hint_y=None, height=40
        )

        self.saldo = Label(text="Saldo pendiente: B/. 0.00", font_size=18, size_hint_y=None, height=40)

        self.pantalla.add_widget(self.cliente)
        self.pantalla.add_widget(self.cantidad)
        self.pantalla.add_widget(self.precio)
        self.pantalla.add_widget(self.total)
        self.pantalla.add_widget(self.abonado)
        self.pantalla.add_widget(self.saldo)

        self.boton_abono = Button(text="Registrar abono", size_hint_y=None,height=50)
        self.boton_abono.bind(on_press=self.abrir_formulario_abono)
        self.pantalla.add_widget(self.boton_abono)

        self.boton_estado = Button(text="Cambiar estado de entrega", size_hint_y=None,height=50)
        self.boton_estado.bind(on_press=self.abrir_cambiar_estado)
        self.pantalla.add_widget(self.boton_estado)

        self.boton_volver = Button(text="Volver a pediidos", size_hint_y=None,height=50)
        self.boton_volver.bind(on_press=lambda instancia: setattr(self.manager, "current", "pedidos_lista"))
        self.pantalla.add_widget(self.boton_volver)

    
        self.add_widget(self.pantalla)

    def cargar_pedido(self, id_venta):

        self.id_venta = id_venta

        exito, detalle = consultar_detalle_pedido(id_venta)

        if not exito:
            self.mostrar_mensaje(detalle)
            return

        exito_pago, resumen = consultar_resumen_pago(id_venta)

        if not exito_pago:
            self.mostrar_mensaje(resumen)
            return

        self.cliente.text = f"Cliente: {detalle['nombre_cliente']}"
        self.cantidad.text = f"Cantidad: {detalle['cantidad']} unidades"

        self.precio.text = (
            f"Precio unitario: B/. {detalle['precio_unitario']:.2f}"
        )

        self.total.text = f"Total: B/. {resumen['total']:.2f}"
        self.abonado.text = f"Abonado: B/. {resumen['abonado']:.2f}"
        self.saldo.text = f"Saldo pendiente: B/. {resumen['saldo']:.2f}"

        self.estado_entrega = detalle["estado_entrega"]


    def abrir_formulario_abono(self, instancia):

        contenido = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        monto_input = TextInput(
            hint_text="Monto del abono",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=45
        )

        metodo_input = TextInput(
            hint_text="Método: EFECTIVO, YAPPY, TRANSFERENCIA, TARJETA u OTRO",
            multiline=False,
            size_hint_y=None,
            height=45
        )

        boton_guardar = Button(
            text="Guardar Abono",
            size_hint_y=None,
            height=45
        )

        contenido.add_widget(monto_input)
        contenido.add_widget(metodo_input)
        contenido.add_widget(boton_guardar)

        popup = Popup(
            title="Registrar Abono",
            content=contenido,
            size_hint=(0.9, 0.45)
        )

        def guardar_abono(instancia):

            if not monto_input.text or not metodo_input.text:
                self.mostrar_mensaje("Completa el monto y el método de pago.")
                return

            exito, mensaje = registrar_abono(
                self.id_venta,
                monto_input.text,
                metodo_input.text
            )

            self.mostrar_mensaje(mensaje)

            if exito:
                popup.dismiss()
                self.cargar_pedido(self.id_venta)

        boton_guardar.bind(on_press=guardar_abono)

        popup.open()


    def abrir_cambiar_estado(self, instancia):

        contenido = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        estado_input = TextInput(
            text=self.estado_entrega,
            hint_text="PENDIENTE, ENTREGADO o CANCELADO",
            multiline=False,
            size_hint_y=None,
            height=45
        )

        boton_guardar = Button(
            text="Guardar Estado",
            size_hint_y=None,
            height=45
        )

        contenido.add_widget(estado_input)
        contenido.add_widget(boton_guardar)

        popup = Popup(
            title="Cambiar Estado de Entrega",
            content=contenido,
            size_hint=(0.9, 0.35)
        )

        def guardar_estado(instancia):

            nuevo_estado = estado_input.text.strip().upper()

            if nuevo_estado not in ("PENDIENTE", "ENTREGADO", "CANCELADO"):
                self.mostrar_mensaje(
                    "Estado no válido. Utiliza PENDIENTE, ENTREGADO o CANCELADO."
                )
                return

            exito, mensaje = actualizar_estado_entrega(
                self.id_venta,
                nuevo_estado
            )

            self.mostrar_mensaje(mensaje)

            if exito:
                popup.dismiss()
                self.cargar_pedido(self.id_venta)

        boton_guardar.bind(on_press=guardar_estado)
        popup.open()

    def mostrar_mensaje(self, mensaje):
        contenido = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        etiqueta = Label(
            text=str(mensaje),
            halign="center",
            valign="middle"
        )

        boton_cerrar = Button(
            text="Aceptar",
            size_hint_y=None,
            height=45
        )

        contenido.add_widget(etiqueta)
        contenido.add_widget(boton_cerrar)

        popup = Popup(
            title="Información",
            content=contenido,
            size_hint=(0.85, 0.35)
        )

        boton_cerrar.bind(on_press=popup.dismiss)
        popup.open()