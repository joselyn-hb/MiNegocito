
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from decimal import Decimal, InvalidOperation

from ventas_db import crear_lista_ventas


# --------------------------------------------------
# BOTÓN PERSONALIZADO
# --------------------------------------------------

class BotonFormulario(Button):

    def __init__(self, color_fondo, **kwargs):
        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self.color = (1, 1, 1, 1)
        self.font_size = dp(17)
        self.bold = True

        with self.canvas.before:
            Color(*color_fondo)
            self.fondo = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(14)]
            )

        self.bind(
            pos=self.actualizar_fondo,
            size=self.actualizar_fondo
        )

    def actualizar_fondo(self, instancia, valor):
        self.fondo.pos = instancia.pos
        self.fondo.size = instancia.size


# --------------------------------------------------
# PANTALLA NUEVA LISTA DE VENTAS
# --------------------------------------------------

class NuevaListaVentasScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Contenedor principal.
        pantalla = BoxLayout(
            orientation="vertical",
            padding=[dp(18), dp(15), dp(18), dp(15)],
            spacing=dp(12)
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
            padding=dp(12),
            spacing=dp(3),
            size_hint_y=None,
            height=dp(100)
        )

        with encabezado.canvas.before:
            Color(0.02, 0.25, 0.65, 1)
            fondo_encabezado = RoundedRectangle(
                pos=encabezado.pos,
                size=encabezado.size,
                radius=[dp(20)]
            )

        encabezado.bind(
            pos=lambda instancia, valor:
            setattr(fondo_encabezado, "pos", valor),
            size=lambda instancia, valor:
            setattr(fondo_encabezado, "size", valor)
        )

        encabezado.add_widget(
            Label(
                text="Nueva lista de ventas",
                font_size=dp(27),
                bold=True,
                color=(1, 1, 1, 1)
            )
        )

        encabezado.add_widget(
            Label(
                text="Organiza tus productos y precios",
                font_size=dp(14),
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
        # INDICACIONES
        # ------------------------------------------

        pantalla.add_widget(
            Label(
                text="Completa los datos de tu nueva lista",
                font_size=dp(20),
                bold=True,
                color=(0.07, 0.15, 0.35, 1),
                size_hint_y=None,
                height=dp(55)
            )
        )

        # ------------------------------------------
        # FORMULARIO
        # ------------------------------------------

        formulario = BoxLayout(
        orientation="vertical",
        spacing=dp(10),
        size_hint_y=None,
        height=dp(190)
    )

        # Nombre de la lista.
        formulario.add_widget(
            Label(
                text="Nombre de la lista",
                font_size=dp(16),
                bold=True,
                color=(0.07, 0.15, 0.35, 1),
                size_hint_y=None,
                height=dp(28),
                halign="left",
                valign="middle"
            )
        )

        self.entrada_nombre = TextInput(
            hint_text="Ejemplo: Postres",
            multiline=False,
            size_hint_y=None,
            height=dp(48),
            font_size=dp(17),
            padding=[dp(12), dp(12)],
            background_normal="",
            background_active="",
            background_color=(1, 1, 1, 1),
            foreground_color=(0.10, 0.15, 0.23, 1),
            cursor_color=(0.02, 0.25, 0.65, 1),
            hint_text_color=(0.45, 0.49, 0.55, 1)
        )

        formulario.add_widget(self.entrada_nombre)

        # Precio unitario.
        formulario.add_widget(
            Label(
                text="Precio unitario (B/.)",
                font_size=dp(16),
                bold=True,
                color=(0.07, 0.15, 0.35, 1),
                size_hint_y=None,
                height=dp(28),
                halign="left",
                valign="middle"
            )
        )

        self.entrada_precio = TextInput(
            hint_text="Ejemplo: 2.00",
            multiline=False,
            input_filter="float",
            size_hint_y=None,
            height=dp(48),
            font_size=dp(17),
            padding=[dp(12), dp(12)],
            background_normal="",
            background_active="",
            background_color=(1, 1, 1, 1),
            foreground_color=(0.10, 0.15, 0.23, 1),
            cursor_color=(0.02, 0.25, 0.65, 1),
            hint_text_color=(0.45, 0.49, 0.55, 1)
        )

        formulario.add_widget(self.entrada_precio)

        pantalla.add_widget(formulario)

        # ------------------------------------------
        # BOTÓN GUARDAR
        # ------------------------------------------

        boton_guardar = BotonFormulario(
            color_fondo=(0.09, 0.42, 0.53, 1),
            text="Guardar lista",
            size_hint_y=None,
            height=dp(52)
        )

        boton_guardar.bind(
            on_release=self.guardar_lista
        )

        pantalla.add_widget(boton_guardar)

        # ------------------------------------------
        # BOTÓN VOLVER
        # ------------------------------------------

        boton_volver = BotonFormulario(
            color_fondo=(0.02, 0.17, 0.43, 1),
            text="Volver",
            size_hint_y=None,
            height=dp(48)
        )

        boton_volver.bind(
            on_release=lambda instancia:
            setattr(self.manager, "current", "mis_ventas")
        )

        pantalla.add_widget(boton_volver)

        self.add_widget(pantalla)

    # --------------------------------------------------
    # GUARDAR NUEVA LISTA
    # --------------------------------------------------

    def guardar_lista(self, instancia):

        nombre = self.entrada_nombre.text.strip()
        precio_texto = self.entrada_precio.text.strip()

        # Validar el nombre.
        if not nombre:
            self.mostrar_mensaje(
                "Escribe el nombre de la lista."
            )
            return

        # Validar que se haya ingresado el precio.
        if not precio_texto:
            self.mostrar_mensaje(
                "Escribe el precio unitario de la lista."
            )
            return

        try:
            precio = Decimal(precio_texto)

            # El precio debe ser mayor que cero.
            if precio <= 0:
                self.mostrar_mensaje(
                    "El precio unitario debe ser mayor que cero."
                )
                return

            # No permitir más de dos decimales.
            if precio.as_tuple().exponent < -2:
                self.mostrar_mensaje(
                    "El precio unitario no puede tener más de dos decimales."
                )
                return

            # Guardar la lista utilizando la función existente.
            exito, mensaje = crear_lista_ventas(
                nombre,
                precio
            )

            self.mostrar_mensaje(mensaje)

            # Limpiar los campos si se guardó correctamente.
            if exito:
                self.entrada_nombre.text = ""
                self.entrada_precio.text = ""

        except InvalidOperation:
            self.mostrar_mensaje(
                "El precio unitario debe ser un número válido."
            )

    # --------------------------------------------------
    # MENSAJES EMERGENTES
    # --------------------------------------------------

    
def mostrar_mensaje(self, mensaje):

    # Contenedor del mensaje.
    contenido = BoxLayout(
        orientation="vertical",
        padding=dp(18),
        spacing=dp(12)
    )

    # Mensaje con texto oscuro sobre fondo claro.
    etiqueta = Label(
        text=mensaje,
        color=(0.07, 0.15, 0.35, 1),
        font_size=dp(16),
        halign="center",
        valign="middle"
    )

    contenido.add_widget(etiqueta)

    # Botón aceptar más pequeño.
    boton_aceptar = BotonFormulario(
        color_fondo=(0.02, 0.25, 0.65, 1),
        text="Aceptar",
        size_hint=(0.75, None),
        height=dp(42),
        pos_hint={"center_x": 0.5}
    )

    contenido.add_widget(boton_aceptar)

    # Ventana clara y compacta.
    ventana = Popup(
        title="Mi Negocito",
        content=contenido,
        size_hint=(0.75, None),
        height=dp(185),
        background="",
        background_color=(0.91, 0.96, 0.99, 1),
        separator_color=(1, 0.78, 0.12, 1),
        title_color=(0.07, 0.15, 0.35, 1),
        title_size=dp(18)
    )

    boton_aceptar.bind(
        on_release=lambda instancia: ventana.dismiss()
    )

    ventana.open()

