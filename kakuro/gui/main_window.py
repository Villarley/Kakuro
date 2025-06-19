"""
Ventana principal del juego Kakuro
Maneja la interfaz principal y el menú del juego
"""

import tkinter as tk
from tkinter import ttk


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Kakuro 2025")
        self.root.geometry("800x600")
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de usuario principal"""
        # TODO: Implementar interfaz principal
        pass
    
    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()


if __name__ == "__main__":
    app = MainWindow()
    app.run() 