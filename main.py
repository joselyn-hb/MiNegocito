
import os

from kivy.app import App
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors import ButtonBehavior


# --------------------------------------------------
# RUTA PRINCIPAL DEL PROYECTO
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construye las rutas de los cinco iconos.
ICONOS = {
    "ventas": os.path.join(BASE_DIR, "assets", "icons", "ventas.png"),
    "rifas": os.path.join(BASE_DIR, "assets", "icons", "rifas.png"),
    "chance": os.path.join(BASE_DIR, "assets", "icons", "chance.png"),
    "clientes": os.path.join(BASE_DIR, "assets", "icons", "clientes.png"),
    "por_cobrar": os.path.join(BASE_DIR, "assets", "icons", "porcobrar.png"),
}


# --------------------------------------------------
# IMPORTACIÓN DE LAS PANTALLAS PRINCIPALES
# --------------------------------------------------

from screens.VENTAS.mis_ventas import MisVentasScreen
from screens.RIFAS.rifas import RifasScreen
from screens.CHANCE.chance import ChanceScreen
from screens.CLIENTES.clientes import ClientesScreen
from screens.POR_COBRAR.por_cobrar import PorCobrarScreen


# --------------------------------------------------
# PANTALLAS DEL MÓDULO RIFAS
# --------------------------------------------------

from screens.RIFAS.crear_rifa import CrearRifaScreen
from screens.RIFAS.rifas_activas import RifasActivasScreen
from screens.RIFAS.historial_rifas import HistorialRifasScreen
from screens.RIFAS.tablero_rifa import TableroRifaScreen


# --------------------------------------------------
# PANTALLAS DEL MÓDULO CHANCE
# --------------------------------------------------

from screens.CHANCE.nueva_lista import NuevaListaScreen
from screens.CHANCE.listas_activas import ListasActivasScreen
from screens.CHANCE.historial_listas import HistorialListasScreen


# --------------------------------------------------
# PANTALLAS DEL MÓDULO MIS VENTAS
# --------------------------------------------------

from screens.VENTAS.registrar_ventas import RegistrarVentasScreen
from screens.VENTAS.historial_ventas import HistorialVentasScreen
from screens.VENTAS.listas_ventas import ListasVentasScreen
from screens.VENTAS.pedidos_lista import PedidosListaScreen
from screens.VENTAS.detalle_pedido import DetallePedidoScreen


# --------------------------------------------------
# PANTALLAS DEL MÓDULO CLIENTES
# --------------------------------------------------

from screens.CLIENTES.nuevo_cliente import NuevoClienteScreen
from screens.CLIENTES.mis_clientes import MisClientesScreen
from screens.CLIENTES.buscar_cliente import BuscarClienteScreen
from screens.CLIENTES.historial_clientes import HistorialClienteScreen


# --------------------------------------------------
# TARJETA PERSONALIZADA DEL MENÚ PRINCIPAL
# --------------------------------------------------

class TarjetaMenu(ButtonBehavior, BoxLayout):

    def __init__(
        self,
        icono,
        titulo,
        descripcion,
        color_fondo,
        destino,
        gestor,
        horizontal=False,
        **kwargs
    ):
        super().__init__(
            orientation="horizontal" if horizontal else "vertical",
            padding=dp(12),
            spacing=dp(5),
            size_hint_y=None,
            height=dp(105) if horizontal else dp(145),
            **kwargs
        )

        self.destino = destino
        self.gestor = gestor

        # Dibuja el fondo de la tarjeta con esquinas redondeadas.
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

        # Comprueba que el archivo del icono exista.
        if not os.path.isfile(icono):
            raise FileNotFoundError(
                f"No se encontró el icono: {icono}"
            )

        # Carga la imagen PNG conservando sus proporciones.
        if horizontal:

            etiqueta_icono = Image(
                source=icono,
                size_hint=(None, None),
                size=(dp(85), dp(85)),
                fit_mode="contain"
            )

            self.add_widget(etiqueta_icono)

            # Contenedor del título y la descripción.
            informacion = BoxLayout(
                orientation="vertical",
                spacing=dp(3)
            )

            informacion.add_widget(
                Label(
                    text=titulo,
                    font_size=22,
                    bold=True,
                    color=(1, 1, 1, 1),
                    halign="center",
                    valign="middle"
                )
            )

            informacion.add_widget(
                Label(
                    text=descripcion,
                    font_size=14,
                    color=(1, 1, 1, 1),
                    halign="center",
                    valign="middle"
                )
            )

            self.add_widget(informacion)

            # Flecha indicadora.
            self.add_widget(
                Label(
                    text="›",
                    font_size=42,
                    color=(1, 1, 1, 1),
                    size_hint_x=None,
                    width=dp(30)
                )
            )

        else:

            etiqueta_icono = Image(
                source=icono,
                size_hint=(1, None),
                height=dp(65),
                fit_mode="contain"
            )

            self.add_widget(etiqueta_icono)

            self.add_widget(
                Label(
                    text=titulo,
                    font_size=21,
                    bold=True,
                    color=(1, 1, 1, 1),
                    size_hint_y=None,
                    height=dp(32)
                )
            )

            self.add_widget(
                Label(
                    text=descripcion,
                    font_size=14,
                    color=(1, 1, 1, 1),
                    size_hint_y=None,
                    height=dp(25)
                )
            )

        # Abre el módulo correspondiente al pulsar la tarjeta.
        self.bind(
            on_release=lambda instancia:
            setattr(self.gestor, "current", self.destino)
        )

    # Actualiza el fondo cuando cambia el tamaño de la tarjeta.
    def actualizar_fondo(self, instancia, valor):
        self.fondo.pos = instancia.pos
        self.fondo.size = instancia.size


# --------------------------------------------------
# APLICACIÓN PRINCIPAL
# --------------------------------------------------

class MiNegocitoApp(App):

    def build(self):

        # Crea el administrador de pantallas.
        gestor = ScreenManager()

        # Crea la pantalla de inicio.
        inicio = Screen(name="inicio")

        # Contenedor principal de la pantalla.
        pantalla = BoxLayout(
            orientation="vertical",
            padding=[dp(18), dp(12), dp(18), dp(12)],
            spacing=dp(12)
        )

        # Fondo general azul claro.
        with pantalla.canvas.before:
            Color(0.91, 0.96, 0.99, 1)
            fondo_general = RoundedRectangle(
                pos=pantalla.pos,
                size=pantalla.size
            )

        pantalla.bind(
            pos=lambda instancia, valor:
            setattr(fondo_general, "pos", valor),
            size=lambda instancia, valor:
            setattr(fondo_general, "size", valor)
        )

        # ------------------------------------------
        # ENCABEZADO AZUL
        # ------------------------------------------

        encabezado = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(3),
            size_hint_y=None,
            height=dp(115)
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
                text="Mi Negocito",
                font_size=29,
                bold=True,
                color=(1, 1, 1, 1)
            )
        )

        encabezado.add_widget(
            Label(
                text="Tu negocio organizado en un solo lugar",
                font_size=14,
                color=(1, 1, 1, 1)
            )
        )

        pantalla.add_widget(encabezado)

        # ------------------------------------------
        # LÍNEA DECORATIVA AMARILLA
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
        # TÍTULO DE LOS MÓDULOS
        # ------------------------------------------

        pantalla.add_widget(
            Label(
                text="¿Qué deseas administrar?",
                font_size=24,
                bold=True,
                color=(0.07, 0.15, 0.35, 1),
                size_hint_y=None,
                height=dp(48)
            )
        )

        # ------------------------------------------
        # CUADRÍCULA DE LOS CUATRO MÓDULOS
        # ------------------------------------------

        tarjetas = GridLayout(
            cols=2,
            spacing=dp(12),
            size_hint_y=None,
            row_default_height=dp(145),
            row_force_default=True
        )

        tarjetas.bind(
            minimum_height=tarjetas.setter("height")
        )

        # Mis ventas: azul petróleo.
        tarjetas.add_widget(
            TarjetaMenu(
                icono=ICONOS["ventas"],
                titulo="Mis ventas",
                descripcion="Control de ventas",
                color_fondo=(0.09, 0.42, 0.53, 1),
                destino="mis_ventas",
                gestor=gestor
            )
        )

        # Rifas: morado profundo.
        tarjetas.add_widget(
            TarjetaMenu(
                icono=ICONOS["rifas"],
                titulo="Rifas",
                descripcion="Gestiona tus rifas",
                color_fondo=(0.44, 0.22, 0.65, 1),
                destino="rifas",
                gestor=gestor
            )
        )

        # Chance: coral rojizo.
        tarjetas.add_widget(
            TarjetaMenu(
                icono=ICONOS["chance"],
                titulo="Chance",
                descripcion="Control de pedazos",
                color_fondo=(0.85, 0.29, 0.27, 1),
                destino="chance",
                gestor=gestor
            )
        )

        # Clientes: azul real.
        tarjetas.add_widget(
            TarjetaMenu(
                icono=ICONOS["clientes"],
                titulo="Clientes",
                descripcion="Tu cartera de clientes",
                color_fondo=(0.14, 0.35, 0.72, 1),
                destino="clientes",
                gestor=gestor
            )
        )

        pantalla.add_widget(tarjetas)

        # ------------------------------------------
        # POR COBRAR: TARJETA HORIZONTAL
        # ------------------------------------------

        pantalla.add_widget(
            TarjetaMenu(
                icono=ICONOS["por_cobrar"],
                titulo="Por cobrar",
                descripcion="Control de cuentas pendientes",
                color_fondo=(0.137, 0.608, 0.396, 1),
                destino="por_cobrar",
                gestor=gestor,
                horizontal=True
            )
        )

        # ------------------------------------------
        # PIE DE PANTALLA AZUL MARINO
        # ------------------------------------------

        pie = BoxLayout(
            size_hint_y=None,
            height=dp(42),
            padding=dp(5)
        )

        with pie.canvas.before:
            Color(0.02, 0.17, 0.43, 1)
            fondo_pie = RoundedRectangle(
                pos=pie.pos,
                size=pie.size,
                radius=[dp(12)]
            )

        pie.bind(
            pos=lambda instancia, valor:
            setattr(fondo_pie, "pos", valor),
            size=lambda instancia, valor:
            setattr(fondo_pie, "size", valor)
        )

        pie.add_widget(
            Label(
                text="Mi Negocito · Gestión para emprendedores",
                font_size=13,
                color=(1, 1, 1, 1)
            )
        )

        pantalla.add_widget(pie)

        # Agrega el menú a la pantalla de inicio.
        inicio.add_widget(pantalla)
        gestor.add_widget(inicio)

        # ------------------------------------------
        # REGISTRO DE LAS PANTALLAS EXISTENTES
        # ------------------------------------------

        gestor.add_widget(RifasScreen(name="rifas"))
        gestor.add_widget(ChanceScreen(name="chance"))
        gestor.add_widget(MisVentasScreen(name="mis_ventas"))
        gestor.add_widget(PorCobrarScreen(name="por_cobrar"))

        # Pantallas de Chance.
        gestor.add_widget(NuevaListaScreen(name="nueva_lista"))
        gestor.add_widget(ListasActivasScreen(name="listas_activas"))
        gestor.add_widget(HistorialListasScreen(name="historial_listas"))

        # Pantallas de Rifas.
        gestor.add_widget(CrearRifaScreen(name="crear_rifa"))
        gestor.add_widget(RifasActivasScreen(name="rifas_activas"))
        gestor.add_widget(HistorialRifasScreen(name="historial_rifas"))
        gestor.add_widget(TableroRifaScreen(name="tablero_rifa"))

        # Pantallas de Mis ventas.
        gestor.add_widget(HistorialVentasScreen(name="historial_ventas"))
        gestor.add_widget(RegistrarVentasScreen(name="registrar_ventas"))
        gestor.add_widget(ListasVentasScreen(name="listas_ventas"))
        gestor.add_widget(PedidosListaScreen(name="pedidos_lista"))
        gestor.add_widget(DetallePedidoScreen(name="detalle_pedido"))

        # Pantallas de Clientes.
        gestor.add_widget(ClientesScreen(name="clientes"))
        gestor.add_widget(MisClientesScreen(name="mis_clientes"))
        gestor.add_widget(NuevoClienteScreen(name="nuevo_cliente"))
        gestor.add_widget(BuscarClienteScreen(name="buscar_cliente"))
        gestor.add_widget(HistorialClienteScreen(name="historial_clientes"))

        # Devuelve el administrador de pantallas.
        return gestor


# --------------------------------------------------
# INICIAR LA APLICACIÓN
# --------------------------------------------------

if __name__ == "__main__":
    MiNegocitoApp().run()
