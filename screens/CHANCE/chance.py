from kivy.uix.screenmanager import Screen #crea una pantalla que pueda ser manejada por el ScreenManager (gestor de pantallas)
from kivy.uix.boxlayout import BoxLayout # ES EL CONTENEDOR QUE USAMOS PARA ORGANIZAR LOS ELEMENTOS DE LA PANTALLA CHANCE
from kivy.uix.label import Label #PERMOYE COLOCAR TITULO Y TEXTOS DENTRO DE LA PANTALLA
from kivy.uix.button import Button #PERMITE COLOCAR BOTONES DENTRO DE LA PANTALLA


class ChanceScreen(Screen): #CREA LA PANTALLA CHANCE QUE PUEDE SER MANEJADA POR EL GESTOR DE PANTALLAS
    def __init__(self, **kwargs): #INICIALIZA LA PANTALLA CHANCE Y SUS ELEMENTOS
        super().__init__(**kwargs)
        pantalla = BoxLayout(orientation='vertical', padding=20, spacing=15) #CREA UN CONTENEDOR VERTICAL PARA ORGANIZAR LOS ELEMENTOS DE LA PANTALLA

        titulo = Label(text=' CHANCE', font_size=32, size_hint_y=None, height=60) #CREA EL TITULO DE LA PANTALLA
    

        pantalla.add_widget(titulo) #AGREGA EL TITULO AL CONTENEDOR

        boton_nueva_lista=Button(text='Nueva Lista', font_size=18, size_hint_y=None, height=50) #CREA UN BOTON PARA CREAR UNA NUEVA LISTA
        boton_listas_activas=Button(text='Listas Activas', font_size=18, size_hint_y=None, height=50) #CREA UN BOTON PARA VER LAS LISTAS ACTIVAS
        boton_historial_listas=Button(text='Historial de Listas', font_size=18, size_hint_y=None, height=50) #CREA UN BOTON PARA VER EL HISTORIAL DE LISTAS
        boton_volver = Button(text='Atrás', font_size=18, size_hint_y=None, height=50) #CREA UN BOTON PARA VOLVER A LA PANTALLA ANTERIOR
        pantalla.add_widget(boton_nueva_lista) #AGREGA EL BOTON AL CONTENEDOR
        pantalla.add_widget(boton_listas_activas) #AGREGA EL BOTON AL CONTENEDOR
        pantalla.add_widget(boton_historial_listas) #AGREGA EL BOTON AL CONTENEDOR
        pantalla.add_widget(boton_volver) #AGREGA EL BOTON AL CONTENEDOR
        
        boton_volver.bind(on_press=lambda x: setattr(self.manager, 'current', 'inicio'))  # CAMBIA A LA PANTALLA DE INICIO AL PRESIONAR EL BOTON
        self.add_widget(pantalla) #AGREGA EL CONTENEDOR A LA PANTALLA CHANCE

        boton_nueva_lista.bind(on_press=lambda x: setattr(self.manager, 'current', 'nueva_lista'))  # CAMBIA A LA PANTALLA DE NUEVA LISTA AL PRESIONAR EL BOTON
        boton_listas_activas.bind(on_press=lambda x: setattr(self.manager, 'current', 'listas_activas'))  # CAMBIA A LA PANTALLA DE LISTAS ACTIVAS AL PRESIONAR EL BOTON
        boton_historial_listas.bind(on_press=lambda x: setattr(self.manager, 'current', 'historial_listas'))  # CAMBIA A LA PANTALLA DE HISTORIAL DE LISTAS AL PRESIONAR EL BOTON