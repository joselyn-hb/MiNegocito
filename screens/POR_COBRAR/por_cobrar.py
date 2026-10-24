from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button


class PorCobrarScreen(Screen): #indica que Rifas es una pantalla completa de la aplicación 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pantalla = BoxLayout(orientation='vertical', padding=20, spacing=15)
        

        titulo = Label(text=' POR COBRAR', font_size=32, size_hint_y=None, height=60)
        mensaje = Label(text='¡Gestiona los pagos pendientes de tus clientes!', font_size=18)

        pantalla.add_widget(titulo)
        pantalla.add_widget(mensaje)
       
       
        # BOTONES DE POR COBRAR
        
        boton_volver = Button(text='Atrás', font_size=20, size_hint_y=None, height=50)
        boton_volver.bind(on_press=lambda x: setattr(self.manager, 'current', 'inicio'))  # Cambia a la pantalla de inicio al presionar el botón


       
        pantalla.add_widget(boton_volver)
        self.add_widget(pantalla)