from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import  Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from clientes_db import registrar_cliente

class NuevoClienteScreen(Screen):
    def __init__(self, **kwargs): #inicializa correctamente la pantalla 
        super().__init__(**kwargs)

        pantalla = BoxLayout(orientation='vertical', padding=20, spacing=10) #contenedor principal de la pantalla, que contiene todos los elementos de la pantalla
        
        titulo = Label(text='Crear Cliente', font_size=28, size_hint_y=None, height=60) #titulo de la pantalla
        pantalla.add_widget(titulo) #agrega el titulo a la pantalla

        mensaje = Label(text='registrar Cliente:', font_size=18) #mensaje que indica al usuario que ingrese el nombre del nuevo cliente
        pantalla.add_widget(mensaje) #agrega el mensaje a la pantalla


        ###  CAMPOS DEL FORMULARIO ########
        self.nombre_input =TextInput(
            hint_text="Nombre completo*",
            multiline=False,
            size_hint_y=None,
            height=48
        )
        pantalla.add_widget(self.nombre_input)

        self.telefono_input =TextInput(
            hint_text="teléfono",
                        multiline=False,
                        input_type="tel",
                        size_hint_y=None,
                        height=48
        )
        pantalla.add_widget(self.telefono_input)


        self.correo_input=TextInput(
                    hint_text="Correo Electrónico (opcional)",
                                multiline=False,
                                input_type="text",
                                size_hint_y=None,
                                height=48
                )
        pantalla.add_widget(self.correo_input)


        self.direccion_input=TextInput(
                            hint_text="Dirección (opcional)",
                                        multiline=False,
                                        input_type="text",
                                        size_hint_y=None,
                                        height=48
                        )
        pantalla.add_widget(self.direccion_input)



        self.notas_input=TextInput(
                                    hint_text="Notas (opcional)",
                                                multiline=True,
                                                input_type="text",
                                                size_hint_y=None,
                                                height=80
                                )
        pantalla.add_widget(self.notas_input)


    ###  MENSAJE DE RESULTADO ####


        self.mensaje_resultado = Label(
            text="",
            font_size=16,
            size_hint_y=None,
            height=40
        )

        pantalla.add_widget(self.mensaje_resultado)


         ###  BOTON PARA GUARDAR ####
        boton_guardar = Button(
                    text="Guardar Cliente",
                    font_size=18,
                    size_hint_y=None,
                    height=50
                )

        boton_guardar.bind(on_press=self.guardar_cliente)
        
        pantalla.add_widget(boton_guardar)
            
    


        boton_volver = Button(text='Volver', font_size=18, size_hint_y=None, height=50) #botónque permite volver a la pantalla anterior
        pantalla.add_widget(boton_volver) #agrega el botón de volver a la pantalla
        boton_volver.bind(on_press=lambda x: setattr(self.manager, 'current', 'clientes'))  # Cambia a la pantalla clientes al presionar el botón
       
        self.add_widget(pantalla) #agrega el contenedor principal a la pantalla.



    def guardar_cliente(self, instancia):
        nombre = self.nombre_input.text.strip()
        telefono = self.telefono_input.text.strip()
        correo = self.correo_input.text.strip()
        direccion = self.direccion_input.text.strip()
        notas = self.notas_input.text.strip()

        if not nombre:
            self.mensaje_resultado.text =("Escribe el nombre del cliente")
            return
        resultado = registrar_cliente(
            nombre=nombre,
            telefono=telefono or None,
            correo=correo or None,
            direccion=direccion or None,
            notas=notas or None 
        )

        if resultado:
            self.mensaje_resultado.text=(f"Cliente guardado correctamenta. ID: {resultado}")

            self.nombre_input.text=""
            self.telefono_input.text=""
            self.correo_input.text=""
            self.direccion_input.text=""
            self.notas_input.text=""

        else:
            self.mensaje_resultado.text =("No se pudo guardar, revisa la terminal")
    