from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

from rifas_db import listar_historial_rifas


class HistorialRifasScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        pantalla = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=12
        )

        titulo = Label(
            text="Historial de Rifas",
            font_size=28,
            size_hint_y=None,
            height=55
        )
        pantalla.add_widget(titulo)

        self.lista = BoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint_y=None
        )
        self.lista.bind(
            minimum_height=self.lista.setter("height")
        )

        desplazamiento = ScrollView()
        desplazamiento.add_widget(self.lista)
        pantalla.add_widget(desplazamiento)

        boton_volver = Button(
            text="Volver a Rifas",
            size_hint_y=None,
            height=50
        )
        boton_volver.bind(
            on_press=lambda instancia:
                setattr(self.manager, "current", "rifas")
        )
        pantalla.add_widget(boton_volver)

        self.add_widget(pantalla)

    def on_enter(self, *args):
        self.lista.clear_widgets()

        rifas = listar_historial_rifas()

        if not rifas:
            self.lista.add_widget(
                Label(
                    text="No hay rifas finalizadas todavía.",
                    size_hint_y=None,
                    height=60
                )
            )
            return

        for rifa in rifas:
            nombre = rifa.get("nombre") or "Sin nombre"
            estado = rifa.get("estado") or "Sin estado"
            fecha = rifa.get("fecha_sorteo") or "Sin fecha"
            precio = rifa.get("precio_numero") or 0

            detalle = (
                f"{nombre}\n"
                f"Estado: {estado}\n"
                f"Fecha del sorteo: {fecha}\n"
                f"Precio por número: B/. {precio}"
            )

            self.lista.add_widget(
                Label(
                    text=detalle,
                    size_hint_y=None,
                    height=105
                )
            )


  