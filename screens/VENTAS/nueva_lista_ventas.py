from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from decimal import Decimal, InvalidOperation

from ventas_db import crear_lista_ventas

class NuevaListaVentasScreen(Screen):
    def __init__(self, **kwargs): #inicializa correctamente la pantalla 
        super().__init__(**kwargs)

        pantalla = BoxLayout(orientation='vertical', padding=20, spacing=15)

        titulo = Label(
            text='Nueva Lista de Ventas',
            font_size=32,
            size_hint_y=None,
            height=60,
        )
        pantalla.add_widget(titulo)

        mensaje = Label(
            text='Ingrese el nombre de la nueva lista de ventas:',
            font_size=18,
        )
        pantalla.add_widget(mensaje)

        self.entrada_nombre = TextInput(
            hint_text="Ejemplo: Postres",
            multiline=False,
            size_hint_y=None,
            height=50,
        )
        pantalla.add_widget(self.entrada_nombre)

        self.entrada_precio = TextInput(
            hint_text="ejemplo:2.00",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=50,
        )
        pantalla.add_widget(self.entrada_precio)

        boton_guardar = Button(
            text="Guardar lista",
            font_size=18,
            size_hint_y=None,
            height=50,
        )
        boton_guardar.bind(on_press=self.guardar_lista)
        pantalla.add_widget(boton_guardar)

        boton_volver = Button(
            text='Volver',
            font_size=18,
            size_hint_y=None,
            height=50,
        )
        boton_volver.bind(
            on_press=lambda _: setattr(self.manager, 'current', 'mis_ventas')
        )
        pantalla.add_widget(boton_volver)
        self.add_widget(pantalla)

    def guardar_lista(self, _):
        
        nombre = self.entrada_nombre.text.strip()

        precio_texto = self.entrada_precio.text.strip()
        
        if not nombre:
            self.mostrar_mensaje("Escribe el nombre de la lista.")
            return

        if not precio_texto:
            self.mostrar_mensaje("Escribe el precio unitario de la lista.")
            return

        try:
            precio = Decimal(precio_texto)
            if precio <= 0:
                self.mostrar_mensaje("El precio unitario debe ser mayor que cero.")
                return

            if precio.as_tuple().exponent < -2:
                self.mostrar_mensaje("El precio unitario no puede tener más de dos decimales.")
                return

            exito, mensaje = crear_lista_ventas(nombre, precio)
            self.mostrar_mensaje(mensaje)

            if exito:
                self.entrada_nombre.text = ""
                self.entrada_precio.text = ""

        except InvalidOperation:
            self.mostrar_mensaje("El precio unitario debe ser un número válido.")

        


    def mostrar_mensaje(self, mensaje):
        contenido = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10,
        )
        contenido.add_widget(Label(text=mensaje))

        boton_aceptar = Button(
            text="Aceptar",
            size_hint_y=None,
            height=45,
        )
        contenido.add_widget(boton_aceptar)

        ventana = Popup(
            title="Mi Negocito",
            content=contenido,
            size_hint=(0.8, 0.4),
        )
        boton_aceptar.bind(on_press=lambda _: ventana.dismiss())
        ventana.open()
        