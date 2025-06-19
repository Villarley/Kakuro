"""
Ventana principal del juego Kakuro
Maneja la interfaz principal con botones visibles
"""

import tkinter as tk
from tkinter import messagebox


class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Kakuro 2025")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz de usuario principal con botones"""
        self.root.configure(bg="#1e1e1e")  # Fondo oscuro (opcional)

        title_label = tk.Label(
            self.root,
            text="Bienvenido a Kakuro 2025 🧠",
            font=("Arial", 28, "bold"),
            fg="white",
            bg="#1e1e1e"
        )
        title_label.pack(pady=50)

        # Contenedor de botones
        button_frame = tk.Frame(self.root, bg="#1e1e1e")
        button_frame.pack()

        # Crear botones
        buttons = [
            ("🎮 Jugar", self.jugar),
            ("⚙️ Configurar", self.configurar),
            ("📘 Ayuda", self.ver_manual),
            ("ℹ️ Acerca de", self.acerca_de),
            ("🚪 Salir", self.root.quit)
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
                fg="black",
                activebackground="#5e5e5e",
                bd=0,
                highlightthickness=0
            )
            btn.pack(pady=10)

    # Acciones de los botones
    def jugar(self):
        messagebox.showinfo("Jugar", "Aquí se iniciará el juego...")

    def configurar(self):
        messagebox.showinfo("Configurar", "Aquí se configurará el nivel y el reloj.")

    def ver_manual(self):
        messagebox.showinfo("Manual", "Aquí se mostrará el manual de usuario.")

    def acerca_de(self):
        messagebox.showinfo(
            "Acerca de",
            "Kakuro 2025\nVersión 1.0\nAutor: Santiago Villarreal Arley\nCreado para - Taller de Programación 2025"
        )

    def run(self):
        """Ejecuta la aplicación"""
        self.root.mainloop()


if __name__ == "__main__":
    app = MainWindow()
    app.run()
