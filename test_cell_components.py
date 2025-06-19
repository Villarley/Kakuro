#!/usr/bin/env python3
"""
Script de prueba para los componentes de celdas del tablero Kakuro
"""

import tkinter as tk
import sys
import os

# Añadir el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.components.cell_components import create_white_cell, create_black_cell, create_key_cell


def test_cell_components():
    """Prueba todos los componentes de celdas"""
    root = tk.Tk()
    root.title("Prueba Componentes de Celdas - Kakuro")
    root.geometry("600x400")
    root.configure(bg="#1e1e1e")
    
    # Título
    title = tk.Label(
        root,
        text="🧪 Prueba de Componentes de Celdas",
        font=("Arial", 18, "bold"),
        bg="#1e1e1e",
        fg="white"
    )
    title.pack(pady=20)
    
    # Frame para las celdas de prueba
    test_frame = tk.Frame(root, bg="#1e1e1e")
    test_frame.pack(pady=20)
    
    # Crear diferentes tipos de celdas para demostración
    cells = [
        ("Celda Blanca", create_white_cell(test_frame)),
        ("Celda Negra", create_black_cell(test_frame)),
        ("Clave Fila (15)", create_key_cell(test_frame, clave_fila=15)),
        ("Clave Columna (12)", create_key_cell(test_frame, clave_columna=12)),
        ("Clave Ambos (8, 9)", create_key_cell(test_frame, clave_fila=8, clave_columna=9)),
    ]
    
    # Mostrar las celdas en una fila
    for i, (label, cell) in enumerate(cells):
        # Label descriptivo
        desc_label = tk.Label(
            test_frame,
            text=label,
            font=("Arial", 10),
            bg="#1e1e1e",
            fg="white"
        )
        desc_label.grid(row=0, column=i, pady=(0, 10))
        
        # Celda
        cell.grid(row=1, column=i, padx=10)
    
    # Botón de salir
    exit_btn = tk.Button(
        root,
        text="🚪 Salir",
        command=root.quit,
        font=("Arial", 12),
        bg="#3a3a3a",
        fg="white",
        bd=0
    )
    exit_btn.pack(pady=20)
    
    root.mainloop()


if __name__ == "__main__":
    test_cell_components() 