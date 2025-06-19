"""
Pantalla del juego Kakuro
Maneja la interfaz del tablero de juego
"""

import tkinter as tk
from tkinter import ttk


class GameScreen:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz del juego"""
        # TODO: Implementar tablero de juego
        pass
    
    def show(self):
        """Muestra la pantalla del juego"""
        self.frame.pack(fill=tk.BOTH, expand=True)
    
    def hide(self):
        """Oculta la pantalla del juego"""
        self.frame.pack_forget() 