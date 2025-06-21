"""
Componentes de celdas para el tablero de Kakuro
Funciones modulares para crear diferentes tipos de celdas del juego
"""

import tkinter as tk


def create_white_cell(parent, row, col, command=None):
    """
    Crea una celda blanca editable para el tablero de Kakuro.
    
    Args:
        parent: Widget padre donde se creará la celda
        row: Fila de la celda
        col: Columna de la celda
        command (function, optional): Función a ejecutar al hacer clic en la celda
        
    Returns:
        tk.Button: Celda blanca con borde, lista para ser editable
        
    Características:
        - Fondo blanco
        - Tamaño estándar 45x45px
        - Borde visible
        - Preparada para ser editable posteriormente
    """
    btn = tk.Button(
        parent,
        width=5,
        height=2,
        font=("Segoe UI", 12, "bold"),
        bg="white",
        fg="black",
        relief="solid",
        bd=1,
        command=command if command else lambda: None
    )
    btn.grid(row=row, column=col, padx=1, pady=1)
    return btn


def create_black_cell(parent, row, col):
    """
    Crea una celda negra bloqueada para el tablero de Kakuro.
    
    Args:
        parent: Widget padre donde se creará la celda
        row: Fila de la celda
        col: Columna de la celda
        
    Returns:
        tk.Label: Celda negra completamente bloqueada
        
    Características:
        - Fondo completamente negro
        - Sin contenido ni claves
        - Representa una celda bloqueada/imposible
        - Tamaño estándar 45x45px
    """
    lbl = tk.Label(
        parent,
        width=5,
        height=2,
        font=("Segoe UI", 12, "bold"),
        bg="black",
        fg="white",
        relief="flat"
    )
    lbl.grid(row=row, column=col, padx=1, pady=1)
    return lbl


def create_key_cell(parent, row, col, text):
    """
    Crea una celda con claves (números objetivo) para filas y columnas.
    
    Args:
        parent: Widget padre donde se creará la celda
        row: Fila de la celda
        col: Columna de la celda
        text: Texto a mostrar en la celda
        
    Returns:
        tk.Label: Celda con claves numéricas
        
    Características:
        - Fondo gris claro
        - Texto en negrita
        - Borde visible
        - Tamaño estándar 45x45px
    """
    lbl = tk.Label(
        parent,
        width=5,
        height=2,
        font=("Segoe UI", 12, "bold"),
        bg="#bdbdbd",
        fg="black",
        text=text,
        relief="ridge",
        bd=1
    )
    lbl.grid(row=row, column=col, padx=1, pady=1)
    return lbl 