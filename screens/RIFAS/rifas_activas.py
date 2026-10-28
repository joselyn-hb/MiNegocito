from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from rifas_db import listar_rifas_activas
from kivy.uix.popup import Popup
from rifas_db import finalizar_rifa


class RifasActivasScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        pantalla = BoxLayout(orientation='vertical', padding=20, spacing=15)

        titulo = Label(text='Rifas activas', font_size=32, size_hint_y=None, height=60)
        pantalla.add_widget(titulo)

        mensaje = Label(text='Lista de rifas activas:', font_size=18)
        pantalla.add_widget(mensaje)

        self.lista_rifas = BoxLayout(
            orientation ="vertical",
            spacing = 10,
            size_hint_y =None
        )

        self.lista_rifas.bind(
            minimum_height=self.lista_rifas.setter("height")
        )
        desplazamiento =ScrollView()
        desplazamiento.add_widget(self.lista_rifas)

        pantalla.add_widget(desplazamiento)


            
        boton_volver = Button(text='Volver', font_size=18, size_hint_y=None, height=50)
        pantalla.add_widget(boton_volver)

        boton_volver.bind(on_press=lambda x: setattr(self.manager, 'current', 'rifas'))

        self.add_widget(pantalla)


    def on_enter(self):
        self.cargar_rifas()

    def cargar_rifas(self):
        self.lista_rifas.clear_widgets()

        rifas = listar_rifas_activas()
        print("RIFAS ENCONTRADAS:")

        if not rifas:
            self.lista_rifas.add_widget(
                Label(
                    text="No hay rifas activas registradas.",
                    size_hint_y=None,
                    height=50
                )
            )
            return

        for rifa in rifas:
            fecha = rifa["fecha_sorteo"]

            if fecha:
                fecha = fecha.strftime("%d/%m/%Y")
            else:
                fecha = "Sin fecha definida"

            tarjeta = Button(
                text=(
                    f"{rifa['nombre']}\n"
                    f"Descripción: {rifa['descripcion'] or 'Sin descripción'}\n"
                    f"Precio por número: B/. {rifa['precio_numero']:.2f}\n"
                    f"Sorteo: {fecha}"
                ),
                font_size=16,
                size_hint_y=None,
                height=130
            )
            tarjeta.bind(on_press=lambda instancia, r=rifa:
                         self.abrir_tablero(r))

            self.lista_rifas.add_widget(tarjeta)


    def abrir_tablero(self, rifa):
        contenido = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        contenido.add_widget(
            Label(
                text=f"¿Qué deseas hacer con la rifa\n"
                     f"{rifa['nombre']}?",
                font_size=18
            )
        )

        boton_tablero = Button(
            text="Abrir tablero",
            size_hint_y=None,
            height=45
        )

        boton_finalizar = Button(
            text="Finalizar rifa",
            size_hint_y=None,
            height=45
        )

        boton_cancelar = Button(
            text="Cancelar",
            size_hint_y=None,
            height=45
        )

        contenido.add_widget(boton_tablero)
        contenido.add_widget(boton_finalizar)
        contenido.add_widget(boton_cancelar)

        ventana = Popup(
            title="Opciones de la rifa",
            content=contenido,
            size_hint=(0.85, 0.55),
            auto_dismiss=False
        )

        def abrir_tablero_seleccionado(instancia):
            ventana.dismiss()

            tablero = self.manager.get_screen("tablero_rifa")
            tablero.mostrar_rifa(
                rifa["id_rifa"],
                rifa["nombre"]
            )
            self.manager.current = "tablero_rifa"

        def confirmar_finalizacion(instancia):
            ventana_confirmacion = Popup(
                title="Confirmar finalización",
                size_hint=(0.85, 0.4),
                auto_dismiss=False
            )

            panel = BoxLayout(
                orientation="vertical",
                padding=15,
                spacing=10
            )

            panel.add_widget(
                Label(
                    text=f"¿Finalizar la rifa {rifa['nombre']}?\n"
                         "Ya no aparecerá en Rifas Activas."
                )
            )

            botones = BoxLayout(
                size_hint_y=None,
                height=45,
                spacing=10
            )

            boton_si = Button(text="Sí, finalizar")
            boton_no = Button(text="Cancelar")

            botones.add_widget(boton_si)
            botones.add_widget(boton_no)
            panel.add_widget(botones)

            ventana_confirmacion.content = panel

            def ejecutar_finalizacion(instancia):
                exito, mensaje = finalizar_rifa(rifa["id_rifa"])

                ventana_confirmacion.dismiss()
                ventana.dismiss()

                self.cargar_rifas()
                self.mostrar_mensaje(mensaje)

            boton_si.bind(on_press=ejecutar_finalizacion)
            boton_no.bind(
                on_press=lambda instancia:
                    ventana_confirmacion.dismiss()
            )

            ventana_confirmacion.open()

        boton_tablero.bind(on_press=abrir_tablero_seleccionado)
        boton_finalizar.bind(on_press=confirmar_finalizacion)
        boton_cancelar.bind(
            on_press=lambda instancia: ventana.dismiss()
        )

        ventana.open()

    def mostrar_mensaje(self, mensaje):
        contenido = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        contenido.add_widget(Label(text=mensaje))

        boton_aceptar = Button(
            text="Aceptar",
            size_hint_y=None,
            height=45
        )
        contenido.add_widget(boton_aceptar)

        ventana_mensaje = Popup(
            title="Mi Negocito",
            content=contenido,
            size_hint=(0.8, 0.4)
        )

        boton_aceptar.bind(
            on_press=lambda instancia: ventana_mensaje.dismiss()
        )

        ventana_mensaje.open()


