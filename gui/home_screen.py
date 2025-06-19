import tkinter as tk
from tkinter import messagebox


class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1e1e1e")
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        title_label = tk.Label(
            self,
            text="Bienvenido a Kakuro 2025 🧠",
            font=("Arial", 28, "bold"),
            fg="white",
            bg="#1e1e1e"
        )
        title_label.pack(pady=50)

        button_frame = tk.Frame(self, bg="#1e1e1e")
        button_frame.pack()

        buttons = [
            ("🎮 Jugar", lambda: self.controller.show_frame("GameScreen")),
            ("⚙️ Configurar", lambda: self.controller.show_frame("ConfigScreen")),
            ("📘 Ayuda", self.ver_manual),
            ("ℹ️ Acerca de", self.acerca_de),
            ("🚪 Salir", self.controller.quit)
        ]

        for text, command in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                font=("Arial", 16),
                width=20,
                height=2,
                command=command,
                bg="#3a3a3a",
                fg="white",
                activebackground="#5e5e5e",
                bd=0
            )
            btn.pack(pady=10)

    def ver_manual(self):
        messagebox.showinfo("Manual", "Aquí se mostrará el manual de usuario.")

    def acerca_de(self):
        messagebox.showinfo(
            "Acerca de",
            "Kakuro 2025\nVersión 1.0\nAutor: Santiago Villarreal Arley"
        )
