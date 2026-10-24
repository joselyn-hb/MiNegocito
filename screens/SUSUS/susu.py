from kivy.uix.screenmanager import Screen #crea una pantalla que pueda ser manejada por el ScreenManager (gestor de pantallas)
from kivy.uix.boxlayout import BoxLayout # ES EL CONTENEDOR QUE USAMOS PARA ORGANIZAR LOS ELEMENTOS DE LA PANTALLA CHANCE
from kivy.uix.label import Label #PERMOYE COLOCAR TITULO Y TEXTOS DENTRO DE LA PANTALLA
from kivy.uix.button import Button #PERMITE COLOCAR BOTONES DENTRO DE LA PANTALLA

class SusuScreen(Screen): #CREA LA PANTALLA CHANCE QUE PUEDE SER MANEJADA POR EL GESTOR DE PANTALLAS
    def __init__(self, **kwargs): #INICIALIZA LA PANTALLA CHANCE Y SUS ELEMENTOS
        super().__init__(**kwargs)
        pantalla = BoxLayout(orientation='vertical', padding=20, spacing=15) #CREA UN CONTENEDOR VERTICAL PARA ORGANIZAR LOS ELEMENTOS DE LA PANTALLA

        titulo = Label(text=' SUSÚ', font_size=32, size_hint_y=None, height=60) #CREA EL TITULO DE LA PANTALLA
        pantalla.add_widget(titulo) #AGREGA EL TITULO AL CONTENEDOR
        mensaje = Label(text='¡Gestiona tus susús y turnos de manera sencilla!', font_size=18)
        pantalla.add_widget(mensaje) #AGREGA EL MENSAJE AL CONTENEDOR

        #BOTONES DE LA PANTALLA SUSU
        boton_nuevo_susu= Button(text='Nuevo Susú', font_size=18, size_hint_y=None, height=50)
        boton_nuevo_susu.bind(on_press=lambda x: setattr(self.manager, 'current', 'nuevo_susu'))
        pantalla.add_widget(boton_nuevo_susu) #AGREGA EL BOTON AL CONTENEDOR

        boton_susus_activos=Button(text='Susús Activos', font_size=18, size_hint_y=None, height=50)
        boton_susus_activos.bind(on_press=lambda x: setattr(self.manager, 'current', 'susus_activos'))
        pantalla.add_widget(boton_susus_activos)

        boton_historial_susus = Button(text='Historial de Susús', font_size=18, size_hint_y=None, height=50)
        boton_historial_susus.bind(on_press=lambda x: setattr(self.manager, 'current', 'historial_susus'))
        pantalla.add_widget(boton_historial_susus)

        boton_volver = Button(text='Atrás', font_size=18, size_hint_y=None, height=50) #CREA UN BOTON PARA VOLVER A LA PANTALLA ANTERIOR
        boton_volver.bind(on_press=lambda x: setattr(self.manager, 'current', 'inicio'))  # CAMBIA A LA PANTALLA DE INICIO AL PRESIONAR EL BOTON
        
        pantalla.add_widget(boton_volver) #AGREGA EL BOTON AL CONTENEDOR
    
        

        self.add_widget(pantalla) #AGREGA EL CONTENEDOR A LA PANTALLA SUSÚ

   