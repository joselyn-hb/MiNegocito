
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
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

class BotonAccion(Button):

    def __init__(self, color_fondo, **kwargs):
        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self.color = (1, 1, 1, 1)
        self.font_size = dp(18)
        self.bold = True

        with self.canvas.before:
            Color(*color_fondo)
            self.fondo = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(18)]
            )

        self.bind(
            pos=self.actualizar_fondo,
            size=self.actualizar_fondo
        )

    def actualizar_fondo(self, instancia, valor):
        self.fondo.pos = instancia.pos
        self.fondo.size = instancia.size


# --------------------------------------------------
# VENTANA EMERGENTE CON FONDO CLARO
# --------------------------------------------------

class PopupClaro(Popup):

    def __init__(self, **kwargs):
        kwargs["background"] = ""
        kwargs["background_color"] = (1, 1, 1, 1)

        super().__init__(**kwargs)

        # Fondo azul claro de la ventana.
        with self.canvas.before:
            Color(0.91, 0.96, 0.99, 1)
            self.fondo_popup = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(16)]
            )

        self.bind(
            pos=self.actualizar_fondo,
            size=self.actualizar_fondo
        )

    def actualizar_fondo(self, instancia, valor):
        self.fondo_popup.pos = instancia.pos
        self.fondo_popup.size = instancia.size



# --------------------------------------------------
# PANTALLA MIS VENTAS
# --------------------------------------------------

class MisVentasScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        pantalla = BoxLayout(
            orientation="vertical",
            padding=[dp(18), dp(15), dp(18), dp(15)],
            spacing=dp(12)
        )

        # Fondo general.
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

        # Encabezado.
        encabezado = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(3),
            size_hint_y=None,
            height=dp(105)
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
                text="Mis ventas",
                font_size=dp(29),
                bold=True,
                color=(1, 1, 1, 1)
            )
        )

        encabezado.add_widget(
            Label(
                text="Organiza y controla tus ventas",
                font_size=dp(14),
                color=(1, 1, 1, 1)
            )
        )

        pantalla.add_widget(encabezado)

        # Línea amarilla.
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

        # Título de opciones.
        pantalla.add_widget(
            Label(
                text="¿Qué deseas hacer?",
                font_size=dp(23),
                bold=True,
                color=(0.07, 0.15, 0.35, 1),
                size_hint_y=None,
                height=dp(55)
            )
        )

        # Cuadrícula de opciones.
        opciones = GridLayout(
            cols=2,
            spacing=dp(12),
            size_hint_y=None,
            row_default_height=dp(145),
            row_force_default=True
        )

        opciones.bind(
            minimum_height=opciones.setter("height")
        )

        # Nueva lista: ahora abre un Popup.
        boton_nueva_lista = BotonAccion(
            color_fondo=(0.09, 0.42, 0.53, 1),
            text="Nueva lista\nde ventas"
        )

        boton_nueva_lista.bind(
            on_release=lambda instancia:
            self.abrir_nueva_lista()
        )

        opciones.add_widget(boton_nueva_lista)

        # Registrar ventas individuales.
        boton_registrar = BotonAccion(
            color_fondo=(0.44, 0.22, 0.65, 1),
            text="Registrar ventas\nindividuales"
        )

        boton_registrar.bind(
            on_release=lambda instancia:
            setattr(self.manager, "current", "registrar_ventas")
        )

        opciones.add_widget(boton_registrar)

        # Listas de ventas.
        boton_listas = BotonAccion(
            color_fondo=(0.85, 0.29, 0.27, 1),
            text="Listas de ventas"
        )

        boton_listas.bind(
            on_release=lambda instancia:
            setattr(self.manager, "current", "listas_ventas")
        )

        opciones.add_widget(boton_listas)

        # Historial de ventas.
        boton_historial = BotonAccion(
            color_fondo=(0.14, 0.35, 0.72, 1),
            text="Historial de ventas"
        )

        boton_historial.bind(
            on_release=lambda instancia:
            setattr(self.manager, "current", "historial_ventas")
        )

        opciones.add_widget(boton_historial)

        pantalla.add_widget(opciones)

        # Volver al inicio.
        boton_volver = BotonAccion(
            color_fondo=(0.02, 0.17, 0.43, 1),
            text="Volver",
            size_hint_y=None,
            height=dp(50),
            font_size=dp(16)
        )

        boton_volver.bind(
            on_release=lambda instancia:
            setattr(self.manager, "current", "inicio")
        )

        pantalla.add_widget(boton_volver)

        self.add_widget(pantalla)

    # --------------------------------------------------
    # POPUP PARA CREAR UNA NUEVA LISTA
    # --------------------------------------------------

    def abrir_nueva_lista(self):

        contenido = BoxLayout(
            orientation="vertical",
            padding=dp(18),
            spacing=dp(12)
        )

        # Título del formulario.
        contenido.add_widget(
            Label(
                text="Nueva lista de ventas",
                font_size=dp(21),
                bold=True,
                color=(0.07, 0.15, 0.35, 1),
                size_hint_y=None,
                height=dp(35)
            )
        )

        # Campo del nombre.
        contenido.add_widget(
            Label(
                text="Nombre de la lista",
                font_size=dp(15),
                bold=True,
                color=(0.07, 0.15, 0.35, 1),
                size_hint_y=None,
                height=dp(25)
            )
        )

        entrada_nombre = TextInput(
        hint_text="Ejemplo: Postres",
        multiline=False,
        size_hint_y=None,
        height=dp(48),
        font_size=dp(16),
        padding=[dp(12), dp(12)],
        background_normal="",
        background_active="",
        background_color=(0.88, 0.94, 0.98, 1),
        foreground_color=(0.07, 0.15, 0.35, 1),
        cursor_color=(0.02, 0.25, 0.65, 1),
        hint_text_color=(0.40, 0.46, 0.55, 1)
    )

        contenido.add_widget(entrada_nombre)

        # Campo del precio.
        contenido.add_widget(
            Label(
                text="Precio unitario (B/.)",
                font_size=dp(15),
                bold=True,
                color=(0.07, 0.15, 0.35, 1),
                size_hint_y=None,
                height=dp(25)
            )
        )

        entrada_precio = TextInput(
        hint_text="Ejemplo: 2.00",
        multiline=False,
        input_filter="float",
        size_hint_y=None,
        height=dp(48),
        font_size=dp(16),
        padding=[dp(12), dp(12)],
        background_normal="",
        background_active="",
        background_color=(0.88, 0.94, 0.98, 1),
        foreground_color=(0.07, 0.15, 0.35, 1),
        cursor_color=(0.02, 0.25, 0.65, 1),
        hint_text_color=(0.40, 0.46, 0.55, 1)
    )
        contenido.add_widget(entrada_precio)

        # Botones.
        botones = BoxLayout(
            size_hint_y=None,
            height=dp(45),
            spacing=dp(10)
        )

        boton_guardar = BotonAccion(
            color_fondo=(0.09, 0.42, 0.53, 1),
            text="Guardar",
            font_size=dp(15)
        )

        boton_cancelar = BotonAccion(
            color_fondo=(0.82, 0.16, 0.19, 1),
            text="Cancelar",
            font_size=dp(15)
        )

        botones.add_widget(boton_guardar)
        botones.add_widget(boton_cancelar)
        contenido.add_widget(botones)

        # Ventana emergente.
        ventana = PopupClaro(
            title="Mi Negocito",
            content=contenido,
            size_hint=(0.85, None),
            height=dp(365),
            auto_dismiss=False,
            background_color=(0.91, 0.96, 0.99, 1),
            separator_color=(1, 0.78, 0.12, 1),
            title_color=(0.07, 0.15, 0.35, 1),
            title_size=dp(17)
        )

        # ------------------------------------------
        # GUARDAR LA LISTA
        # ------------------------------------------

        def guardar(instance):

            nombre = entrada_nombre.text.strip()
            precio_texto = entrada_precio.text.strip()

            if not nombre:
                self.mostrar_mensaje(
                    "Escribe el nombre de la lista."
                )
                return

            if not precio_texto:
                self.mostrar_mensaje(
                    "Escribe el precio unitario."
                )
                return

            try:
                precio = Decimal(precio_texto)

                if not precio.is_finite():
                    self.mostrar_mensaje(
                        "Escribe un precio válido."
                    )
                    return

                if precio <= 0:
                    self.mostrar_mensaje(
                        "El precio debe ser mayor que cero."
                    )
                    return

                if precio.as_tuple().exponent < -2:
                    self.mostrar_mensaje(
                        "El precio no puede tener más de dos decimales."
                    )
                    return

                exito, mensaje = crear_lista_ventas(
                    nombre,
                    precio
                )

                if exito:
                    ventana.dismiss()
                    self.mostrar_mensaje(mensaje)
                else:
                    self.mostrar_mensaje(mensaje)

            except InvalidOperation:
                self.mostrar_mensaje(
                    "El precio debe ser un número válido."
                )

        boton_guardar.bind(on_release=guardar)
        boton_cancelar.bind(
            on_release=lambda instance: ventana.dismiss()
        )

        ventana.open()

    
    # --------------------------------------------------
    # MENSAJE EMERGENTE
    # --------------------------------------------------

    def mostrar_mensaje(self, mensaje):

        contenido = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10)
        )

        etiqueta = Label(
            text=mensaje,
            color=(0.07, 0.15, 0.35, 1),
            font_size=dp(16),
            halign="center",
            valign="middle",
            size_hint_y=None,
            height=dp(65)
        )

        etiqueta.bind(
            width=lambda instancia, valor:
            setattr(instancia, "text_size", (valor - dp(10), None))
        )

        contenido.add_widget(etiqueta)

        boton_aceptar = BotonAccion(
            color_fondo=(0.02, 0.25, 0.65, 1),
            text="Aceptar",
            size_hint=(0.65, None),
            height=dp(42),
            pos_hint={"center_x": 0.5},
            font_size=dp(15)
        )

        contenido.add_widget(boton_aceptar)

        ventana = PopupClaro(
            title="Mi Negocito",
            content=contenido,
            size_hint=(0.82, None),
            height=dp(190),
            separator_color=(1, 0.78, 0.12, 1),
            title_color=(0.07, 0.15, 0.35, 1),
            title_size=dp(17)
        )

        boton_aceptar.bind(
            on_release=lambda instancia: ventana.dismiss()
        )

        ventana.open()


    # --------------------------------------------------
    # MENSAJE EMERGENTE COMPACTO
    # --------------------------------------------------

    
def mostrar_mensaje(self, mensaje):

    contenido = BoxLayout(
        orientation="vertical",
        padding=[dp(18), dp(15)],
        spacing=dp(12)
    )

    # Texto centrado y ajustado al ancho disponible.
    etiqueta = Label(
        text=mensaje,
        color=(0.07, 0.15, 0.35, 1),
        font_size=dp(16),
        halign="center",
        valign="middle",
        size_hint_y=None,
        height=dp(65)
    )

    # Ajustar el texto al ancho de la etiqueta.
    etiqueta.bind(
        width=lambda instancia, valor:
        setattr(
            instancia,
            "text_size",
            (valor - dp(10), None)
        )
    )

    contenido.add_widget(etiqueta)

    # Botón aceptar.
    boton_aceptar = BotonAccion(
        color_fondo=(0.02, 0.25, 0.65, 1),
        text="Aceptar",
        size_hint=(0.65, None),
        height=dp(42),
        pos_hint={"center_x": 0.5},
        font_size=dp(15)
    )

    contenido.add_widget(boton_aceptar)

    # Ventana de confirmación.
    ventana = PopupClaro(
        title="Mi Negocito",
        content=contenido,
        size_hint=(0.82, None),
        height=dp(190),
        separator_color=(1, 0.78, 0.12, 1),
        title_color=(0.07, 0.15, 0.35, 1),
        title_size=dp(17)
    )

    boton_aceptar.bind(
        on_release=lambda instancia: ventana.dismiss()
    )

    ventana.open()
