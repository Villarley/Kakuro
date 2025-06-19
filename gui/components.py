"""
Componentes reutilizables de la interfaz de usuario
Botones personalizados, panel de números, reloj, etc.
"""

import tkinter as tk
from tkinter import ttk


class PurpleButton(tk.Button):
    """Botón personalizado con texto púrpura y bordes redondeados"""
    
    def __init__(self, parent, text, command=None, **kwargs):
        # Configuración por defecto para el botón púrpura
        default_config = {
            'font': ("Arial", 16),
            'width': 20,
            'height': 2,
            'bg': "#3a3a3a",
            'fg': "#8A2BE2",  # Color púrpura
            'activebackground': "#5e5e5e",
            'activeforeground': "#9370DB",  # Púrpura más claro al hacer hover
            'bd': 0,
            'highlightthickness': 0,
            'relief': 'flat',
            'cursor': 'hand2'
        }
        
        # Actualizar con configuraciones personalizadas
        default_config.update(kwargs)
        
        super().__init__(parent, text=text, command=command, **default_config)
        
        # Aplicar bordes redondeados usando un canvas personalizado
        self._create_rounded_button()
    
    def _create_rounded_button(self):
        """Crea el efecto de bordes redondeados"""
        # Configurar el estilo del botón para bordes redondeados
        self.configure(
            relief="flat",
            borderwidth=0,
            highlightthickness=0
        )
        
        # Crear un canvas para dibujar el botón redondeado
        canvas = tk.Canvas(
            self,
            bg=self.cget('bg'),
            highlightthickness=0,
            relief="flat"
        )
        canvas.place(relwidth=1, relheight=1)
        
        # Dibujar el rectángulo redondeado
        def draw_rounded_rect(event=None):
            canvas.delete("all")
            width = self.winfo_width()
            height = self.winfo_height()
            radius = min(width, height) // 8  # Radio para los bordes redondeados
            
            # Dibujar rectángulo redondeado
            canvas.create_rounded_rectangle(
                2, 2, width-2, height-2,
                radius=radius,
                fill=self.cget('bg'),
                outline="",
                tags="button_bg"
            )
        
        # Configurar el canvas para redibujar cuando cambie el tamaño
        canvas.bind('<Configure>', draw_rounded_rect)
        
        # Configurar eventos de hover
        def on_enter(event):
            canvas.itemconfig("button_bg", fill=self.cget('activebackground'))
            self.configure(fg=self.cget('activeforeground'))
        
        def on_leave(event):
            canvas.itemconfig("button_bg", fill=self.cget('bg'))
            self.configure(fg="#8A2BE2")
        
        canvas.bind('<Enter>', on_enter)
        canvas.bind('<Leave>', on_leave)
        self.bind('<Enter>', on_enter)
        self.bind('<Leave>', on_leave)


# Extender Canvas para soportar rectángulos redondeados
def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
    """Crea un rectángulo con esquinas redondeadas"""
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1
    ]
    return self.create_polygon(points, **kwargs, smooth=True)

# Añadir el método al Canvas
tk.Canvas.create_rounded_rectangle = create_rounded_rectangle


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
    """Botón personalizado para el juego (legacy - usar PurpleButton en su lugar)"""
    def __init__(self, parent, text, command=None):
        self.button = tk.Button(parent, text=text, command=command)
    
    def pack(self, **kwargs):
        return self.button.pack(**kwargs) 