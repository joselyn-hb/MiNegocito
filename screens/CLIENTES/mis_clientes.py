from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import  Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from clientes_db import listar_clientes
from kivy.uix.scrollview import ScrollView #para desplazarse verticalmente cuando la lista es larga

class MisClientesScreen(Screen):
    def __init__(self, **kwargs): #inicializa correctamente la pantalla 
        super().__init__(**kwargs)

        pantalla = BoxLayout(orientation='vertical', padding=20, spacing=15) #contenedor principal de la pantalla, que contiene todos los elementos de la pantalla
        
        titulo = Label(text='Mis Clientes', font_size=32, size_hint_y=None, height=60) #titulo de la pantalla
        pantalla.add_widget(titulo) #agrega el titulo a la pantalla

        mensaje = Label(text='Lista de Clientes:', font_size=18) #mensaje que indica al usuario que ingrese el nombre del nuevo cliente
        pantalla.add_widget(mensaje) #agrega el mensaje a la pantalla

        ###  CONTENEDOR PARA MOSTRARLOS CLIENTES  ####
        self.lista_clientes = BoxLayout(
            orientation ="vertical", # organiza los clientes uno debajo del otro
            spacing=8, # espacio entre los registros
            size_hint_y=None # permite que el contenedor ajuste su altura según el contenido
            )

           # minimum_height hace que el contenedor crezca cuando añadimos mas clientes
        self.lista_clientes.bind(minimum_height=self.lista_clientes.setter("height"))

        # AREA DESPLAZABLE PARA LA LISTA
        desplazamiento=ScrollView()
        desplazamiento.add_widget(self.lista_clientes)
        pantalla.add_widget(desplazamiento)

        boton_volver = Button(text='Volver', font_size=18, size_hint_y=None, height=50) #botónque permite volver a la pantalla anterior
        pantalla.add_widget(boton_volver) #agrega el botón de volver a la pantalla
        boton_volver.bind(on_press=lambda x: setattr(self.manager, 'current', 'clientes'))  # Cambia a la pantalla clientes al presionar el botón
       
        self.add_widget(pantalla) #agrega el contenedor principal a la pantalla

    def on_enter(self): #actualiza la lista cada vez que se abre la pantalla
        self.cargar_clientes()

    def cargar_clientes(self): # limpia los registros anteriores para evitar duplicados
        self.lista_clientes.clear_widgets()
        clientes = listar_clientes()

        if not clientes:
            self.lista_clientes.add_widget(
                Label(text="Aún no hay clientes registrados.",
                      font_size=16,
                      size_hint_y=None,
                      height=50 ) )
            return
        for cliente in clientes:
            telefono = cliente["telefono"] or "sin telefono"
            correo = cliente ["correo"] or "sin correo"
            datos = (
    f"{cliente['nombre']}\n"
    f"Teléfono: {telefono}\n"
    f"Correo: {correo}"
)

            
            tarjeta = Label(
                text=datos,
                font_size=16,
                size_hint_y=None,
                height=90,
                halign="left",
                valign="middle"
            )

            tarjeta.bind(
                size=lambda widget, size:setattr(
                    widget,"text_size", (size[0]-20, None)
                    ))
            self.lista_clientes.add_widget(tarjeta)

