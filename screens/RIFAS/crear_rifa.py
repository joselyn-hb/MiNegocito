from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from datetime import datetime
from rifas_db import crear_rifa

class CrearRifaScreen(Screen):
    def __init__(self, **kwargs): #inicializa correctamente la pantalla 
        super().__init__(**kwargs)

        pantalla = BoxLayout(orientation='vertical', padding=20, spacing=15) #contenedor principal de la pantalla, que contiene todos los elementos de la pantalla
        
        titulo = Label(text='Crear Rifa', font_size=32, size_hint_y=None, height=60) #titulo de la pantalla
        pantalla.add_widget(titulo) #agrega el titulo a la pantalla

        mensaje = Label(text='Ingrese el nombre de la nueva rifa:', font_size=18) #mensaje que indica al usuario que ingrese el nombre de la nueva lista
        pantalla.add_widget(mensaje) #agrega el mensaje a la pantalla


        self.entrada_nombre = TextInput(
            hint_text="Nombre de la rifa*",
            multiline=False,
            size_hint_y=None,
            height=50,
        )
        pantalla.add_widget(self.entrada_nombre)

        self.entrada_descripcion = TextInput(
            hint_text="descripción (opcional)",
            multiline=True,
            size_hint_y=None,
            height=80,
        )
        pantalla.add_widget(self.entrada_descripcion)

        self.entrada_precio = TextInput(
            hint_text="Precio por número (ej. 1.00)",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=50,
        )
        pantalla.add_widget(self.entrada_precio)

        self.entrada_fecha = TextInput(
            hint_text="Fecha del sorteo (AAAA-MM-DD, opcional)",
            multiline=False,
            input_type="text",
            size_hint_y=None,
            height=50,
        )
        pantalla.add_widget(self.entrada_fecha)

        self.mensaje_resultado = Label(
            text="",
            size_hint_y=None,
            height=60,
        )
        pantalla.add_widget(self.mensaje_resultado)

        boton_guardar = Button(text="Guardar rifa", font_size=18, size_hint_y=None, height=50)
        boton_guardar.bind(on_press=self.guardar_rifa)
        pantalla.add_widget(boton_guardar)

        boton_volver = Button(
            text="Volver", font_size=18, size_hint_y=None, height=50
        )  # botón que permite volver a la pantalla anterior
        pantalla.add_widget(boton_volver)
        boton_volver.bind(
            on_press=lambda x: setattr(self.manager, "current", "rifas")
        )

        self.add_widget(pantalla)

    def guardar_rifa(self, instancia):
        nombre = self.entrada_nombre.text.strip()
        descripcion = self.entrada_descripcion.text.strip()
        precio_texto = self.entrada_precio.text.strip()
        fecha_texto = self.entrada_fecha.text.strip()

        if not nombre:
            self.mensaje_resultado.text = "Escribe el nombre de la rifa."
            return

        if not precio_texto:
            self.mensaje_resultado.text = "Escribe el precio por número."
            return

        try:
            precio = float(precio_texto)
            if precio <= 0:
                self.mensaje_resultado.text = "El precio debe ser mayor que cero."
                return
        except ValueError:
            self.mensaje_resultado.text = "El precio no es válido."
            return

        fecha_sorteo = None
        if fecha_texto:
            try:
                fecha_sorteo = datetime.strptime(fecha_texto, "%Y-%m-%d").date()
            except ValueError:
                self.mensaje_resultado.text = (
                    "Fecha inválida. Usa AAAA-MM-DD, por ejemplo 2026-12-13."
                )
                return

        exito, mensaje = crear_rifa(
            nombre, descripcion or None, precio, fecha_sorteo
        )
        self.mensaje_resultado.text = mensaje

        if exito:
            self.entrada_nombre.text = ""
            self.entrada_descripcion.text = ""
            self.entrada_precio.text = ""
            self.entrada_fecha.text = ""