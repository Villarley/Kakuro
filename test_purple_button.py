#!/usr/bin/env python3
"""
Script de prueba para el componente PurpleButton
"""

import tkinter as tk
import sys
import os

# Añadir el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.components import PurpleButton


def test_purple_button():
    """Prueba el componente PurpleButton"""
    root = tk.Tk()
    root.title("Prueba PurpleButton")
    root.geometry("400x300")
    root.configure(bg="#1e1e1e")
    
    # Título
    title = tk.Label(
        root,
        text="🧪 Prueba de PurpleButton",
        font=("Arial", 18, "bold"),
        bg="#1e1e1e",
        fg="white"
    )
    title.pack(pady=20)
    
    # Botones de prueba
    buttons = [
        ("🎮 Botón Grande", lambda: print("Botón grande clickeado")),
        ("⚙️ Botón Mediano", lambda: print("Botón mediano clickeado"), {"width": 15, "height": 1}),
        ("📘 Botón Pequeño", lambda: print("Botón pequeño clickeado"), {"width": 10, "height": 1, "font": ("Arial", 12)}),
    ]
    
    for i, button_info in enumerate(buttons):
        if len(button_info) == 2:
            text, command = button_info
            kwargs = {}
        else:
            text, command, kwargs = button_info
        
        btn = PurpleButton(root, text=text, command=command, **kwargs)
        btn.pack(pady=10)
    
    # Botón de salir
    exit_btn = PurpleButton(
        root,
        text="🚪 Salir",
        command=root.quit,
        width=10,
        height=1
    )
    exit_btn.pack(pady=20)
    
    root.mainloop()


if __name__ == "__main__":
    test_purple_button() 