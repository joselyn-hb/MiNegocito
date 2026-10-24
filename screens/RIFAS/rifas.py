from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button


class RifasScreen(Screen): #indica que Rifas es una pantalla completa de la aplicación 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pantalla = BoxLayout(orientation='vertical', padding=20, spacing=15)
        

        titulo = Label(text=' RIFAS', font_size=32, size_hint_y=None, height=60)
        mensaje = Label(text='¡Gestiona tus rifas de manera sencilla!', font_size=18)

        # BOTONES DE RIFAS
        boton_crear_rifa = Button(text='Crear Rifa', font_size=20, size_hint_y=None, height=50)
        boton_crear_rifa.bind(on_press=lambda x: setattr(self.manager, 'current', 'crear_rifa'))
        
        boton_rifas_activas = Button(text='Rifas Activas', font_size=20, size_hint_y=None, height=50)
        boton_rifas_activas.bind(on_press=lambda x: setattr(self.manager, 'current', 'rifas_activas'))
        
        boton_historial_rifas = Button(text='Historial de Rifas', font_size=20, size_hint_y=None, height=50)
        boton_historial_rifas.bind(on_press=lambda x: setattr(self.manager, 'current', 'historial_rifas'))

        boton_volver = Button(text='Atrás', font_size=20, size_hint_y=None, height=50)
        boton_volver.bind(on_press=lambda x: setattr(self.manager, 'current', 'inicio'))  # Cambia a la pantalla de inicio al presionar el botón
        
     
        boton_historial_rifas.bind(on_press=lambda x: setattr(self.manager, 'current', 'historial_rifas'))

        pantalla.add_widget(titulo)
        pantalla.add_widget(mensaje)
        pantalla.add_widget(boton_crear_rifa)
        pantalla.add_widget(boton_rifas_activas)
        pantalla.add_widget(boton_historial_rifas)
        pantalla.add_widget(boton_volver)
        self.add_widget(pantalla)