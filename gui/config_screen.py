import tkinter as tk


class ConfigScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1e1e1e")
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        label = tk.Label(
            self,
            text="⚙️ Pantalla de Configuración",
            font=("Arial", 24),
            bg="#1e1e1e",
            fg="white"
        )
        label.pack(pady=50)

        back_btn = tk.Button(
            self,
            text="← Volver al Inicio",
            font=("Arial", 14),
            command=lambda: self.controller.show_frame("HomeScreen"),
            bg="#3a3a3a",
            fg="#8A2BE2",
            activebackground="#5e5e5e",
            bd=0
        )
        back_btn.pack(pady=20)
