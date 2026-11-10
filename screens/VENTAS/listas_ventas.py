from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from ventas_db import listar_listas_ventas, editar_lista_ventas, eliminar_lista_ventas


class ListasVentasScreen(Screen):
    def __init__(self, **kwargs): #inicializa correctamente la pantalla 
        super().__init__(**kwargs)

        pantalla = BoxLayout(orientation='vertical', padding=20, spacing=10) 
        titulo = Label(text='Mis Listas de Ventas', font_size=28, size_hint_y=None, height=55) #titulo de la pantalla
        pantalla.add_widget(titulo)

        self.contenedor_listas = BoxLayout(
            orientation="vertical",
            spacing=10,
            size_hint_y=None
        )
        self.contenedor_listas.bind(minimum_height=self.contenedor_listas.setter("height"))

        desplazamiento = ScrollView()
        desplazamiento.add_widget(self.contenedor_listas)
        pantalla.add_widget(desplazamiento)

        boton_actualizar = Button(
            text="Actualizar Listas",
            size_hint_y=None,
            height=45
        )

        boton_actualizar.bind(
            on_press=lambda instancia: self.cargar_listas()
        )

        pantalla.add_widget(boton_actualizar)

        boton_volver = Button(
            text="Volver", size_hint_y=None, height=45
        )  # botón que permite volver a la pantalla anterior
        pantalla.add_widget(boton_volver)
        boton_volver.bind(
            on_press=lambda x: setattr(self.manager, "current", "mis_ventas")
        )

        self.add_widget(pantalla)

    def on_enter(self):
        self.cargar_listas()

    def cargar_listas(self):
        self.contenedor_listas.clear_widgets()
        listas = listar_listas_ventas()

        if not listas:
            self.contenedor_listas.add_widget(
                Label(
                    text="No hay listas de ventas registradas",
                    size_hint_y=None,
                    height=50
                )
            )
            return

        for lista in listas:
            tarjeta = Button(
                text=(
                    f"{lista['nombre']}\n"
                    f"precio unitario: B/. "
                    f"{lista['precio_unitario']:.2f}"
                ),
                size_hint_y=None,
                height=90
            )

            tarjeta.bind(
                on_press=lambda instancia, datos=lista: 
                self.mostrar_opciones_lista(datos)
                
            )
            self.contenedor_listas.add_widget(tarjeta)


    def mostrar_opciones_lista(self, lista):
        print("seleccionaste la lista:", lista)
        contenido = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=15
        )

        titulo = Label(
            text=f"Lista: {lista['nombre']}",
            size_hint_y=None,
            height=45
        )

        boton_abrir = Button(text="abrir Lista")
        boton_abrir.bind(
            on_press=lambda instancia: self.abrir_lista(lista)
             )
            
        boton_editar = Button(text="Editar Lista")
        boton_editar.bind(
            on_press=lambda _: self.editar_lista(lista)
        )
        boton_eliminar = Button(text="Eliminar Lista")
        boton_eliminar.bind(
            on_press=lambda _: self.confirmar_eliminacion(lista)
        )

        contenido.add_widget(titulo)
        contenido.add_widget(boton_abrir)
        contenido.add_widget(boton_editar)
        contenido.add_widget(boton_eliminar)

        self.popup_opciones = Popup(
            title="Opciones de la Lista",
            content=contenido,
            size_hint=(0.85, 0.55)
        )
        self.popup_opciones.open()
            
    def editar_lista(self, lista):
        self.popup_opciones.dismiss()

        contenido = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=15
        )

        entrada_nombre = TextInput(
            text=lista['nombre'],
            multiline=False,
            hint_text="Nombre de la lista",
            
        )
        entrada_precio = TextInput(
            text=str(lista['precio_unitario']),
            multiline=False,
            input_filter="float",
            hint_text="Precio unitario",
        )

        boton_guardar = Button(
            text="Guardar Cambios"
        )
        contenido.add_widget(Label(text="Nombre"))
        contenido.add_widget(entrada_nombre)
        contenido.add_widget(Label(text="Precio Unitario"))
        contenido.add_widget(entrada_precio)
        contenido.add_widget(boton_guardar)

        ventana = Popup(
            title="Editar Lista de Ventas",
            content=contenido,
            size_hint=(0.85, 0.65)
        )

        def guardar_cambios(instancia):

            nombre = entrada_nombre.text.strip()
            try:
                precio = float(entrada_precio.text)

                if not nombre or precio <= 0:
                    raise ValueError
            except ValueError:
                self.mostrar_mensaje("escribe un nombre válido y un precio unitario mayor que cero.")
                return

            exito, mensaje = editar_lista_ventas(lista['id_lista'], nombre, precio)

            print("RESULTADO:", exito, mensaje)
            self.mostrar_mensaje(mensaje)

            if exito:
                ventana.dismiss()
                self.cargar_listas()

    
        boton_guardar.bind(on_press=guardar_cambios)
        ventana.open()
        
        

    def mostrar_mensaje(self, mensaje):
        contenido = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10,
        )

        texto_mensaje = Label(
            text=mensaje,
            halign="center",
            valign="middle"
        )

        boton_aceptar = Button(
            text="Aceptar",
            size_hint_y=None,
            height=45
        )

        contenido.add_widget(texto_mensaje)
        contenido.add_widget(boton_aceptar)

        ventana = Popup(
            title="Información",
            content=contenido,
            size_hint=(0.8, 0.4)
        )

        boton_aceptar.bind(on_press=lambda instancia: ventana.dismiss())
        ventana.open()


    def confirmar_eliminacion(self, lista):
            contenido = BoxLayout(
                orientation="vertical",
                spacing=10,
                padding=15
            )

            texto = Label(
                text=f"¿Estás seguro de eliminar la lista '{lista['nombre']}'?")

            boton_confirmar = Button(text="Sí, eliminar")
            boton_cancelar = Button(text="Cancelar")

            contenido.add_widget(texto)
            contenido.add_widget(boton_confirmar)
            contenido.add_widget(boton_cancelar)

            ventana = Popup(
                title="Confirmar Eliminación",
                content=contenido,
                size_hint=(0.85, 0.45)
            )

            boton_confirmar.bind(
                on_press=lambda instancia: self.ejecutar_eliminacion(lista, ventana)
            )

            boton_cancelar.bind(on_press=lambda instancia: ventana.dismiss())

            ventana.open()


    def ejecutar_eliminacion(self, lista, ventana):
        ventana.dismiss()
        self.popup_opciones.dismiss()
        exito, mensaje = eliminar_lista_ventas(lista['id_lista'])

        self.mostrar_mensaje(mensaje)

        if exito:
            self.cargar_listas()


    def abrir_lista(self, lista):
        self.popup_opciones.dismiss()
        pantalla = self.manager.get_screen("pedidos_lista")
        pantalla.cargar_lista(lista)

        self.manager.current = "pedidos_lista"