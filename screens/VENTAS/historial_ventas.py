from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import  Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup

from ventas_db import listar_ventas_individuales, consultar_detalle_venta, eliminar_venta_individual

class HistorialVentasScreen(Screen):
    def __init__(self, **kwargs): #inicializa correctamente la pantalla 
        super().__init__(**kwargs)

        pantalla = BoxLayout(orientation='vertical', padding=20, spacing=15) #contenedor principal de la pantalla, que contiene todos los elementos de la pantalla
        
        titulo = Label(text='Historial  de Ventas', font_size=32, size_hint_y=None, height=60) #titulo de la pantalla
        pantalla.add_widget(titulo) #agrega el titulo a la pantalla


        boton_volver = Button(text='Volver', font_size=18, size_hint_y=None, height=50) #botón que permite volver a la pantalla anterior
        boton_volver.bind(on_press=lambda x: setattr(self.manager, 'current', 'mis_ventas'))  # Cambia a la pantalla de Mis Ventas al presionar el botón
       

        self.add_widget(pantalla) #agrega el contenedor principal a la pantalla
            
        
        # Tabla principal del historial
        self.tabla = GridLayout(
            cols=6,
            spacing=1,
            size_hint_y=None
        )

        self.tabla.bind(
            minimum_height=self.tabla.setter("height")
        )

        # Encabezados
        encabezados = [
            "N.º",
            "Fecha",
            "Cliente",
            "Total",
            "Eliminar"
        ]

        for encabezado in encabezados:

            celda = Label(
                text=encabezado,
                bold=True,
                size_hint_y=None,
                height=45,
                color=(1, 1, 1, 1)
            )

            celda.canvas.before.clear()

            self.tabla.add_widget(celda)

        # Contenedor desplazable
        self.scroll = ScrollView(
            size_hint=(1, 1)
        )

        self.scroll.add_widget(self.tabla)

        pantalla.add_widget(self.scroll)

        self.cargar_ventas()

        pantalla.add_widget(boton_volver)

        

    def cargar_ventas(self):

        self.tabla.clear_widgets()

        encabezados = [
            "N.º",
            "Fecha",
            "Cliente",
            "Total",
            "Ver detalles",
            "Eliminar"
        ]

        for encabezado in encabezados:
            self.tabla.add_widget(
                Label(
                    text=encabezado,
                    bold=True,
                    size_hint_y=None,
                    height=45,
                    color=(1, 1, 1, 1)
                )
            )

        ventas = listar_ventas_individuales()

        if not ventas:
            self.tabla.add_widget(
                Label(
                    text="No hay ventas registradas",
                    size_hint_y=None,
                    height=45
                )
            )
            return

        for venta in ventas:

            fecha = venta["fecha_venta"]

            if fecha:
                fecha = fecha.strftime("%d/%m/%Y")
            else:
                fecha = ""

            datos = [
                str(venta["id_ventas"]),
                fecha,
                venta["nombre_cliente"] or "",
                f'B/. {venta["total"]:.2f}'
            ]

            for dato in datos:
                self.tabla.add_widget(
                    Label(
                        text=dato,
                        size_hint_y=None,
                        height=50
                    )
                )

                # Esto hace que cada fila del historial tenga su propio botón para consultar los productos de esa venta.
            boton_detalles = Button(
                        text="Ver detalles",
                        size_hint_y=None,
                        height=40
                    )

            boton_detalles.bind(
                        on_press=lambda instancia, id_venta=venta["id_ventas"]:
                            self.ver_detalles(id_venta)
                    )

            self.tabla.add_widget(boton_detalles)

            boton_eliminar = Button(
                text="Eliminar",
                size_hint_y=None,
                height=40
            )

            boton_eliminar.bind(
                on_press=lambda instancia, id_venta=venta["id_ventas"]:
                    self.confirmar_eliminacion(id_venta)
            )

            self.tabla.add_widget(boton_eliminar)

        # consulta los productos que componen una venta individual y mostrarlos en una ventana emergente dentro de Mi Negocito.
    def ver_detalles(self, id_venta):

        detalles = consultar_detalle_venta(id_venta)

        if not detalles:
            self.mostrar_mensaje(
                "Esta venta no tiene productos registrados."
            )
            return

        # Datos generales de la venta
        venta = detalles[0]

        fecha = venta["fecha_venta"]

        if fecha:
            fecha = fecha.strftime("%d/%m/%Y")
        else:
            fecha = ""

        # Contenedor principal
        contenido = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=15
        )

        # Encabezado de la factura
        encabezado = Label(
            text="[b]MI NEGOCITO[/b]\nFACTURA DE VENTA",
            markup=True,
            font_size=24,
            size_hint_y=None,
            height=85
        )

        contenido.add_widget(encabezado)

        # Número de factura
        numero = Label(
            text=f"N.º {id_venta}",
            size_hint_y=None,
            height=30
        )

        contenido.add_widget(numero)

        # Datos del cliente
        cliente = Label(
            text=f'Cliente: {venta["nombre_cliente"] or "Sin nombre"}',
            size_hint_y=None,
            height=35
        )

        contenido.add_widget(cliente)

        fecha_label = Label(
            text=f"Fecha: {fecha}",
            size_hint_y=None,
            height=30
        )

        contenido.add_widget(fecha_label)

        # Tabla de productos
        tabla = GridLayout(
            cols=4,
            spacing=2,
            size_hint_y=None
        )

        tabla.bind(
            minimum_height=tabla.setter("height")
        )

        encabezados = [
            "Producto",
            "Cantidad",
            "Precio",
            "Subtotal"
        ]

        for texto in encabezados:
            tabla.add_widget(
                Label(
                    text=f"[b]{texto}[/b]",
                    markup=True,
                    size_hint_y=None,
                    height=40
                )
            )

        for producto in detalles:

            datos = [
                producto["producto"],
                str(producto["cantidad"]),
                f'B/. {producto["precio_unitario"]:.2f}',
                f'B/. {producto["subtotal"]:.2f}'
            ]

            for dato in datos:
                tabla.add_widget(
                    Label(
                        text=dato,
                        size_hint_y=None,
                        height=40
                    )
                )

        desplazamiento = ScrollView(
            size_hint=(1, 1)
        )

        desplazamiento.add_widget(tabla)

        contenido.add_widget(desplazamiento)

        # Total de la factura
        total = Label(
            text=f'[b]TOTAL: B/. {venta["total"]:.2f}[/b]',
            markup=True,
            font_size=22,
            size_hint_y=None,
            height=55
        )

        contenido.add_widget(total)

        # Botón cerrar
        boton_cerrar = Button(
            text="Cerrar",
            size_hint_y=None,
            height=45
        )

        contenido.add_widget(boton_cerrar)

        ventana = Popup(
            title="Detalle de venta",
            content=contenido,
            size_hint=(0.9, 0.85)
        )

        boton_cerrar.bind(
            on_press=ventana.dismiss
        )

        ventana.open()   

    def confirmar_eliminacion(self, id_venta):

        contenido = BoxLayout(
            orientation="vertical",
            spacing=10,
            padding=15
        )

        mensaje = Label(
            text=f"¿Estás segura de eliminar la venta N.º {id_venta}?"
        )

        boton_confirmar = Button(
            text="Sí, eliminar",
            size_hint_y=None,
            height=45
        )

        boton_cancelar = Button(
            text="Cancelar",
            size_hint_y=None,
            height=45
        )

        contenido.add_widget(mensaje)
        contenido.add_widget(boton_confirmar)
        contenido.add_widget(boton_cancelar)

        ventana = Popup(
            title="Confirmar eliminación",
            content=contenido,
            size_hint=(0.75, 0.45)
        )

        boton_cancelar.bind(
            on_press=ventana.dismiss
        )

        def eliminar(instancia):

            exito, mensaje = eliminar_venta_individual(id_venta)

            ventana.dismiss()


            if exito:
                self.cargar_ventas()

            self.mostrar_mensaje(mensaje)

        boton_confirmar.bind(
            on_press=eliminar
        )

        ventana.open()
