# -*- coding: utf-8 -*-
__version__ = '1.0.0'

import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line
from kivy.utils import get_color_from_hex, platform
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window

# Configuración específica para Android
if platform == 'android':
    from android.permissions import request_permissions, Permission
    from android.storage import primary_external_storage_path
    
    def check_permissions(dt):
        request_permissions([
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE
        ])
    Clock.schedule_once(check_permissions, 0)
import weakref
from database import crear_tabla, migrar_tabla_tareas
from tasks import agregar_tarea, mostrar_tareas, marcar_completada, eliminar_tarea, obtener_tarea_por_id, actualizar_tarea, obtener_trabajadores, eliminar_trabajador, agregar_trabajador
import sqlite3
from kivy.uix.spinner import Spinner
from datetime import datetime
import pytz
from auth import crear_usuario, verificar_usuario, usuario_existe, obtener_rol_usuario
from kivy.uix.togglebutton import ToggleButton
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.metrics import dp

# Configuración global para móviles
from kivy.config import Config
Config.set('kivy', 'default_font', ['Roboto', 'Arial'])
Config.set('kivy', 'keyboard_mode', 'systemanddock')  
Config.set('kivy', 'keyboard_mode', 'systemandmulti')
Config.set('graphics', 'resizable', '0')  # Deshabilitar redimensionamiento
Config.set('graphics', 'width', '360')    # Ancho base para diseño
Config.set('graphics', 'height', '640')  
Config.set('postproc', 'retain_time', '100')  # Retener toques por más tiempo
Config.set('postproc', 'retain_distance', '50')  # Mayor margen para toques
Config.set('graphics', 'show_cursor', '1')
from kivy.animation import Animation


# Configuración de ventana
from kivy.metrics import dp
Window.softinput_mode = 'below_target' 
Window.size = (dp(360), dp(640))  # Usar dp para densidad independiente
Window.minimum_width, Window.minimum_height = dp(300), dp(500)


from kivy.config import Config
from kivy.core.window import Window

# Configuración esencial para dispositivos táctiles
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('kivy', 'keyboard_mode', 'systemandmulti')
Config.set('kivy', 'keyboard_layout', 'qwerty')
Config.set('graphics', 'multisamples', '0')  # Mejorar rendimiento táctil

# Ajustar ventana para dispositivos móviles
Window.softinput_mode = 'below_target'
Window.keyboard_anim_args = {'d': 0.2, 't': 'in_out_quad'}
from kivy.clock import Clock

ZONA_HORARIA = pytz.timezone('America/Lima')

# Paletas de colores
THEMES = {
    "light": {
        "background": get_color_from_hex("#8792F1"),
        "text": get_color_from_hex("#0F0A0A"),
        "primary": get_color_from_hex("#4285F4"),
        "btn_text": get_color_from_hex("#181515"),
        "secondary": get_color_from_hex("#EA4335")
    },
    "dark": {
        "background": get_color_from_hex("#B6ACAC"),
        "text": get_color_from_hex("#FFFFFF"),
        "primary": get_color_from_hex("#BB86FC"),
        "btn_text": get_color_from_hex("#0C0C0C"),
        "secondary": get_color_from_hex("#E05353")
    }
}

class SpinnerOption(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0.9, 0.9, 0.9, 1)
        self.color = (0, 0, 0, 1)
        self.size_hint_y = None
        self.height = 80
        self.font_size = '24sp'
        self.padding = (20, 10)

class TactileButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = ThemeManager.get_theme_colors()["primary"]
        self.color = ThemeManager.get_theme_colors()["btn_text"]
        self.font_size = '21sp'  # Reducir de 18sp a 16sp
        self.size_hint_y = None
        self.height = dp(80)  # Aumentado de 60
        self.padding = (dp(20), dp(15)) # Aumentar padding
        self.halign = 'center'
        self.valign = 'middle'
        self.minimum_width = dp(150)
        
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.background_color = [c * 0.7 for c in self.background_color]
            return super().on_touch_down(touch)
        return False
        
    def on_touch_up(self, touch):
        self.background_color = ThemeManager.get_theme_colors()["primary"]
        return super().on_touch_up(touch)

class ThemeManager:
    current_theme = "light"
    _observers = weakref.WeakSet()

    @classmethod
    def toggle_theme(cls):
        cls.current_theme = "dark" if cls.current_theme == "light" else "light"
        cls.notify_observers()
        return cls.current_theme

    @classmethod
    def add_observer(cls, observer):
        cls._observers.add(observer)

    @classmethod
    def notify_observers(cls):
        for observer in cls._observers:
            if hasattr(observer, 'update_theme'):
                observer.update_theme(cls.current_theme)

    @classmethod
    def get_theme_colors(cls):
        return THEMES[cls.current_theme]

class ThemedScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ThemeManager.add_observer(self)
        self.bind(size=self.update_rect, pos=self.update_rect)
        with self.canvas.before:
            self.bg_color = Color(*ThemeManager.get_theme_colors()["background"])
            self.rect = Rectangle(size=self.size, pos=self.pos)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_theme(self, theme):
        colors = ThemeManager.get_theme_colors()
        self.bg_color.rgba = colors["background"]
        self.apply_theme_colors(colors)

    def apply_theme_colors(self, colors):
        for child in self.children:
            if isinstance(child, (Label, TextInput)):
                child.color = colors["text"]
            elif isinstance(child, Button):
                child.background_color = colors["primary"]
                child.color = colors["btn_text"]

class LoginScreen(ThemedScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=dp(30), padding=[dp(30), dp(60), dp(30), dp(80)])
        
        # Campo de usuario
        self.username = TextInput(
            hint_text='Usuario',
            size_hint_y=None,
            height=dp(90),
            font_size=dp(25),
            background_normal='',
            background_color=(1, 1, 1, 0.7),
            padding=[dp(25), dp(20)],
            multiline=False,
            write_tab=False,
            foreground_color=(0, 0, 0, 1)
        )
        
        # Contenedor contraseña
        password_container = BoxLayout(
            orientation='horizontal', 
            size_hint_y=None, 
            height=dp(90),  # Altura aumentada
            spacing=dp(15) 
        )
        
        self.password = TextInput(
            hint_text='Contraseña',
            password=True,
            size_hint_x=0.75,
            font_size=dp(25),
            background_normal='',
            background_color=(1, 1, 1, 0.7),
            padding=[dp(25), dp(20)],
            multiline=False,
            foreground_color=(0, 0, 0, 1)
        )
        
        self.show_password = Button(
            text='MOSTRAR',
            size_hint_x=0.3,
            size_hint_y=1,
            background_normal='',
            background_color=(0.6, 0.6, 0.8, 1),
            color=(0, 0, 0, 1),
            font_size='14sp',
            bold=True
        )
        self.show_password.bind(on_press=self.toggle_password_visibility)
        
        password_container.add_widget(self.password)
        password_container.add_widget(self.show_password)
        
        # Botones principales
        btn_login = TactileButton(text='INICIAR SESIÓN',size_hint_y=None,height=dp(90))
        btn_login.bind(on_press=self.iniciar_sesion)
        
        btn_registro = TactileButton(
            text='REGISTRARSE',
            size_hint_y=None,
            height=dp(90),  # Aumentado de 60
            background_color=ThemeManager.get_theme_colors()["secondary"]
        )
        btn_registro.bind(on_press=self.ir_a_registro)
        
        layout.add_widget(Label(
            text='INICIAR SESIÓN', 
            font_size='24sp',
            size_hint_y=None,
            height=80
        ))
        layout.add_widget(self.username)
        layout.add_widget(password_container)
        layout.add_widget(btn_login)
        layout.add_widget(btn_registro)
        self.add_widget(layout)
    
    def toggle_password_visibility(self, instance):
        if self.password.password:
            self.password.password = False
            instance.text = 'OCULTAR'
            instance.background_color = (0.8, 0.6, 0.6, 1)
        else:
            self.password.password = True
            instance.text = 'MOSTRAR'
            instance.background_color = (0.6, 0.6, 0.8, 1)
    
    def iniciar_sesion(self, instance):
        username = self.username.text.strip()
        password = self.password.text.strip()
        
        if not username or not password:
            self.mostrar_mensaje('⚠️ Usuario y contraseña requeridos')
            return
        
        resultado = verificar_usuario(username, password)
        if resultado:
            usuario_id, rol = resultado
            self.manager.usuario_actual = usuario_id
            self.manager.es_admin = (rol == 'admin')
            
            mensaje = '✅ Sesión iniciada' + (' (Admin)' if rol == 'admin' else '')
            self.mostrar_mensaje(mensaje)
            self.manager.current = 'menu'
        else:
            self.mostrar_mensaje('❌ Credenciales incorrectas')
    
    def ir_a_registro(self, instance):
        self.manager.current = 'registro'
    
    def mostrar_mensaje(self, mensaje):
        colors = ThemeManager.get_theme_colors()
        popup = Popup(
            title='Mensaje',
            size_hint=(0.85, 0.5),
            title_size='20sp',  # Título más grande
            separator_height=dp(2),
            background='atlas://data/images/defaulttheme/button_pressed'
        )
        content = BoxLayout(orientation='vertical',spacing=dp(25),padding=dp(25))
        content.add_widget(Label(
            text=mensaje, 
            color=colors["text"],
            font_size='20sp'
        ))
        btn_ok = TactileButton(
            text='OK',
            size_hint_y=None,
            height=dp(80), 
            font_size='20sp'
        )
        btn_ok.bind(on_press=popup.dismiss)
        content.add_widget(btn_ok)
        popup.content = content
        popup.open()

class RegistroScreen(ThemedScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=25, padding=[40, 60, 40, 60])
        
        self.username = TextInput(
            hint_text='Usuario',
            size_hint_y=None,
            height=dp(100), 
            font_size=dp(24),
            background_normal='',
            background_color=(1, 1, 1, 0.9),
            padding=[dp(25), dp(20)],
            multiline=False,
            write_tab=False
        )
        
        # Contenedor para contraseña
        password_container = BoxLayout(
            orientation='horizontal', 
            size_hint_y=None, 
            height=dp(100),  # Aumentado
            spacing=dp(15)
        )
        
        self.password = TextInput(
            hint_text='Contraseña',
            password=True,
            size_hint_x=0.75,
            font_size='18sp',
            background_normal='',
            background_color=(1, 1, 1, 0.9),
            foreground_color=(0, 0, 0, 1),
            padding=[dp(25), dp(20)],
            multiline=False
        )
        
        self.show_password = TactileButton(
            text='MOSTRAR',
            size_hint_x=0.25,
            background_color=(0.6, 0.6, 0.8, 1),
            width=100,  # Añadir un ancho mínimo
            padding=(5, 5),  # Añadir padding interno
            text_size=(None, None),  # Permitir que el texto ocupe espacio natural
            halign='center'  # Centrar el texto
        )
        self.show_password.bind(on_press=self.toggle_password_visibility)
        
        password_container.add_widget(self.password)
        password_container.add_widget(self.show_password)
        
        # Contenedor para confirmar contraseña
        confirm_container = BoxLayout(
            orientation='horizontal', 
            size_hint_y=None, 
            height=dp(100),  # Aumentado
            spacing=dp(15)
        )
        
        self.confirm_password = TextInput(
            hint_text='Confirmar Contraseña',
            password=True,
            size_hint_x=0.75,
            font_size='18sp',
            background_normal='',
            background_color=(1, 1, 1, 0.9),
            foreground_color=(0, 0, 0, 1),
            padding=[dp(25), dp(20)],
            multiline=False
        )
        
        self.show_confirm_password = TactileButton(
            text='MOSTRAR',
            size_hint_x=0.25,
            background_color=(0.6, 0.6, 0.8, 1)
        )
        self.show_confirm_password.bind(on_press=self.toggle_confirm_password_visibility)
        
        confirm_container.add_widget(self.confirm_password)
        confirm_container.add_widget(self.show_confirm_password)
        
        btn_registro = TactileButton(text='REGISTRARSE')
        btn_registro.bind(on_press=self.registrar)
        
        btn_volver = TactileButton(
            text='VOLVER A LOGIN',
            background_color=ThemeManager.get_theme_colors()["secondary"]
        )
        btn_volver.bind(on_press=self.volver)
        
        layout.add_widget(Label(
            text='REGISTRO', 
            font_size='24sp',
            size_hint_y=None,
            height=80
        ))
        layout.add_widget(self.username)
        layout.add_widget(password_container)
        layout.add_widget(confirm_container)
        layout.add_widget(btn_registro)
        layout.add_widget(btn_volver)
        self.add_widget(layout)

    def toggle_password_visibility(self, instance):
        if self.password.password:
            self.password.password = False
            instance.text = 'OCULTAR'
            instance.background_color = (0.8, 0.6, 0.6, 1)
        else:
            self.password.password = True
            instance.text = 'MOSTRAR'
            instance.background_color = (0.6, 0.6, 0.8, 1)

    def toggle_confirm_password_visibility(self, instance):
        if self.confirm_password.password:
            self.confirm_password.password = False
            instance.text = 'OCULTAR'
            instance.background_color = (0.8, 0.6, 0.6, 1)
        else:
            self.confirm_password.password = True
            instance.text = 'MOSTRAR'
            instance.background_color = (0.6, 0.6, 0.8, 1)
    
    def registrar(self, instance):
        username = self.username.text.strip()
        password = self.password.text.strip()
        confirm_password = self.confirm_password.text.strip()
        
        if not username or not password:
            self.mostrar_mensaje('⚠️ Usuario y contraseña requeridos')
            return
            
        if password != confirm_password:
            self.mostrar_mensaje('⚠️ Las contraseñas no coinciden')
            return
            
        if usuario_existe(username):
            self.mostrar_mensaje('⚠️ El usuario ya existe')
            return
            
        if crear_usuario(username, password):
            self.mostrar_mensaje('✅ Usuario creado con éxito')
            self.volver(None)
        else:
            self.mostrar_mensaje('❌ Error al crear usuario')
    
    def volver(self, instance):
        self.manager.current = 'login'
        self.username.text = ''
        self.password.text = ''
        self.confirm_password.text = ''
    
    def mostrar_mensaje(self, mensaje):
        colors = ThemeManager.get_theme_colors()
        popup = Popup(
            title='Mensaje',
            size_hint=(0.8, 0.4),
            background='atlas://data/images/defaulttheme/button_pressed'
        )
        content = BoxLayout(orientation='vertical', spacing=15, padding=20)
        content.add_widget(Label(
            text=mensaje, 
            color=colors["text"],
            font_size='18sp'
        ))
        btn_ok = TactileButton(text='OK')
        btn_ok.bind(on_press=popup.dismiss)
        content.add_widget(btn_ok)
        popup.content = content
        popup.open()

class RootWidget(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = ScreenManager()
        self.sm.usuario_actual = None
        self.add_widget(self.sm)
        
        # Botón de tema táctil
        self.theme_btn = TactileButton(
            text='Light' if ThemeManager.current_theme == 'light' else 'Dark',
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={'right': 0.95, 'top': 0.95},
            font_size='16sp'
        )
        self.theme_btn.bind(on_press=self.toggle_theme)
        self.add_widget(self.theme_btn)
    
    def toggle_theme(self, instance):
        new_theme = ThemeManager.toggle_theme()
        colors = ThemeManager.get_theme_colors()
        instance.text = 'Light' if new_theme == 'light' else 'Dark'
        instance.background_color = colors["primary"]
        instance.color = colors["btn_text"]

class MenuPrincipal(ThemedScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=25, padding=[40, 60, 40, 60])
        
        self.title_label = Label(
            text='Gestor de Tareas', 
            font_size='24sp', 
            size_hint_y=None,
            height=80,
            color=ThemeManager.get_theme_colors()["text"]
        )
        self.layout.add_widget(self.title_label)
        
        btn_container = GridLayout(cols=1, spacing=20, size_hint_y=None)
        btn_container.bind(minimum_height=btn_container.setter('height'))
        
        opciones = [
            ("AGREGAR TAREA", 'agregar'),
            ("MOSTRAR TAREAS", 'lista'),
            ("GESTIONAR TRABAJADORES", 'trabajadores'),
            ("CERRAR SESIÓN", 'logout')
        ]
        
        for texto, screen_name in opciones:
            btn = TactileButton(text=texto)
            if screen_name == 'logout':
                btn.bind(on_press=self.cerrar_sesion)
            else:
                btn.bind(on_press=lambda x, sn=screen_name: self.cambiar_pantalla(sn))
            btn_container.add_widget(btn)
        
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(btn_container)
        self.layout.add_widget(scroll)
        self.add_widget(self.layout)
    
    def on_enter(self):
        if not self.manager.usuario_actual:
            self.manager.current = 'login'
        else:
            if hasattr(self.manager, 'es_admin'):
                if self.manager.es_admin:
                    self.title_label.text = 'Gestor de Tareas (Admin)'
                else:
                    self.title_label.text = 'Gestor de Tareas'
    
    def cambiar_pantalla(self, screen_name):
        self.manager.current = screen_name
    
    def cerrar_sesion(self, instance):
        self.manager.usuario_actual = None
        self.manager.current = 'login'



class AgregarTareaScreen(ThemedScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = None
        
        # Layout principal con ScrollView
        self.scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        self.main_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=dp(20),
            size_hint_y=None
        )
        self.main_layout.bind(minimum_height=self.main_layout.setter('height'))
        
        # Configuración del campo de título
        self.titulo = TextInput(
            hint_text='Título de la tarea',
            size_hint_y=None,
            height=dp(70),
            font_size='24sp',
            multiline=False,
            background_normal='',
            background_color=(1, 1, 1, 0.8),
            foreground_color=(0, 0, 0, 1),
            padding=[dp(20), dp(20)],
            write_tab=False
        )
        
        # Campo de descripción
        self.descripcion = TextInput(
            hint_text='Descripción (opcional)',
            size_hint_y=None,
            height=dp(150),
            font_size='20sp',
            background_normal='',
            background_color=(1, 1, 1, 0.8),
            foreground_color=(0, 0, 0, 1),
            padding=[dp(20), dp(20)],
            multiline=True
        )
        
        # Spinner de trabajadores
        self.spinner = Spinner(
            text='Seleccionar trabajador',
            values=['Ninguno'] + [t[1] for t in obtener_trabajadores()],
            size_hint_y=None,
            height=dp(60),
            font_size='20sp',
            background_normal='',
            background_color=ThemeManager.get_theme_colors()["primary"],
            option_cls=SpinnerOption
        )
        
        # Botones
        btn_guardar = Button(
            text='GUARDAR TAREA',
            size_hint_y=None,
            height=dp(70),
            background_normal='',
            background_color=(0.2, 0.7, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size='20sp',
            bold=True
        )
        btn_guardar.bind(on_press=self.guardar_tarea)
        
        btn_volver = Button(
            text='CANCELAR',
            size_hint_y=None,
            height=dp(70),
            background_normal='',
            background_color=(0.8, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            font_size='20sp',
            bold=True
        )
        btn_volver.bind(on_press=self.volver)
        
        # Construcción de la interfaz
        self.main_layout.add_widget(Label(
            text='NUEVA TAREA',
            size_hint_y=None,
            height=dp(60),
            font_size='28sp',
            bold=True
        ))
        self.main_layout.add_widget(self.titulo)
        self.main_layout.add_widget(self.descripcion)
        self.main_layout.add_widget(self.spinner)
        self.main_layout.add_widget(btn_guardar)
        self.main_layout.add_widget(btn_volver)
        
        self.scroll.add_widget(self.main_layout)
        self.add_widget(self.scroll)
        
        # Configurar eventos
        self.titulo.bind(on_focus=self._on_titulo_focus)
        self.descripcion.bind(on_focus=self._on_descripcion_focus)
    
    def _on_titulo_focus(self, instance, value):
        if value:
            self._setup_keyboard()
    
    def _on_descripcion_focus(self, instance, value):
        if value:
            self._setup_keyboard()
    
    def _setup_keyboard(self):
        if not self._keyboard:
            self._keyboard = Window.request_keyboard(
                self._keyboard_closed, self)
            self._keyboard.bind(on_key_down=self._on_keyboard_down)
    
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'enter':
            if self.titulo.focus:
                self.descripcion.focus = True
                return True
            elif self.descripcion.focus:
                self.guardar_tarea(None)
                return True
        return False
    
    def _keyboard_closed(self):
        if self._keyboard:
            self._keyboard.unbind(on_key_down=self._on_keyboard_down)
            self._keyboard.release()
            self._keyboard = None
    
    def on_pre_enter(self):
        self.actualizar_spinner()

    def on_enter(self):
    # Programar el foco para después de que la pantalla esté completamente cargada
        Clock.schedule_once(self._set_focus, 0.1)
        # Programar el foco para después de que la pantalla esté completamente cargada
        
    
    def _set_focus(self, dt):
        self.titulo.focus = True
        self._setup_keyboard()
    
    def on_leave(self):
        # Liberar el teclado al salir de la pantalla
        self._keyboard_closed()

    def actualizar_spinner(self):
        trabajadores = obtener_trabajadores()
        self.spinner.values = ['Ninguno'] + [t[1] for t in trabajadores]
    
    def guardar_tarea(self, instance):
        titulo = self.titulo.text.strip()
        if not titulo:
            self.mostrar_mensaje('⚠️ El título es requerido')
            self.titulo.focus = True
            return
        
        trabajador_id = None
        if self.spinner.text != 'Ninguno':
            for t in obtener_trabajadores():
                if t[1] == self.spinner.text:
                    trabajador_id = t[0]
                    break
        
        if agregar_tarea(
            titulo=titulo,
            descripcion=self.descripcion.text,
            trabajador_id=trabajador_id,
            usuario_id=self.manager.usuario_actual
        ):
            self.mostrar_mensaje('✅ Tarea guardada')
            self.limpiar_campos()
            pantalla_lista = self.manager.get_screen('lista')
            if hasattr(pantalla_lista, 'actualizar_lista'):
                pantalla_lista.actualizar_lista()
        else:
            self.mostrar_mensaje('❌ Error al guardar')
    
    def limpiar_campos(self):
        self.titulo.text = ''
        self.descripcion.text = ''
        self.spinner.text = 'Seleccionar trabajador'
    
    def volver(self, instance):
        self.manager.current = 'menu'
    
    def mostrar_mensaje(self, mensaje):
        popup = Popup(
            title='Mensaje',
            size_hint=(0.8, 0.4),
            separator_height=dp(2),
            background='atlas://data/images/defaulttheme/button_pressed'
        )
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
        content.add_widget(Label(
            text=mensaje,
            font_size='20sp'
        ))
        btn_ok = Button(
            text='OK',
            size_hint_y=None,
            height=dp(60),
            background_normal='',
            background_color=(0.2, 0.5, 0.8, 1)
        )
        btn_ok.bind(on_press=popup.dismiss)
        content.add_widget(btn_ok)
        popup.content = content
        popup.open()


class ListaTareasScreen(ThemedScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)
    
    def on_enter(self):
        if not self.manager.usuario_actual:
            self.manager.current = 'login'
        else:
            self.actualizar_lista()
    
    def actualizar_lista(self):
        self.layout.clear_widgets()
        usuario_id = self.manager.usuario_actual
        es_admin = getattr(self.manager, 'es_admin', False)

        tareas = mostrar_tareas(usuario_id, es_admin)
        
        scroll = ScrollView()
        listado = GridLayout(cols=1, spacing=20, size_hint_y=None, padding=[20, 20])
        listado.bind(minimum_height=listado.setter('height'))
        
        theme_colors = ThemeManager.get_theme_colors()
        bg_color = (0.95, 0.95, 0.95, 1) if ThemeManager.current_theme == "light" else (0.2, 0.2, 0.2, 1)
        border_color = (0.8, 0.8, 0.8, 1) if ThemeManager.current_theme == "light" else (0.4, 0.4, 0.4, 1)
        
        for tarea in tareas:
            card_height = 320 if es_admin else 320

            card = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=card_height,  # Ejemplo: 280 si es_admin, 240 si no
                padding=[15, 20, 15, 15],  # Más espacio arriba (20)
                spacing=8  # Reducir espacio entre elementos
            )
            
            with card.canvas.before:
                Color(*bg_color)
                card.bg_rect = RoundedRectangle(
                    size=card.size,
                    pos=card.pos,
                    radius=[15]
                )
                Color(*border_color)
                card.border_rect = RoundedRectangle(
                    size=card.size,
                    pos=card.pos,
                    radius=[15]
                )
                Line(
                    rounded_rectangle=(card.pos[0], card.pos[1], card.size[0], card.size[1], 15),
                    width=1.5
                )
            
            card.bind(pos=self.update_card_rect, size=self.update_card_rect)
            
            title_box = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=70,
                padding=[20, 10, 20, 10],  # Añadir padding horizontal
                spacing=10
            )
            with title_box.canvas.before:
                Color(*theme_colors["primary"])
                title_box.rect = Rectangle(
                    size=title_box.size,
                    pos=title_box.pos
                )
            
            lbl_titulo = Label(
                text=f"[b]{tarea[1]}[/b]",
                markup=True,
                halign='left',
                valign='middle',
                color=theme_colors["btn_text"],
                bold=True,
                size_hint_x=0.9,
                text_size=(Window.width * 0.7, None),
                shorten=True,
                shorten_from='right',
                font_size='16sp',
                padding=(10,5)
            )
            title_box.add_widget(lbl_titulo)
            card.add_widget(title_box)

            fecha_str = tarea[3]
            try:
                fecha_local = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
                fecha_texto = f"[size=14]Creada: {fecha_local.strftime('%d/%m/%Y %H:%M')}[/size]"
            except Exception as e:
                fecha_texto = f"[size=14]Creada: {fecha_str}[/size]"
            
            lbl_fecha = Label(
                text=fecha_texto,
                markup=True,
                size_hint_y=None,
                height=30,
                halign='left',
                color=(0, 0, 0, 1),
                font_size='14sp'
            )
            card.add_widget(lbl_fecha)
            
            trabajador_text = "Sin asignar"
            if tarea[5]:
                trabajadores = obtener_trabajadores()
                for t in trabajadores:
                    if t[0] == tarea[5]:
                        trabajador_text = f"Asignado a: {t[1]}"
                        break
            
            lbl_trabajador = Label(
                text=trabajador_text,
                size_hint_y=None,
                height=30,
                halign='left',
                color=theme_colors["text"],
                font_size='14sp'
            )
            card.add_widget(lbl_trabajador)
            
            lbl_desc = Label(
                text=tarea[2] if tarea[2] else "[i](Sin descripción)[/i]",
                markup=True,
                size_hint_y=None,
                height=80,
                halign='left',
                valign='top',
                color=theme_colors["text"],
                text_size=(Window.width - 50, None),
                font_size='16sp'
            )
            card.add_widget(lbl_desc)
            
            footer = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=50,
                spacing=15
            )
            
            estado = "COMPLETADA" if tarea[4] else "PENDIENTE"
            estado_color = (0, 0.7, 0, 1) if tarea[4] else (0.8, 0.2, 0, 1)
            lbl_estado = Label(
                text=f"[b]Estado:[/b] {estado}",
                markup=True,
                color=estado_color,
                halign='left',
                size_hint_x=0.6,
                font_size='16sp'
            )
            
            btn_acciones = TactileButton(
                text="Ver detalles",
                size_hint_x=0.4,
                font_size='16sp'
            )
            btn_acciones.bind(
                on_press=lambda instance, tid=tarea[0]: self.mostrar_detalle(tid)
            )
            
            footer.add_widget(lbl_estado)
            footer.add_widget(btn_acciones)
            card.add_widget(footer)
            
            if es_admin and len(tarea) > 6:
                lbl_usuario = Label(
                    text=f"Usuario: {tarea[6]}",
                    size_hint_y=None,
                    height=30,
                    halign='left',
                    color=theme_colors["text"],
                    font_size='14sp'
                )
                card.add_widget(lbl_usuario)
            
            listado.add_widget(card)

        scroll.add_widget(listado)
        self.layout.add_widget(scroll)
        
        btn_volver = TactileButton(
            text='VOLVER AL MENÚ',
            background_color=ThemeManager.get_theme_colors()["secondary"]
        )
        btn_volver.bind(on_press=lambda x: setattr(self.manager, 'current', 'menu'))
        self.layout.add_widget(btn_volver)

    def update_card_rect(self, instance, value):
        instance.bg_rect.pos = instance.pos
        instance.bg_rect.size = instance.size
        instance.border_rect.pos = instance.pos
        instance.border_rect.size = instance.size
    
    def mostrar_detalle(self, tarea_id):
        usuario_id = self.manager.usuario_actual
        es_admin = getattr(self.manager, 'es_admin', False)
        
        tarea = obtener_tarea_por_id(tarea_id, usuario_id, es_admin)
        if not tarea:
            self.mostrar_mensaje("No se encontró la tarea o no tienes permisos")
            return
                
        colors = ThemeManager.get_theme_colors()
        
        popup = Popup(
            title=f"Detalles de la tarea: {tarea[1]}",
            size_hint=(0.9, 0.8),
            background='atlas://data/images/defaulttheme/button_pressed',
            title_size='20sp',
            title_align='center'
        )
        
        scroll_content = ScrollView(size_hint=(1, 1))
        main_content = BoxLayout(
            orientation='vertical', 
            spacing=15, 
            padding=25,
            size_hint_y=None
        )
        main_content.bind(minimum_height=main_content.setter('height'))
        
        main_content.add_widget(Label(size_hint_y=None, height=10))
        
        estado = "COMPLETADA" if tarea[4] else "PENDIENTE"
        color_estado = (0, 0.6, 0, 1) if tarea[4] else (0.8, 0, 0, 1)
        lbl_estado = Label(
            text=f"[b]Estado:[/b] {estado}",
            markup=True,
            size_hint_y=None,
            height=40,
            halign='left',
            color=color_estado,
            font_size='18sp'
        )
        main_content.add_widget(lbl_estado)
        
        fecha_str = tarea[3]
        try:
            fecha_local = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
            fecha_texto = f"[b]Creada:[/b] {fecha_local.strftime('%d/%m/%Y %H:%M')}"
        except Exception as e:
            fecha_texto = f"[b]Creada:[/b] {fecha_str}"
        
        lbl_fecha = Label(
            text=fecha_texto,
            markup=True,
            size_hint_y=None,
            height=40,
            halign='left',
            color=colors["text"],
            font_size='18sp'
        )
        main_content.add_widget(lbl_fecha)
        
        if tarea[5]:
            trabajadores = obtener_trabajadores()
            trabajador_nombre = "Sin asignar"
            for t in trabajadores:
                if t[0] == tarea[5]:
                    trabajador_nombre = t[1]
                    break
            
            lbl_trabajador = Label(
                text=f"[b]Trabajador:[/b] {trabajador_nombre}",
                markup=True,
                size_hint_y=None,
                height=40,
                halign='left',
                color=colors["text"],
                font_size='18sp'
            )
            main_content.add_widget(lbl_trabajador)
        
        if es_admin and len(tarea) > 7:
            lbl_usuario = Label(
                text=f"[b]Usuario:[/b] {tarea[7]}",
                markup=True,
                size_hint_y=None,
                height=40,
                halign='left',
                color=colors["text"],
                font_size='18sp'
            )
            main_content.add_widget(lbl_usuario)
        
        descripcion = tarea[2] if tarea[2] else "[i](Sin descripción)[/i]"
        lbl_desc = Label(
            text=f"[b]Descripción:[/b]\n{descripcion}",
            markup=True,
            size_hint_y=None,
            height=150,
            halign='left',
            valign='top',
            color=colors["text"],
            font_size='18sp',
            text_size=(Window.width * 0.85, None)
        )
        main_content.add_widget(lbl_desc)
        
        main_content.add_widget(Label(size_hint_y=None, height=20))
        
        es_dueño = (not es_admin) and (tarea[6] == usuario_id if len(tarea) > 6 else False)
        mostrar_botones = es_admin or es_dueño
        
        if mostrar_botones:
            btn_container = GridLayout(
                cols=2,
                spacing=dp(25),
                size_hint_y=None,
                height=dp(250) if es_admin else dp(200)
            )
            
            btn_completar = TactileButton(
                text='MARCAR',
                background_color=(0.2, 0.7, 0.2, 1),  # Verde más vibrante
                size_hint_x=0.48 if es_admin else 1,
                size_hint_y=None,
                height=dp(70)
        )
            
            btn_editar = TactileButton(
                text='EDITAR',
                background_color=(0.2, 0.5, 0.8, 1),
                size_hint_x=0.48 if es_admin else 1,
                size_hint_y=None,
                height=dp(70) # Altura definida
            )
            
            btn_eliminar = TactileButton(
                text='ELIMINAR',
                background_color=(0.8, 0.2, 0.2, 1),
                size_hint_x=0.48,
                size_hint_y=None,
                height=dp(70)
            )
            
            btn_container.add_widget(btn_completar)
            btn_container.add_widget(btn_editar)
            btn_container.add_widget(btn_eliminar)
            
            main_content.add_widget(btn_container)
            
            btn_completar.bind(on_press=lambda x: self.cambiar_estado(tarea_id, popup, usuario_id, es_admin))
            btn_editar.bind(on_press=lambda x: self.editar_tarea(tarea_id, popup, usuario_id, es_admin))
            btn_eliminar.bind(on_press=lambda x: self.eliminar_tarea(tarea_id, popup, usuario_id, es_admin))
        
        btn_cerrar = TactileButton(
            text='CERRAR',
            size_hint_x=0.48,
            size_hint_y=None,
            height=dp(70)
    )
        btn_cerrar.bind(on_press=popup.dismiss)
        main_content.add_widget(btn_cerrar)
        
        scroll_content.add_widget(main_content)
        popup.content = scroll_content
        popup.open()

    def cambiar_estado(self, tarea_id, popup, usuario_id=None, es_admin=False):
        if marcar_completada(tarea_id, usuario_id, es_admin):
            self.actualizar_lista()
            popup.dismiss()
        else:
            self.mostrar_mensaje("❌ No tienes permisos para esta acción")

    def eliminar_tarea(self, tarea_id, popup, usuario_id=None, es_admin=False):
        if eliminar_tarea(tarea_id, usuario_id, es_admin):
            self.actualizar_lista()
            popup.dismiss()
        else:
            self.mostrar_mensaje("❌ No tienes permisos para eliminar esta tarea")

    def editar_tarea(self, tarea_id, popup, usuario_id=None, es_admin=False):
        popup.dismiss()
        pantalla_editar = self.manager.get_screen('editar')
        pantalla_editar.cargar_tarea(tarea_id)
        self.manager.current = 'editar'

    def mostrar_mensaje(self, mensaje):
        colors = ThemeManager.get_theme_colors()
        popup = Popup(
            title='Mensaje',
            size_hint=(0.8, 0.4),
            background='atlas://data/images/defaulttheme/button_pressed'
        )
        content = BoxLayout(orientation='vertical', spacing=15, padding=20)
        content.add_widget(Label(
            text=mensaje, 
            color=colors["text"],
            font_size='18sp'
        ))
        btn_ok = TactileButton(text='OK')
        btn_ok.bind(on_press=popup.dismiss)
        content.add_widget(btn_ok)
        popup.content = content
        popup.open()

class EditarTareaScreen(ThemedScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=25, padding=[40, 60, 40, 60])
        
        self.titulo = TextInput(
            hint_text='Título',
            size_hint_y=None,
            height=60,
            font_size='18sp',
            background_normal='',
            background_color=(1, 1, 1, 0.7),
            padding=[15, (60 - 18*1.5)/2],
            multiline=False
        )
        
        self.descripcion = TextInput(
            hint_text='Descripción',
            size_hint_y=None,
            height=150,
            font_size='18sp',
            background_normal='',
            background_color=(1, 1, 1, 0.7),
            padding=[15, 10]
        )
        
        btn_guardar = TactileButton(text='GUARDAR CAMBIOS')
        btn_guardar.bind(on_press=self.guardar_cambios)
        
        btn_cancelar = TactileButton(
            text='CANCELAR',
            background_color=ThemeManager.get_theme_colors()["secondary"]
        )
        btn_cancelar.bind(on_press=self.volver)
        
        self.layout.add_widget(Label(
            text='EDITAR TAREA', 
            font_size='24sp',
            size_hint_y=None,
            height=80
        ))
        self.layout.add_widget(self.titulo)
        self.layout.add_widget(self.descripcion)
        self.layout.add_widget(btn_guardar)
        self.layout.add_widget(btn_cancelar)
        self.add_widget(self.layout)
    
    def on_enter(self):
        if not self.manager.usuario_actual:
            self.manager.current = 'login'
    
    def cargar_tarea(self, tarea_id):
        usuario_id = self.manager.usuario_actual
        es_admin = getattr(self.manager, 'es_admin', False)
        
        tarea = obtener_tarea_por_id(tarea_id, usuario_id, es_admin)
        if tarea:
            self.tarea_id = tarea_id
            self.titulo.text = tarea[1]
            self.descripcion.text = tarea[2] if tarea[2] else ''
        else:
            self.mostrar_mensaje("❌ No tienes permisos para editar esta tarea")
            self.manager.current = 'lista'
    
    def guardar_cambios(self, instance):
        if hasattr(self, 'tarea_id'):
            if self.titulo.text.strip():
                usuario_id = self.manager.usuario_actual
                es_admin = getattr(self.manager, 'es_admin', False)
                
                if actualizar_tarea(
                    self.tarea_id,
                    self.titulo.text,
                    self.descripcion.text,
                    usuario_id,
                    es_admin
                ):
                    self.manager.get_screen('lista').actualizar_lista()
                    self.manager.current = 'lista'
                else:
                    self.mostrar_mensaje("❌ No tienes permisos para editar esta tarea")
            else:
                self.mostrar_mensaje("⚠️ Ingresa un título")
    
    def volver(self, instance):
        self.manager.current = 'lista'
    
    def mostrar_mensaje(self, mensaje):
        colors = ThemeManager.get_theme_colors()
        popup = Popup(
            title='Mensaje',
            size_hint=(0.8, 0.4),
            background='atlas://data/images/defaulttheme/button_pressed'
        )
        content = BoxLayout(orientation='vertical', spacing=15, padding=20)
        content.add_widget(Label(
            text=mensaje, 
            color=colors["text"],
            font_size='18sp'
        ))
        btn_ok = TactileButton(text='OK')
        btn_ok.bind(on_press=popup.dismiss)
        content.add_widget(btn_ok)
        popup.content = content
        popup.open()

class GestionTrabajadoresScreen(ThemedScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Layout principal optimizado
        main_layout = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))
        
        # Campos de entrada
        input_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(250),
            spacing=dp(15)
        )
        
        self.nombre = TextInput(
            hint_text='Nombre del trabajador',
            size_hint_y=None,
            height=dp(60),
            font_size=dp(20),
            multiline=False,
            write_tab=False,
            background_normal='',
            background_color=(1, 1, 1, 0.8)
        )
        
        self.cargo = TextInput(
            hint_text='Cargo (opcional)',
            size_hint_y=None,
            height=dp(60),
            font_size=dp(20),
            multiline=False,
            write_tab=False,
            background_normal='',
            background_color=(1, 1, 1, 0.8)
        )
        
        btn_agregar = Button(
            text='AGREGAR TRABAJADOR',
            size_hint_y=None,
            height=dp(60),
            background_normal='',
            background_color=(0.2, 0.6, 0.2, 1),
            color=(1, 1, 1, 1),
            bold=True
        )
        btn_agregar.bind(on_press=self.agregar_trabajador)
        
        input_layout.add_widget(self.nombre)
        input_layout.add_widget(self.cargo)
        input_layout.add_widget(btn_agregar)
        
        # Listado de trabajadores con ScrollView
        self.list_scroll = ScrollView(size_hint=(1, 1))
        self.listado = GridLayout(
            cols=1,
            spacing=dp(10),
            size_hint_y=None,
            padding=[dp(5), 0, dp(5), dp(10)]
        )
        self.listado.bind(minimum_height=self.listado.setter('height'))
        
        self.list_scroll.add_widget(self.listado)
        
        # Botón de volver
        btn_volver = Button(
            text='VOLVER AL MENÚ',
            size_hint_y=None,
            height=dp(60),
            background_normal='',
            background_color=(0.8, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            bold=True
        )
        btn_volver.bind(on_press=self.volver)
        
        # Construir la interfaz
        main_layout.add_widget(Label(
            text='GESTIÓN DE TRABAJADORES',
            size_hint_y=None,
            height=dp(50),
            font_size=dp(24),
            bold=True
        ))
        main_layout.add_widget(input_layout)
        main_layout.add_widget(self.list_scroll)
        main_layout.add_widget(btn_volver)
        
        self.add_widget(main_layout)
        self.actualizar_listado()
    
    def actualizar_listado(self):
        self.listado.clear_widgets()
        trabajadores = obtener_trabajadores()
        
        for trabajador in trabajadores:
            # Tarjeta para cada trabajador
            card = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(70),
                spacing=dp(10),
                padding=[dp(15), dp(5)]
            )
            
            with card.canvas.before:
                Color(rgba=(0.95, 0.95, 0.95, 1) if ThemeManager.current_theme == "light" else (0.2, 0.2, 0.2, 1))
                card.rect = RoundedRectangle(
                    size=card.size,
                    pos=card.pos,
                    radius=[dp(8)]
                )
            
            lbl_info = Label(
                text=f"{trabajador[1]} - {trabajador[2] or 'Sin cargo'}",
                halign='left',
                valign='middle',
                size_hint_x=0.8,
                text_size=(Window.width * 0.7, None),
                font_size=dp(16)
            )
            
            btn_eliminar = Button(
                text='×',
                size_hint=(None, None),
                size=(dp(50), dp(50)),
                background_normal='',
                background_color=(0.9, 0.2, 0.2, 1),
                color=(1, 1, 1, 1),
                font_size=dp(24),
                bold=True
            )
            btn_eliminar.bind(
                on_press=lambda instance, tid=trabajador[0]: self.eliminar_trabajador(tid)
            )
            
            card.add_widget(lbl_info)
            card.add_widget(btn_eliminar)
            self.listado.add_widget(card)
    
    # Resto de métodos permanecen igual...
    def agregar_trabajador(self, instance):
        nombre = self.nombre.text.strip()
        cargo = self.cargo.text.strip()
        
        if not nombre:
            self.mostrar_mensaje('⚠️ Ingresa un nombre para el trabajador')
            self.nombre.focus = True
            return
        
        if agregar_trabajador(nombre, cargo):
            self.nombre.text = ''
            self.cargo.text = ''
            self.actualizar_listado()
            self.mostrar_mensaje('✅ Trabajador agregado')
            # Actualizar spinners en otras pantallas
            pantalla_agregar = self.manager.get_screen('agregar')
            if hasattr(pantalla_agregar, 'actualizar_spinner'):
                pantalla_agregar.actualizar_spinner()
            # Volver a enfocar el campo de nombre
            self.nombre.focus = True
        else:
            self.mostrar_mensaje('❌ Error al agregar trabajador')
    
    def eliminar_trabajador(self, trabajador_id):
        if eliminar_trabajador(trabajador_id):
            self.actualizar_listado()
            self.mostrar_mensaje('✅ Trabajador eliminado')
        else:
            self.mostrar_mensaje('❌ Error al eliminar')
    
    def volver(self, instance):
        pantalla_agregar = self.manager.get_screen('agregar')
        if hasattr(pantalla_agregar, 'actualizar_spinner'):
            pantalla_agregar.actualizar_spinner()
        self.manager.current = 'menu'
    
    def mostrar_mensaje(self, mensaje):
        colors = ThemeManager.get_theme_colors()
        popup = Popup(
            title='Mensaje',
            size_hint=(0.8, 0.4),
            background='atlas://data/images/defaulttheme/button_pressed'
        )
        content = BoxLayout(orientation='vertical', spacing=15, padding=20)
        content.add_widget(Label(
            text=mensaje, 
            color=colors["text"],
            font_size='18sp'
        ))
        btn_ok = TactileButton(text='OK')
        btn_ok.bind(on_press=popup.dismiss)
        content.add_widget(btn_ok)
        popup.content = content
        popup.open()

class GestorTareasApp(App):
    def build(self):
        crear_tabla()
        migrar_tabla_tareas()
        root = RootWidget()
        
        screens = [
            LoginScreen(name='login'),
            RegistroScreen(name='registro'),
            MenuPrincipal(name='menu'),
            AgregarTareaScreen(name='agregar'),
            ListaTareasScreen(name='lista'),
            EditarTareaScreen(name='editar'),
            GestionTrabajadoresScreen(name='trabajadores')
        ]
        
        for screen in screens:
            root.sm.add_widget(screen)
        
        root.sm.current = 'login'
        return root

if __name__ == '__main__':

    from kivy.core.window import Window
    from kivy.metrics import dp
    Window.softinput_mode = 'pan'  # o 'below_target' según lo que funcione mejor
    Window.size = (dp(360), dp(640))
    GestorTareasApp().run()


    