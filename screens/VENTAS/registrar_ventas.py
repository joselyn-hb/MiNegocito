
from decimal import Decimal, InvalidOperation

from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

from ventas_db import registrar_venta_individual


# --------------------------------------------------
# BOTÓN PERSONALIZADO
# --------------------------------------------------

class BotonAccion(Button):

    def __init__(self, color_fondo, **kwargs):
        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self.color = (1, 1, 1, 1)
        self.font_size = dp(15)
        self.bold = True

        with self.canvas.before:
            Color(*color_fondo)
            self.fondo = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(12)]
            )

        self.bind(
            pos=self.actualizar_fondo,
            size=self.actualizar_fondo
        )

    def actualizar_fondo(self, instancia, valor):
        self.fondo.pos = instancia.pos
        self.fondo.size = instancia.size


# --------------------------------------------------
# VENTANA EMERGENTE CLARA
# --------------------------------------------------

class PopupClaro(Popup):

    def __init__(self, **kwargs):

        kwargs.setdefault("background", "")
        kwargs.setdefault("background_color", (1, 1, 1, 1))
        kwargs.setdefault(
            "separator_color",
            (1, 0.78, 0.12, 1)
        )
        kwargs.setdefault(
            "title_color",
            (0.07, 0.15, 0.35, 1)
        )
        kwargs.setdefault("title_size", dp(17))

        super().__init__(**kwargs)


# --------------------------------------------------
# PANTALLA REGISTRAR VENTAS
# --------------------------------------------------

class RegistrarVentasScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.productos = []

        # Contenedor principal.
        pantalla = BoxLayout(
            orientation="vertical",
            padding=[dp(18), dp(12), dp(18), dp(12)],
            spacing=dp(9)
        )

        # Fondo azul claro.
        with pantalla.canvas.before:
            Color(0.91, 0.96, 0.99, 1)
            fondo = RoundedRectangle(
                pos=pantalla.pos,
                size=pantalla.size
            )

        pantalla.bind(
            pos=lambda instancia, valor:
            setattr(fondo, "pos", valor),
            size=lambda instancia, valor:
            setattr(fondo, "size", valor)
        )

        # ------------------------------------------
        # ENCABEZADO
        # ------------------------------------------

        encabezado = BoxLayout(
            orientation="vertical",
            padding=dp(8),
            spacing=dp(2),
            size_hint_y=None,
            height=dp(82)
        )

        with encabezado.canvas.before:
            Color(0.02, 0.25, 0.65, 1)
            fondo_encabezado = RoundedRectangle(
                pos=encabezado.pos,
                size=encabezado.size,
                radius=[dp(18)]
            )

        encabezado.bind(
            pos=lambda instancia, valor:
            setattr(fondo_encabezado, "pos", valor),
            size=lambda instancia, valor:
            setattr(fondo_encabezado, "size", valor)
        )

        encabezado.add_widget(
            Label(
                text="Registrar ventas individuales",
                font_size=dp(23),
                bold=True,
                color=(1, 1, 1, 1)
            )
        )

        encabezado.add_widget(
            Label(
                text="Registra los productos vendidos a cada cliente",
                font_size=dp(13),
                color=(1, 1, 1, 1)
            )
        )

        pantalla.add_widget(encabezado)

        # ------------------------------------------
        # LÍNEA AMARILLA
        # ------------------------------------------

        linea = BoxLayout(
            size_hint_y=None,
            height=dp(5)
        )

        with linea.canvas.before:
            Color(1, 0.78, 0.12, 1)
            fondo_linea = RoundedRectangle(
                pos=linea.pos,
                size=linea.size,
                radius=[dp(3)]
            )

        linea.bind(
            pos=lambda instancia, valor:
            setattr(fondo_linea, "pos", valor),
            size=lambda instancia, valor:
            setattr(fondo_linea, "size", valor)
        )

        pantalla.add_widget(linea)

        # ------------------------------------------
        # DATOS DEL CLIENTE
        # ------------------------------------------

        pantalla.add_widget(
            self.crear_etiqueta("Nombre del cliente")
        )

        self.nombre_cliente = self.crear_campo(
            "Escribe el nombre del cliente"
        )

        pantalla.add_widget(self.nombre_cliente)

        # ------------------------------------------
        # DATOS DEL PRODUCTO
        # ------------------------------------------

        pantalla.add_widget(
            self.crear_etiqueta("Nombre del producto")
        )

        self.nombre_producto = self.crear_campo(
            "Ejemplo: Perfume"
        )

        pantalla.add_widget(self.nombre_producto)

        # Cantidad y precio en una misma fila.
        fila_datos = BoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint_y=None,
            height=dp(65)
        )

        columna_cantidad = BoxLayout(
            orientation="vertical",
            spacing=dp(4)
        )

        columna_cantidad.add_widget(
            self.crear_etiqueta("Cantidad")
        )

        self.cantidad_producto = self.crear_campo(
            "Ejemplo: 2",
            filtro="int"
        )

        columna_cantidad.add_widget(
            self.cantidad_producto
        )

        columna_precio = BoxLayout(
            orientation="vertical",
            spacing=dp(4)
        )

        columna_precio.add_widget(
            self.crear_etiqueta("Precio unitario (B/.)")
        )

        self.precio_producto = self.crear_campo(
            "Ejemplo: 5.00",
            filtro="float"
        )

        columna_precio.add_widget(
            self.precio_producto
        )

        fila_datos.add_widget(columna_cantidad)
        fila_datos.add_widget(columna_precio)

        pantalla.add_widget(fila_datos)

        # ------------------------------------------
        # BOTÓN AGREGAR PRODUCTO
        # ------------------------------------------

        self.boton_agregar = BotonAccion(
            color_fondo=(0.09, 0.42, 0.53, 1),
            text="Agregar producto",
            size_hint_y=None,
            height=dp(45)
        )

        self.boton_agregar.bind(
            on_release=self.agregar_producto
        )

        pantalla.add_widget(self.boton_agregar)

        # ------------------------------------------
        # LISTA DE PRODUCTOS AGREGADOS
        # ------------------------------------------

        self.titulo_productos = Label(
            text="Productos agregados",
            font_size=dp(16),
            bold=True,
            color=(0.07, 0.15, 0.35, 1),
            size_hint_y=None,
            height=dp(28)
        )

        pantalla.add_widget(self.titulo_productos)

        self.contenedor_productos = BoxLayout(
            orientation="vertical",
            spacing=dp(7),
            size_hint_y=None
        )

        self.contenedor_productos.bind(
            minimum_height=
            self.contenedor_productos.setter("height")
        )

        self.scroll_productos = ScrollView(
            size_hint=(1, 1),
            do_scroll_x=False
        )

        self.scroll_productos.add_widget(
            self.contenedor_productos
        )

        pantalla.add_widget(self.scroll_productos)

        # ------------------------------------------
        # TOTAL DE LA VENTA
        # ------------------------------------------

        self.total_venta = Label(
            text="Total: B/. 0.00",
            font_size=dp(21),
            bold=True,
            color=(0.07, 0.15, 0.35, 1),
            size_hint_y=None,
            height=dp(38)
        )

        pantalla.add_widget(self.total_venta)

        # ------------------------------------------
        # BOTÓN GUARDAR VENTA
        # ------------------------------------------

        self.boton_guardar = BotonAccion(
            color_fondo=(0.02, 0.25, 0.65, 1),
            text="Guardar venta",
            size_hint_y=None,
            height=dp(48)
        )

        self.boton_guardar.bind(
            on_release=self.guardar_venta
        )

        pantalla.add_widget(self.boton_guardar)

        # ------------------------------------------
        # BOTÓN VOLVER
        # ------------------------------------------

        boton_volver = BotonAccion(
            color_fondo=(0.02, 0.17, 0.43, 1),
            text="Volver",
            size_hint_y=None,
            height=dp(43)
        )

        boton_volver.bind(
            on_release=lambda instancia:
            setattr(self.manager, "current", "mis_ventas")
        )

        pantalla.add_widget(boton_volver)

        self.add_widget(pantalla)

    # --------------------------------------------------
    # CREAR ETIQUETAS
    # --------------------------------------------------

    def crear_etiqueta(self, texto):

        return Label(
            text=texto,
            font_size=dp(14),
            bold=True,
            color=(0.07, 0.15, 0.35, 1),
            size_hint_y=None,
            height=dp(22),
            halign="left",
            valign="middle"
        )

    # --------------------------------------------------
    # CREAR CAMPOS DE ESCRITURA
    # --------------------------------------------------

    def crear_campo(self, sugerencia, filtro=None):

        return TextInput(
            hint_text=sugerencia,
            multiline=False,
            input_filter=filtro,
            size_hint_y=None,
            height=dp(43),
            font_size=dp(15),
            padding=[dp(10), dp(10)],
            background_normal="",
            background_active="",
            background_color=(0.88, 0.94, 0.98, 1),
            foreground_color=(0.07, 0.15, 0.35, 1),
            cursor_color=(0.02, 0.25, 0.65, 1),
            hint_text_color=(0.40, 0.46, 0.55, 1)
        )

    # --------------------------------------------------
    # AGREGAR PRODUCTO
    # --------------------------------------------------

    def agregar_producto(self, instancia):

        nombre = self.nombre_producto.text.strip()

        try:
            cantidad = int(self.cantidad_producto.text)
            precio = Decimal(self.precio_producto.text)

            if not nombre:
                raise ValueError(
                    "Debes escribir el nombre del producto."
                )

            if cantidad <= 0 or precio <= 0:
                raise ValueError(
                    "La cantidad y el precio deben ser mayores que cero."
                )

        except (ValueError, InvalidOperation):
            self.mostrar_mensaje(
                "Verifica el nombre, la cantidad y el precio."
            )
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

    # --------------------------------------------------
    # ACTUALIZAR LISTA Y TOTAL
    # --------------------------------------------------

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
                height=dp(82),
                spacing=dp(6),
                padding=dp(5)
            )

            # Fondo de cada producto.
            with fila.canvas.before:
                Color(1, 1, 1, 1)
                fondo_fila = RoundedRectangle(
                    pos=fila.pos,
                    size=fila.size,
                    radius=[dp(10)]
                )

            fila.bind(
                pos=lambda instancia, valor, fondo=fondo_fila:
                setattr(fondo, "pos", valor),
                size=lambda instancia, valor, fondo=fondo_fila:
                setattr(fondo, "size", valor)
            )

            informacion = Label(
                text=(
                    f'{producto["producto"]}\n'
                    f'Cantidad: {producto["cantidad"]} | '
                    f'Precio: B/. {producto["precio_unitario"]:.2f}\n'
                    f'Subtotal: B/. {subtotal:.2f}'
                ),
                color=(0.07, 0.15, 0.35, 1),
                font_size=dp(12),
                halign="left",
                valign="middle",
                size_hint_x=1
            )

            informacion.bind(
                size=lambda instancia, valor:
                setattr(instancia, "text_size", valor)
            )

            boton_editar = BotonAccion(
                color_fondo=(0.09, 0.42, 0.53, 1),
                text="Editar",
                size_hint_x=None,
                width=dp(62),
                font_size=dp(11)
            )

            boton_editar.bind(
                on_release=lambda instancia, i=indice:
                self.editar_producto(i)
            )

            boton_eliminar = BotonAccion(
                color_fondo=(0.82, 0.16, 0.19, 1),
                text="Eliminar",
                size_hint_x=None,
                width=dp(70),
                font_size=dp(10)
            )

            boton_eliminar.bind(
                on_release=lambda instancia, i=indice:
                self.eliminar_producto(i)
            )

            fila.add_widget(informacion)
            fila.add_widget(boton_editar)
            fila.add_widget(boton_eliminar)

            self.contenedor_productos.add_widget(fila)

        self.total_venta.text = (
            f"Total: B/. {total:.2f}"
        )

    # --------------------------------------------------
    # ELIMINAR PRODUCTO
    # --------------------------------------------------

    def eliminar_producto(self, indice):

        if 0 <= indice < len(self.productos):

            self.productos.pop(indice)

            self.actualizar_lista_productos()

    # --------------------------------------------------
    # EDITAR PRODUCTO
    # --------------------------------------------------

    def editar_producto(self, indice):

        producto = self.productos[indice]

        contenido = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=dp(15)
        )

        contenido.add_widget(
            self.crear_etiqueta("Nombre del producto")
        )

        nombre = self.crear_campo(
            "Nombre del producto"
        )
        nombre.text = producto["producto"]

        contenido.add_widget(nombre)

        contenido.add_widget(
            self.crear_etiqueta("Cantidad")
        )

        cantidad = self.crear_campo(
            "Cantidad",
            filtro="int"
        )
        cantidad.text = str(producto["cantidad"])

        contenido.add_widget(cantidad)

        contenido.add_widget(
            self.crear_etiqueta("Precio unitario (B/.)")
        )

        precio = self.crear_campo(
            "Precio unitario",
            filtro="float"
        )
        precio.text = str(producto["precio_unitario"])

        contenido.add_widget(precio)

        # Botones de edición.
        botones = BoxLayout(
            size_hint_y=None,
            height=dp(45),
            spacing=dp(10)
        )

        boton_guardar = BotonAccion(
            color_fondo=(0.02, 0.25, 0.65, 1),
            text="Guardar",
            font_size=dp(14)
        )

        boton_cancelar = BotonAccion(
            color_fondo=(0.82, 0.16, 0.19, 1),
            text="Cancelar",
            font_size=dp(14)
        )

        botones.add_widget(boton_guardar)
        botones.add_widget(boton_cancelar)

        contenido.add_widget(botones)

        ventana = PopupClaro(
            title="Editar producto",
            content=contenido,
            size_hint=(0.88, None),
            height=dp(390)
        )

        # Guardar cambios.
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

        boton_guardar.bind(
            on_release=guardar_cambios
        )

        boton_cancelar.bind(
            on_release=lambda instancia: ventana.dismiss()
        )

        ventana.open()

    # --------------------------------------------------
    # MENSAJES EMERGENTES
    # --------------------------------------------------

    def mostrar_mensaje(self, mensaje):

        contenido = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=dp(15)
        )

        texto = Label(
            text=mensaje,
            color=(0.07, 0.15, 0.35, 1),
            font_size=dp(16),
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=dp(65)
        )

        texto.bind(
            width=lambda instancia, valor:
            setattr(
                instancia,
                "text_size",
                (valor - dp(10), None)
            )
        )

        contenido.add_widget(texto)

        boton_cerrar = BotonAccion(
            color_fondo=(0.02, 0.25, 0.65, 1),
            text="Aceptar",
            size_hint=(0.65, None),
            height=dp(42),
            pos_hint={"center_x": 0.5}
        )

        contenido.add_widget(boton_cerrar)

        ventana = PopupClaro(
            title="Mi Negocito",
            content=contenido,
            size_hint=(0.82, None),
            height=dp(190)
        )

        boton_cerrar.bind(
            on_release=lambda instancia: ventana.dismiss()
        )

        ventana.open()

    # --------------------------------------------------
    # GUARDAR VENTA
    # --------------------------------------------------

    def guardar_venta(self, instancia):

        nombre_cliente = self.nombre_cliente.text.strip()

        if not nombre_cliente:
            self.mostrar_mensaje(
                "Escribe el nombre del cliente."
            )
            return

        if not self.productos:
            self.mostrar_mensaje(
                "Agrega al menos un producto."
            )
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
