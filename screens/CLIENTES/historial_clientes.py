from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

from clientes_db import listar_clientes


class HistorialClienteScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        pantalla = BoxLayout(orientation="vertical", padding=20, spacing=15)

        titulo = Label(
            text="Historial de Clientes",
            font_size=32,
            size_hint_y=None,
            height=60,
        )
        pantalla.add_widget(titulo)

        self.lista_clientes = BoxLayout(
            orientation="vertical",
            spacing=8,
            size_hint_y=None,
        )
        self.lista_clientes.bind(
            minimum_height=self.lista_clientes.setter("height")
        )

        desplazamiento = ScrollView()
        desplazamiento.add_widget(self.lista_clientes)
        pantalla.add_widget(desplazamiento)

        boton_volver = Button(
            text="Volver",
            font_size=18,
            size_hint_y=None,
            height=50,
        )
        pantalla.add_widget(boton_volver)
        boton_volver.bind(
            on_press=lambda x: setattr(self.manager, "current", "clientes")
        )

        self.add_widget(pantalla)

    def on_enter(self):
        self.cargar_historial()

    def cargar_historial(self):
        self.lista_clientes.clear_widgets()
        clientes = listar_clientes()

        if not clientes:
            self.lista_clientes.add_widget(
                Label(
                    text="Todavía no hay clientes registrados",
                    size_hint_y=None,
                    height=50,
                )
            )
            return

        for cliente in clientes:
            telefono = cliente["telefono"] or "sin teléfono"
            correo = cliente["correo"] or "sin correo"

            tarjeta = Label(
                text=(
                    f"Cliente: {cliente['nombre']}\n"
                    f"Teléfono: {telefono}\n"
                    f"Correo: {correo}"
                ),
                font_size=16,
                size_hint_y=None,
                height=90,
                halign="left",
                valign="middle",
            )
            tarjeta.bind(
                size=lambda widget, size: setattr(
                    widget, "text_size", (size[0] - 20, None)
                )
            )
            self.lista_clientes.add_widget(tarjeta)
