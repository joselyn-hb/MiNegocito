from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class HistorialRifasScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        pantalla = BoxLayout(orientation='vertical', padding=20, spacing=15)

        titulo = Label(text='Historial de rifas', font_size=32, size_hint_y=None, height=60)
        pantalla.add_widget(titulo)

        mensaje = Label(text='Historial de rifas:', font_size=18)
        pantalla.add_widget(mensaje)
        boton_volver = Button(text='Volver', font_size=18, size_hint_y=None, height=50)

        pantalla.add_widget(boton_volver)

        boton_volver.bind(on_press=lambda x: setattr(self.manager, 'current', 'chance'))
        self.add_widget(pantalla)
