from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import  Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from decimal import Decimal, InvalidOperation
from kivy.uix.popup import Popup

from ventas_db import registrar_venta_individual

class RegistrarVentasScreen(Screen):
    def __init__(self, **kwargs): #inicializa correctamente la pantalla 
        super().__init__(**kwargs)

        self.productos = [] #está lista guardará temporalmente los productos que eel usuari agregue antes de guardar 

        pantalla = BoxLayout(orientation='vertical', padding=20, spacing=15) #contenedor principal de la pantalla, que contiene todos los elementos de la pantalla
        
        titulo = Label(text='Registrar Ventas Individuales', font_size=32, size_hint_y=None, height=60) #titulo de la pantalla

        pantalla.add_widget(titulo) #agrega el titulo a la pantalla

        self.nombre_cliente = TextInput(
            hint_text = "Nombre del Cliwnte",
            multiline = False,
            size_hint_y = None,
            height = 45
        )
        pantalla.add_widget(self.nombre_cliente)

        self.nombre_producto = TextInput(
            hint_text="Nombre del producto",
            multiline=False,
            size_hint_y=None,
            height=45
        )

        pantalla.add_widget(self.nombre_producto)

        self.cantidad_producto = TextInput(
            hint_text="Cantidad",
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=45
        )

        pantalla.add_widget(self.cantidad_producto)

        self.precio_producto = TextInput(
            hint_text="Precio unitario (B/.)",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=45
        )

        pantalla.add_widget(self.precio_producto)

        self.boton_agregar = Button(
            text="Agregar producto",
            size_hint_y=None,
            height=50
        )

        self.boton_agregar.bind(
            on_press=self.agregar_producto
        )

        pantalla.add_widget(self.boton_agregar)

        self.contenedor_productos = BoxLayout(
            orientation="vertical",
            spacing=8,
            size_hint_y=None
        )

        self.contenedor_productos.bind(
            minimum_height=self.contenedor_productos.setter("height")
        )

        self.scroll_productos = ScrollView(
            size_hint=(1, 1)
        )

        self.scroll_productos.add_widget(
            self.contenedor_productos
        )

        pantalla.add_widget(self.scroll_productos)


        self.total_venta = Label(
            text="Total: B/. 0.00",
            font_size=22,
            size_hint_y=None,
            height=50
)

        pantalla.add_widget(self.total_venta)

        self.boton_guardar = Button(
                    text="Guardar venta",
                    size_hint_y=None,
                    height=50
                )
        
        self.boton_guardar.bind(
                    on_press=self.guardar_venta
                )
        
        pantalla.add_widget(self.boton_guardar)

      
        mensaje = Label(text='Registre sus ventas individuales:', font_size=18) #mensaje que indica al usuario que ingrese el nombre de la nueva lista de ventas
        pantalla.add_widget(mensaje) #agrega el mensaje a la pantalla

        boton_volver = Button(text='Volver', font_size=18, size_hint_y=None, height=50) #botón que permite volver a la pantalla anterior
        boton_volver.bind(on_press=lambda x: setattr(self.manager, 'current', 'mis_ventas'))  # Cambia a la pantalla de Mis Ventas al presionar el botón
        
            
        pantalla.add_widget(boton_volver) #agrega el botón de volver a la pantalla

        self.add_widget(pantalla)

    def agregar_producto(self, instancia):

        nombre = self.nombre_producto.text.strip()

        try:
            cantidad = int(self.cantidad_producto.text)
            precio = Decimal(self.precio_producto.text)

            if not nombre:
                raise ValueError("Debes escribir el nombre del producto.")

            if cantidad <= 0 or precio <= 0:
                raise ValueError("La cantidad y el precio deben ser mayores que cero.")

        except (ValueError, InvalidOperation):
            self.mostrar_mensaje("Verifica el nombre, la cantidad y el precio.")
            return

        producto = {
            "producto": nombre,
            "cantidad": cantidad,
            "precio_unitario": precio
        }

        self.productos.append(producto)

        self.nombre_producto.text = ""
        self.cantidad_producto.text = ""
        self.precio_producto.text = ""

        self.actualizar_lista_productos()


    def actualizar_lista_productos(self):

        self.contenedor_productos.clear_widgets()

        total = Decimal("0.00")

        for indice, producto in enumerate(self.productos):

            subtotal = (
                producto["cantidad"] *
                producto["precio_unitario"]
            )

            total += subtotal

            fila = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=70,
                spacing=5
            )

            informacion = Label(
                text=(
                    f'{producto["producto"]}\n'
                    f'Cantidad: {producto["cantidad"]} | '
                    f'Precio: B/. {producto["precio_unitario"]:.2f}\n'
                    f'Subtotal: B/. {subtotal:.2f}'
                ),
                halign="left"
            )

            boton_editar = Button(
                text="Editar",
                size_hint_x=None,
                width=75
            )
            boton_editar.bind(
                on_press=lambda instancia, i=indice: self.editar_producto(i)
            )

            boton_eliminar = Button(
                text="Eliminar",
                size_hint_x=None,
                width=85
            )
            boton_eliminar.bind(
                on_press=lambda instancia, i=indice: self.eliminar_producto(i)
            )

            fila.add_widget(informacion)
            fila.add_widget(boton_editar)
            fila.add_widget(boton_eliminar)

            self.contenedor_productos.add_widget(fila)

        self.total_venta.text = f"Total: B/. {total:.2f}"


    def eliminar_producto(self, indice):  #FUNCIÓN PARA ELIMINAR UN PRODUCTO

        if 0 <= indice < len(self.productos):

            self.productos.pop(indice)

            self.actualizar_lista_productos()


    # MÉTODO PARA EDITAR UN PRODUCTO
    def editar_producto(self, indice):

        producto = self.productos[indice]

        contenido = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10
        )

        nombre = TextInput(
            text=producto["producto"],
            hint_text="Nombre del producto",
            multiline=False,
            size_hint_y=None,
            height=45
        )

        cantidad = TextInput(
            text=str(producto["cantidad"]),
            hint_text="Cantidad",
            input_filter="int",
            multiline=False,
            size_hint_y=None,
            height=45
        )

        precio = TextInput(
            text=str(producto["precio_unitario"]),
            hint_text="Precio unitario",
            input_filter="float",
            multiline=False,
            size_hint_y=None,
            height=45
        )

        boton_guardar = Button(
            text="Guardar cambios",
            size_hint_y=None,
            height=45
        )

        contenido.add_widget(nombre)
        contenido.add_widget(cantidad)
        contenido.add_widget(precio)
        contenido.add_widget(boton_guardar)

        ventana = Popup(
            title="Editar producto",
            content=contenido,
            size_hint=(0.85, 0.65)
        )

        def guardar_cambios(instancia):

            try:
                nuevo_nombre = nombre.text.strip()
                nueva_cantidad = int(cantidad.text)
                nuevo_precio = Decimal(precio.text)

                if not nuevo_nombre:
                    raise ValueError()

                if nueva_cantidad <= 0 or nuevo_precio <= 0:
                    raise ValueError()

            except (ValueError, InvalidOperation):
                self.mostrar_mensaje(
                    "Verifica el nombre, la cantidad y el precio."
                )
                return

            self.productos[indice] = {
                "producto": nuevo_nombre,
                "cantidad": nueva_cantidad,
                "precio_unitario": nuevo_precio
            }

            ventana.dismiss()
            self.actualizar_lista_productos()

        boton_guardar.bind(on_press=guardar_cambios)

        ventana.open()

    def mostrar_mensaje(self, mensaje):

        contenido = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=10
        )

        texto = Label(
            text=mensaje
        )

        boton_cerrar = Button(
            text="Aceptar",
            size_hint_y=None,
            height=45
        )

        contenido.add_widget(texto)
        contenido.add_widget(boton_cerrar)

        ventana = Popup(
            title="Mi Negocito",
            content=contenido,
            size_hint=(0.8, 0.4)
        )

        boton_cerrar.bind(
            on_press=ventana.dismiss
        )

        ventana.open()


    def guardar_venta(self, instancia):

        nombre_cliente = self.nombre_cliente.text.strip()

        if not nombre_cliente:
            self.mostrar_mensaje("Escribe el nombre del cliente.")
            return

        if not self.productos:
            self.mostrar_mensaje("Agrega al menos un producto.")
            return

        exito, mensaje = registrar_venta_individual(
            nombre_cliente,
            self.productos
        )

        if exito:

            self.mostrar_mensaje(mensaje)

            self.nombre_cliente.text = ""
            self.productos.clear()

            self.nombre_producto.text = ""
            self.cantidad_producto.text = ""
            self.precio_producto.text = ""

            self.actualizar_lista_productos()

        else:
            self.mostrar_mensaje(mensaje)
