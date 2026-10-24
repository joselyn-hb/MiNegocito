from kivy.uix.screenmanager import Screen #crea una pantalla que pueda ser manejada por el ScreenManager (gestor de pantallas)
from kivy.uix.boxlayout import BoxLayout # ES EL CONTENEDOR QUE USAMOS PARA ORGANIZAR LOS ELEMENTOS DE LA PANTALLA CHANCE
from kivy.uix.label import Label #PERMOYE COLOCAR TITULO Y TEXTOS DENTRO DE LA PANTALLA
from kivy.uix.button import Button #PERMITE COLOCAR BOTONES DENTRO DE LA PANTALLA

class MisVentasScreen(Screen): #CREA LA PANTALLA MIS VENTAS QUE PUEDE SER MANEJADA POR EL GESTOR DE PANTALLAS
    def __init__(self, **kwargs): #INICIALIZA LA PANTALLA MIS VENTAS Y SUS ELEMENTOS
        super().__init__(**kwargs)
        pantalla = BoxLayout(orientation='vertical', padding=20, spacing=15) #CREA UN CONTENEDOR VERTICAL PARA ORGANIZAR LOS ELEMENTOS DE LA PANTALLA

        titulo = Label(text=' MIS VENTAS', font_size=32, size_hint_y=None, height=60) #CREA EL TITULO DE LA PANTALLA
        pantalla.add_widget(titulo) #AGREGA EL TITULO AL CONTENEDOR
        mensaje = Label(text='¡Gestiona tus ventas de manera sencilla!', font_size=18)
        pantalla.add_widget(mensaje) #AGREGA EL MENSAJE AL CONTENEDOR

        # boton para crear una nueva lista de ventas
        boton_nueva_lista_ventas = Button(text='Nueva Lista de Ventas', font_size=18, size_hint_y=None, height=50) #CREA UN BOTON PARA VER LAS VENTAS
        pantalla.add_widget(boton_nueva_lista_ventas) #AGREGA EL BOTON AL CONTEN
        boton_nueva_lista_ventas.bind(on_press=lambda x: setattr(self.manager, 'current', 'nueva_lista_ventas'))  # CAMBIA A LA PANTALLA DE NUEVA LISTA AL PRESIONAR EL BOTON

        # boton para registrar ventas diarias individuales
        boton_registrar_ventas = Button(text='Registrar Ventas Individuales', font_size=18, size_hint_y=None, height=50) #CREA UN BOTON PARA REGISTRAR VENTAS DIARIAS
        pantalla.add_widget(boton_registrar_ventas) #AGREGA EL BOTON AL CONTENEDOR
        boton_registrar_ventas.bind(on_press=lambda x: setattr(self.manager, 'current', 'registrar_ventas'))  # CAMBIA A LA PANTALLA DE REGISTRAR VENTAS AL PRESIONAR EL BOTON

        # boton historial de ventas 
        boton_historial_ventas = Button(text='Historial de Ventas', font_size=18, size_hint_y=None, height=50) #CREA UN BOTON PARA CONSULTAR VENTAS
        pantalla.add_widget(boton_historial_ventas) #AGREGA EL BOTON AL CONTENEDOR
        boton_historial_ventas.bind(on_press=lambda x: setattr(self.manager, 'current', 'historial_ventas'))  # CAMBIA A LA PANTALLA DE HISTORIAL DE VENTAS AL PRESIONAR EL BOTONñ

      
        # boton para volver a la pantalla de inicio
        boton_volver = Button(text='Atrás', font_size=18, size_hint_y=None, height=50) #CREA UN BOTON PARA VOLVER A LA PANTALLA ANTERIOR
        pantalla.add_widget(boton_volver) #AGREGA EL BOTON AL CONTENEDOR
        boton_volver.bind(on_press=lambda x: setattr(self.manager, 'current', 'inicio'))  # CAMBIA A LA PANTALLA DE INICIO AL PRESIONAR EL BOTON
        self.add_widget(pantalla) #AGREGA EL CONTENEDOR A LA PANTALLA MIS VENTAS