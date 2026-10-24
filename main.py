from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

# PERMITE A KIVY MANEJAR DIFERENTES PANTALLAS Y CAMBIAR DE UNA A OTRA
#ventanas principales: rifas, chance, susu, mis ventas, clientes, por cobrar
from kivy.uix.screenmanager import ScreenManager, Screen
from screens.VENTAS.mis_ventas import MisVentasScreen
from screens.RIFAS.rifas import RifasScreen
from screens.CHANCE.chance import ChanceScreen
from screens.SUSUS.susu import SusuScreen
from screens.CLIENTES.clientes import ClientesScreen
from screens.POR_COBRAR.por_cobrar import PorCobrarScreen


#PANTALLAS DE LA VENTANA RIFAS
from screens.RIFAS.crear_rifa import CrearRifaScreen
from screens.RIFAS.rifas_activas import RifasActivasScreen
from screens.RIFAS.historial_rifas import HistorialRifasScreen


#PANTALLAS DE LA VENTANA CHANCE
from screens.CHANCE.nueva_lista import NuevaListaScreen
from screens.CHANCE.listas_activas import ListasActivasScreen
from screens.CHANCE.historial_listas import HistorialListasScreen

#PANTALLAS DE LA VENTANA SUSUS
from screens.SUSUS.nuevo_susu import NuevoSusuScreen
from screens.SUSUS.susus_activos import SususActivosScreen
from screens.SUSUS.historial_susus import HistorialSususScreen

#PANTALLAS DE LA VENTANA MIS VENTAS
from screens.VENTAS.nueva_lista_ventas import NuevaListaVentasScreen
from screens.VENTAS.registrar_ventas import RegistrarVentasScreen
from screens.VENTAS.historial_ventas import HistorialVentasScreen

#PANTALLAS DE LA VENTANA CLIENTES
from screens.CLIENTES.nuevo_cliente import NuevoClienteScreen
from screens.CLIENTES.mis_clientes import MisClientesScreen
from screens.CLIENTES.buscar_cliente import BuscarClienteScreen
from screens.CLIENTES.historial_clientes import HistorialClienteScreen


class MiNegocitoApp(App):
    def build(self):
        pantalla = BoxLayout(orientation='vertical', padding=20, spacing=15)

        titulo = Label(text=' Mi Negocito', font_size=32, size_hint_y=None, height=60)
        subtitulo = Label(text='¡Tu negocio anotado en un solo lugar!', font_size=18, size_hint_y=None, height=50)
        
        
        #BOTONES PRINCIPALES
        boton_rifas = Button(text='Rifas', font_size=20)
        boton_chance = Button(text='Chance', font_size=20)
        boton_susu = Button(text='Susú', font_size=20)
        boton_mis_ventas = Button(text='Mis ventas', font_size=20)
        boton_clientes = Button(text='Clientes', font_size=20)
        boton_por_cobrar = Button(text='Por cobrar', font_size=20)

        #VINCULA LOS BOTONES PRINCIPALES CON SUS PANTALLAS CORRESPONDIENTES
        boton_rifas.bind(on_press=lambda x: setattr(gestor, 'current', 'rifas'))  
        boton_chance.bind(on_press=lambda x: setattr(gestor, 'current', 'chance'))  
        boton_susu.bind(on_press=lambda x: setattr(gestor, 'current', 'susu'))  
        boton_mis_ventas.bind(on_press=lambda x: setattr(gestor, 'current', 'mis_ventas'))  
        boton_clientes.bind(on_press=lambda x: setattr(gestor, 'current', 'clientes')) 
        boton_por_cobrar.bind(on_press=lambda x: setattr(gestor, 'current', 'por_cobrar')) 


        #AGREGA LOS WIDGETS A LA PANTALLA PRINCIPAL
        pantalla.add_widget(titulo)
        pantalla.add_widget(subtitulo)
        pantalla.add_widget(boton_rifas)
        pantalla.add_widget(boton_chance)
        pantalla.add_widget(boton_susu)
        pantalla.add_widget(boton_mis_ventas)
        pantalla.add_widget(boton_clientes)
        pantalla.add_widget(boton_por_cobrar)




        ##########  CREACIÓN DEL GESTOR DE PANTALLAS   ################ 
        gestor=ScreenManager() 
        inicio= Screen(name='inicio') 
        inicio.add_widget(pantalla)


        #REGISTRA TODAS LAS PANTALLAS AL GESTOR DE PANTALLAS PARA PODER ACCEDER A ELLAS DESDE CUALQUIER PANTALLA
        gestor.add_widget(inicio) 
        gestor.add_widget(RifasScreen(name='rifas'))
        gestor.add_widget(ChanceScreen(name='chance')) 
        gestor.add_widget(SusuScreen(name='susu')) 
        gestor.add_widget(MisVentasScreen(name='mis_ventas')) 
        gestor.add_widget(PorCobrarScreen(name='por_cobrar')) 
        gestor.add_widget(NuevaListaScreen(name='nueva_lista'))
        gestor.add_widget(ListasActivasScreen(name='listas_activas')) 
        gestor.add_widget(HistorialListasScreen(name='historial_listas')) 
        gestor.add_widget(CrearRifaScreen(name='crear_rifa')) 
        gestor.add_widget(RifasActivasScreen(name='rifas_activas')) 
        gestor.add_widget(HistorialRifasScreen(name='historial_rifas'))
        gestor.add_widget(NuevoSusuScreen(name='nuevo_susu'))
        gestor.add_widget(SususActivosScreen(name='susus_activos'))
        gestor.add_widget(HistorialSususScreen(name='historial_susus'))
        gestor.add_widget(HistorialVentasScreen(name='historial_ventas')) 
        gestor.add_widget(RegistrarVentasScreen(name='registrar_ventas'))
        gestor.add_widget(NuevaListaVentasScreen(name='nueva_lista_ventas'))
        gestor.add_widget(ClientesScreen(name='clientes'))
        gestor.add_widget(MisClientesScreen(name='mis_clientes'))
        gestor.add_widget(NuevoClienteScreen(name='nuevo_cliente'))
        gestor.add_widget(BuscarClienteScreen(name='buscar_cliente'))  # Agrega la pantalla de buscar cliente al gestor de pantallas
        gestor.add_widget(HistorialClienteScreen(name='historial_clientes'))  # Agrega la pantalla de historial de clientes al gestor de pantallas
       

        #RETORNA EL GESTOR DE PANTALLAS PARA QUE KIVY PUEDA MOSTRAR LA PANTALLA INICIAL
        return gestor
    


if __name__ == '__main__':
    MiNegocitoApp().run()