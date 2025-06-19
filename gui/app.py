import tkinter as tk
from gui.home_screen import HomeScreen
from gui.game_screen import GameScreen
from gui.config_screen import ConfigScreen


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kakuro 2025")
        self.geometry("800x600")  # Tamaño por defecto
        
        # Permitir redimensionamiento de la ventana
        self.resizable(True, True)  # Ahora la ventana se puede redimensionar
        self.minsize(800, 600)      # Tamaño mínimo permitido

        # Abrir en modo fullscreen al iniciar
        self.attributes("-fullscreen", True)

        # Permitir salir de fullscreen con la tecla Escape
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))

        # Diccionario de pantallas
        self.frames = {}

        for Screen in (HomeScreen, GameScreen, ConfigScreen):
            screen_name = Screen.__name__
            frame = Screen(parent=self, controller=self)
            self.frames[screen_name] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame("HomeScreen")

    def show_frame(self, screen_name):
        """Trae al frente el frame solicitado"""
        frame = self.frames[screen_name]
        frame.tkraise()
