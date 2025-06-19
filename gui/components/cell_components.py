"""
Componentes de celdas para el tablero de Kakuro
Funciones modulares para crear diferentes tipos de celdas del juego
"""

import tkinter as tk


def create_white_cell(parent):
    """
    Crea una celda blanca editable para el tablero de Kakuro.
    
    Args:
        parent: Widget padre donde se creará la celda
        
    Returns:
        tk.Label: Celda blanca con borde, lista para ser editable
        
    Características:
        - Fondo blanco
        - Tamaño estándar 45x45px
        - Borde visible
        - Preparada para ser editable posteriormente
    """
    cell = tk.Label(
        parent,
        text="",
        width=6,  # Aproximadamente 45px
        height=3,  # Aproximadamente 45px
        bg="white",
        fg="black",
        relief="solid",
        borderwidth=1,
        font=("Arial", 12, "bold"),
        anchor="center"
    )
    return cell


def create_black_cell(parent):
    """
    Crea una celda negra bloqueada para el tablero de Kakuro.
    
    Args:
        parent: Widget padre donde se creará la celda
        
    Returns:
        tk.Canvas: Celda negra completamente bloqueada
        
    Características:
        - Fondo completamente negro
        - Sin contenido ni claves
        - Representa una celda bloqueada/imposible
        - Tamaño estándar 45x45px
    """
    cell = tk.Canvas(
        parent,
        width=45,
        height=45,
        bg="black",
        highlightthickness=0,
        relief="flat"
    )
    return cell


def create_key_cell(parent, clave_fila=None, clave_columna=None):
    """
    Crea una celda con claves (números objetivo) para filas y columnas.
    
    Args:
        parent: Widget padre donde se creará la celda
        clave_fila (int, optional): Número objetivo para la fila (parte superior derecha)
        clave_columna (int, optional): Número objetivo para la columna (parte inferior izquierda)
        
    Returns:
        tk.Canvas: Celda negra con línea diagonal y claves numéricas
        
    Características:
        - Fondo negro
        - Línea diagonal '/' de esquina superior izquierda a inferior derecha
        - Clave de fila en la parte superior derecha (si se proporciona)
        - Clave de columna en la parte inferior izquierda (si se proporciona)
        - Texto blanco sobre fondo negro
        - Tamaño estándar 45x45px
    """
    cell = tk.Canvas(
        parent,
        width=45,
        height=45,
        bg="black",
        highlightthickness=0,
        relief="flat"
    )
    
    # Dibujar línea diagonal
    cell.create_line(0, 0, 45, 45, fill="white", width=2)
    
    # Dibujar clave de fila (parte superior derecha)
    if clave_fila is not None:
        cell.create_text(
            35, 12,  # Posición en la parte superior derecha
            text=str(clave_fila),
            fill="white",
            font=("Arial", 8, "bold"),
            anchor="center"
        )
    
    # Dibujar clave de columna (parte inferior izquierda)
    if clave_columna is not None:
        cell.create_text(
            12, 35,  # Posición en la parte inferior izquierda
            text=str(clave_columna),
            fill="white",
            font=("Arial", 8, "bold"),
            anchor="center"
        )
    
    return cell 