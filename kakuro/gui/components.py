"""
Componentes reutilizables de la interfaz de usuario
Botones, panel de números, reloj, etc.
"""

import tkinter as tk
from tkinter import ttk


class NumberPanel:
    """Panel de números para seleccionar valores"""
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Configura el panel de números"""
        # TODO: Implementar panel de números 1-9
        pass


class Timer:
    """Componente de reloj/cronómetro"""
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.time_label = tk.Label(self.frame, text="00:00")
        self.setup_ui()
    
    def setup_ui(self):
        """Configura el reloj"""
        self.time_label.pack()
    
    def update_time(self, seconds):
        """Actualiza el tiempo mostrado"""
        minutes = seconds // 60
        secs = seconds % 60
        self.time_label.config(text=f"{minutes:02d}:{secs:02d}")


class CustomButton:
    """Botón personalizado para el juego"""
    def __init__(self, parent, text, command=None):
        self.button = tk.Button(parent, text=text, command=command)
    
    def pack(self, **kwargs):
        return self.button.pack(**kwargs) 