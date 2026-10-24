from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import  Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class NuevaListaScreen(Screen):
    def __init__(self, **kwargs): #inicializa correctamente la pantalla 
        super().__init__(**kwargs)

        pantalla = BoxLayout(orientation='vertical', padding=20, spacing=15) #contenedor principal de la pantalla, que contiene todos los elementos de la pantalla
        
        titulo = Label(text='Nueva lista', font_size=32, size_hint_y=None, height=60) #titulo de la pantalla
        pantalla.add_widget(titulo) #agrega el titulo a la pantalla

        mensaje = Label(text='Ingrese el nombre de la nueva lista:', font_size=18) #mensaje que indica al usuario que ingrese el nombre de la nueva lista
        pantalla.add_widget(mensaje) #agrega el mensaje a la pantalla
        boton_volver = Button(text='Volver', font_size=18, size_hint_y=None, height=50) #botónque permite volver a la pantalla anterior
        
        pantalla.add_widget(boton_volver) #agrega el botón de volver a la pantalla

        boton_volver.bind(on_press=lambda x: setattr(self.manager, 'current', 'chance'))  # Cambia a la pantalla de Mis Ventas al presionar el botón
        self.add_widget(pantalla) #agrega el contenedor principal a la pantalla
    