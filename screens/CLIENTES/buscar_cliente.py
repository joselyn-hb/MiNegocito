from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import  Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from clientes_db import buscar_clientes
from kivy.uix.scrollview import ScrollView

class BuscarClienteScreen(Screen):
    def __init__(self, **kwargs): #inicializa correctamente la pantalla 
        super().__init__(**kwargs)

        pantalla = BoxLayout(orientation='vertical', padding=20, spacing=15) #contenedor principal de la pantalla, que contiene todos los elementos de la pantalla
        
        titulo = Label(text='Buscar Cliente', font_size=32, size_hint_y=None, height=60) #titulo de la pantalla
        pantalla.add_widget(titulo) #agrega el titulo a la pantalla

        mensaje = Label(text='Ingrese el nombre del cliente a buscar:', font_size=18) #mensaje que indica al usuario que ingrese el nombre del nuevo cliente
        pantalla.add_widget(mensaje) #agrega el mensaje a la pantalla

        # CAMPO PARA ESCRIBIR RL NOMBRE O TELEFONO A BUSCAR
        self.entrada_busqueda = TextInput(hint_text= "Escribe un nombre o teléfono",
                                          multiline= False,
                                          size_hint_y=None,
                                          height=50)

        pantalla.add_widget(self.entrada_busqueda)

        # Botón para ejjecutar la busqueda
        boton_buscar =Button(text="Buscar", font_size=18, size_hint_y=None, height=50)

        boton_buscar.bind(on_press=self.buscar_cliente)
        pantalla.add_widget(boton_buscar)

        # ESPACIO PARA BUSCAR LOS RESULTADOS
        self.resultados = BoxLayout(orientation="vertical", spacing=8, size_hint_y=None)

        self.resultados.bind(minimum_height=self.resultados.setter("height"))

        desplazamiento = ScrollView()
        desplazamiento.add_widget(self.resultados)
        pantalla.add_widget(desplazamiento)
            
                            
    
        

        boton_volver = Button(text='Volver', font_size=18, size_hint_y=None, height=50) #botónque permite volver a la pantalla anterior
        pantalla.add_widget(boton_volver) #agrega el botón de volver a la pantalla
        boton_volver.bind(on_press=lambda x: setattr(self.manager, 'current', 'clientes'))  # Cambia a la pantalla clientes al presionar el botón
       
        self.add_widget(pantalla) #agrega el contenedor principal a la pantalla

    def buscar_cliente(self, instancia):
         texto = self.entrada_busqueda.text.strip()

         self.resultados.clear_widgets()

         if not texto:
            self.resultados.add_widget(
                Label(
                    text="Escribe un nombre o teléfono para buscar.",
                    size_hint_y=None,
                    height=50
                )
            )
            return

         clientes = buscar_clientes(texto)

         if not clientes:
            self.resultados.add_widget(
                Label(
                    text="No se encontraron clientes.",
                    size_hint_y=None,
                    height=50
                )
            )
            return

         for cliente in clientes:
            telefono = cliente["telefono"] or "Sin teléfono"
            correo = cliente["correo"] or "Sin correo"

            tarjeta = Label(
                text=(
                    f"{cliente['nombre']}\n"
                    f"Teléfono: {telefono}\n"
                    f"Correo: {correo}"
                ),
                font_size=16,
                size_hint_y=None,
                height=90,
                halign="left",
                valign="middle"
            )

            tarjeta.bind(
                size=lambda widget, size: setattr(
                    widget,
                    "text_size",
                    (size[0] - 20, None)
                )
            )

            self.resultados.add_widget(tarjeta)