from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from rifas_db import listar_participantes_rifa
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from rifas_db import registrar_participante_rifa
from rifas_db import liberar_numero_rifa
from rifas_db import actualizar_pago_rifa




class TableroRifaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Guarda la rifa seleccionada y prepara el contenedor principal.
        self.id_rifa = None
        self.nombre_rifa =""
        pantalla = BoxLayout(orientation="vertical", padding=15, spacing=10)

        # Muestra el título y las indicaciones del tablero.
        self.titulo = Label(
            text="Tablero de rifa", font_size=26, size_hint_y=None,height=50)

        pantalla.add_widget(self.titulo)


        self.informacion = Label(
                    text="seleccion auna rifa para ver tus numeros", font_size=16, size_hint_y=None,height=40)
        
        pantalla.add_widget(self.informacion)


        # Permite desplazar el tablero si no cabe completo en la pantalla.
        desplazamiento =ScrollView()

        self.tablero = GridLayout(
                cols=10,
                spacing=4,
                padding=4,
                size_hint_y=None)

        self.tablero.bind(
            minimum_height=self.tablero.setter("height"))


        desplazamiento.add_widget(self.tablero)

        pantalla.add_widget(desplazamiento)

        # Regresa a la pantalla de rifas activas.
        boton_volver = Button(text='Volver a Rifas Activas', size_hint_y=None, height=50)
        boton_volver.bind(on_press=lambda instancia: setattr(self.manager, 'current', 'rifas_activas'))
        pantalla.add_widget(boton_volver)

        self.add_widget(pantalla)

    def mostrar_rifa(self, id_rifa, nombre):

        # Actualiza la rifa mostrada y elimina el tablero anterior.
        self.id_rifa = id_rifa
        self.nombre_rifa = nombre

        self. titulo.text = f"Rifa:{nombre}"
        self.informacion.text = "verde:disponible | Rojo: asignado"
        self.tablero.clear_widgets()

        # Consulta qué números están registrados para esta rifa.
        participantes = listar_participantes_rifa(id_rifa)
        numeros_registrados = {str(p["numero"]).zfill(2):
                               p
                               for p in participantes}

        # Crea los botones del 00 al 99 y determina el color de cada número.
        for numero in range(100):
            texto_numero = f"{numero:02d}"
            participante = numeros_registrados.get(texto_numero)

            if participante is None:
                color = (0.14, 0.55, 0.25, 1)
            elif participante.get("estado") == "reservado":
                color = (0.85, 0.60, 0.10, 1)
            else:
                color = (0.75, 0.18, 0.18, 1)

            pagado = participante.get("pagado") if participante else 0
            estado = participante.get("estado") if participante else None
            mostrar_etiqueta = (
                participante is not None
                and estado == "ocupado"
                and str(pagado).lower() in ("1", "true", "pagado", "si")
            )

            casilla = BoxLayout(
                orientation="vertical",
                spacing=0,
                size_hint_y=None,
                height=58
            )

            etiqueta_texto = "PAGADO" if mostrar_etiqueta else ""
            etiqueta = Label(
                text=etiqueta_texto,
                font_size=9,
                bold=True,
                color=(1, 1, 1, 1),
                size_hint_y=None,
                height=16
            )
            casilla.add_widget(etiqueta)

            boton = Button(
                text=texto_numero,
                font_size=14,
                size_hint_y=None,
                height=42,
                background_normal="",
                background_color=color
            )
            boton.bind(
                on_press=lambda instancia, n=texto_numero, p=participante:
                    self.accion_numero(n, p)
            )

            casilla.add_widget(boton)
            self.tablero.add_widget(casilla)
                
        
            
    def accion_numero(self, numero,
                      participante):
            # Si el número aún no está asignado, se abre el formulario para
            # registrar al comprador y guardar la información del boleto.
            if participante is None:
             self.abrir_formulario_numero(numero)
            
            # Si el número ya tiene un participante, se muestra el detalle
            # completo del registro para consultarlo o actualizarlo.
            else:

             self.mostrar_detalle_numero(numero,participante)

    def mostrar_detalle_numero(self, numero, participante):
        contenido = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        nombre = participante.get("nombre_comprador") or "Sin nombre"
        telefono = participante.get("telefono_comprador") or "Sin teléfono"
        estado = participante.get("estado") or "ocupado"
        pago_guardado = participante.get("pagado")

        esta_pagado = str(pago_guardado).lower() in (
            "1", "true", "pagado", "si"
        )

        pago = "Pagado" if esta_pagado else "Pendiente"

        contenido.add_widget(
            Label(text=f"Número: {numero}", font_size=24)
        )
        contenido.add_widget(Label(text=f"Comprador: {nombre}"))
        contenido.add_widget(Label(text=f"Teléfono: {telefono}"))
        contenido.add_widget(Label(text=f"Estado: {estado.capitalize()}"))
        contenido.add_widget(Label(text=f"Pago: {pago}"))

        texto_boton_pago = (
            "Marcar como pendiente"
            if esta_pagado
            else "Marcar como pagado"
        )

        boton_pago = Button(
            text=texto_boton_pago,
            size_hint_y=None,
            height=45
        )
        contenido.add_widget(boton_pago)

        boton_liberar = Button(
            text="Liberar número",
            size_hint_y=None,
            height=45
        )
        contenido.add_widget(boton_liberar)

        boton_cerrar = Button(
            text="Cerrar",
            size_hint_y=None,
            height=45
        )
        contenido.add_widget(boton_cerrar)

        ventana = Popup(
            title=f"Detalle del número {numero}",
            content=contenido,
            size_hint=(0.9, 0.8),
            auto_dismiss=False
        )

        boton_cerrar.bind(
            on_press=lambda instancia: ventana.dismiss()
        )

        def cambiar_pago(instancia):
            nuevo_pago = 0 if esta_pagado else 1

            exito, mensaje = actualizar_pago_rifa(
                self.id_rifa,
                numero,
                nuevo_pago
            )

            if exito:
                ventana.dismiss()
                self.mostrar_rifa(
                    self.id_rifa,
                    self.nombre_rifa
                )

            self.mostrar_mensaje(mensaje)

        boton_pago.bind(on_press=cambiar_pago)

        def confirmar_liberacion(instancia):
            ventana_confirmacion = Popup(
                title="Confirmar liberación",
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
                    text=f"¿Liberar el número {numero}?\n"
                         "Se eliminará su asignación al comprador."
                )
            )

            botones = BoxLayout(
                size_hint_y=None,
                height=45,
                spacing=10
            )

            boton_si = Button(text="Sí, liberar")
            boton_no = Button(text="Cancelar")

            botones.add_widget(boton_si)
            botones.add_widget(boton_no)
            panel.add_widget(botones)

            ventana_confirmacion.content = panel

            def ejecutar_liberacion(instancia):
                exito, mensaje = liberar_numero_rifa(
                    self.id_rifa,
                    numero
                )

                ventana_confirmacion.dismiss()

                if exito:
                    ventana.dismiss()
                    self.mostrar_rifa(
                        self.id_rifa,
                        self.nombre_rifa
                    )

                self.mostrar_mensaje(mensaje)

            boton_si.bind(on_press=ejecutar_liberacion)
            boton_no.bind(
                on_press=lambda instancia:
                    ventana_confirmacion.dismiss()
            )

            ventana_confirmacion.open()

        boton_liberar.bind(on_press=confirmar_liberacion)
        ventana.open()


    def abrir_formulario_numero(self, numero):
        # Prepara el formulario del número seleccionado.
        contenido = BoxLayout(
            orientation="vertical",
            padding=15,
            spacing=10
        )

        contenido.add_widget(Label(text=f"Registrar número{numero}", font_size=22))

       
        # Recoge el nombre y el teléfono de la persona interesada.
        entrada_nombre = TextInput(hint_text="Nombre del comprador",
                                   multiline=False,
                                   size_hint_y=None,
                                   height=45)
        contenido.add_widget(entrada_nombre)


        entrada_telefono = TextInput(hint_text="Telefono del comprador",
                                           multiline=False,
                                           size_hint_y=None,
                                           height=45)
        contenido.add_widget(entrada_telefono)

        # Permite seleccionar si el número queda ocupado o reservado.
        selector_estado = Spinner(text="ocupado",
                                  values =("ocupado", "reservado"),
                                  size_hint_y=None,
                                   height=45 )

        contenido.add_widget(selector_estado)


        # Indica si el comprador pagó el número.
        selector_pago = Spinner(text="pendiente",
                                values=("pendiente", "pagado"),
                                size_hint_y=None,
                                height=45)

        contenido.add_widget(selector_pago)

        # Cierra el formulario sin guardar cambios.
        boton_guardar = Button(text="Guardar", size_hint_y=None, height=45)
        contenido.add_widget(boton_guardar)


        def guardar_numero(instancia):
            nombre = entrada_nombre.text.strip()
            telefono = entrada_telefono.text.strip()

            if not nombre:
                self.mostrar_mensaje(
                    "Escribe el nombre del comprador."
                )
                return

            estado = selector_estado.text
            pagado = 1 if selector_pago.text == "pagado" else 0

            exito, mensaje = registrar_participante_rifa(
                self.id_rifa,
                int(numero),
                nombre,
                telefono,
                estado,
                pagado
            )

            if exito:
                ventana.dismiss()
                self.mostrar_rifa(
                    self.id_rifa,
                    self.nombre_rifa
                )
                self.mostrar_mensaje(mensaje)
            else:
                self.mostrar_mensaje(mensaje)

        boton_guardar.bind(on_press=guardar_numero)

        

        # Cierra el formulario sin guardar cambios.
        boton_cerrar =Button(text="Cancelar", size_hint_y=None, height=45)
        contenido.add_widget(boton_cerrar)

        


        # Presenta el formulario en una ventana emergente.
        ventana = Popup(
            title=f"Rifa:{self.nombre_rifa}",
                        content=contenido,
                        size_hint=(0.90, 0.85),
                        auto_dismiss=False)
        
        boton_cerrar.bind(on_press= lambda instancia: ventana.dismiss())
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
        

        