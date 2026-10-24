from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button


class ClientesScreen(Screen): #indica que Rifas es una pantalla completa de la aplicación 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pantalla = BoxLayout(orientation='vertical', padding=20, spacing=15)
        

        titulo = Label(text=' CLIENTES', font_size=32, size_hint_y=None, height=60)
        mensaje = Label(text='¡Gestiona tus clientes de manera sencilla!', font_size=18)
        pantalla.add_widget(titulo)
        pantalla.add_widget(mensaje)
        ######################## BOTONES DE CLIENTES ####################################################
        boton_nuevo_cliente = Button(text='Nuevo Cliente', font_size=18, size_hint_y=None, height=50)
        boton_nuevo_cliente.bind(on_press=lambda x: setattr(self.manager, 'current', 'nuevo_cliente'))  # Cambia a la pantalla de nuevo cliente al presionar el botón
        pantalla.add_widget(boton_nuevo_cliente)

        boton_mis_clientes = Button(text='Mis Clientes', font_size=18, size_hint_y=None, height=50)
        boton_mis_clientes.bind(on_press=lambda x: setattr(self.manager, 'current', 'mis_clientes'))  # Cambia a la pantalla de mis clientes al presionar el botón
        pantalla.add_widget(boton_mis_clientes)

        boton_buscar_cliente = Button(text='Buscar Cliente', font_size=18, size_hint_y=None, height=50)
        boton_buscar_cliente.bind(on_press=lambda x: setattr(self.manager, 'current', 'buscar_cliente'))  # Cambia a la pantalla de buscar cliente al presionar el botón
        pantalla.add_widget(boton_buscar_cliente)

        boton_historial_clientes = Button(text='Historial de Clientes', font_size=18, size_hint_y=None, height=50)
        boton_historial_clientes.bind(on_press=lambda x: setattr(self.manager, 'current', 'historial_clientes'))  # Cambia a la pantalla de historial de clientes al presionar el botón
        pantalla.add_widget(boton_historial_clientes)

        boton_volver = Button(text='Atrás', font_size=18, size_hint_y=None, height=50)
        boton_volver.bind(on_press=lambda x: setattr(self.manager, 'current', 'inicio'))  # Cambia a la pantalla de inicio al presionar el botón
        pantalla.add_widget(boton_volver)

        self.add_widget(pantalla)