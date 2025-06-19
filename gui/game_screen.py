import tkinter as tk


class GameScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1e1e1e")
        self.controller = controller
        self.setup_ui()

    def setup_ui(self):
        # Título superior y entrada de nombre
        top_frame = tk.Frame(self, bg="#1e1e1e")
        top_frame.pack(pady=10)

        title = tk.Label(
            top_frame,
            text="🧩 KAKURO",
            font=("Arial Black", 32),
            bg="#1e1e1e",
            fg="white"
        )
        title.pack(side=tk.LEFT, padx=10)

        name_label = tk.Label(top_frame, text="Jugador:", fg="white", bg="#1e1e1e")
        name_label.pack(side=tk.LEFT, padx=5)

        self.name_entry = tk.Entry(top_frame, width=30)
        self.name_entry.pack(side=tk.LEFT)

        # Cuerpo principal: tablero + panel lateral
        body_frame = tk.Frame(self, bg="#1e1e1e")
        body_frame.pack(pady=10)

        # 🧩 Tablero (solo visual, sin lógica)
        board_frame = tk.Frame(body_frame, bg="#000000")
        board_frame.pack(side=tk.LEFT, padx=20)

        for row in range(9):
            for col in range(9):
                cell = tk.Label(
                    board_frame,
                    text="",  # Aquí pondremos claves más adelante
                    width=4,
                    height=2,
                    borderwidth=1,
                    relief="solid",
                    bg="white"
                )
                cell.grid(row=row, column=col, padx=1, pady=1)

        # 🎯 Panel lateral de números
        panel_frame = tk.Frame(body_frame, bg="#1e1e1e")
        panel_frame.pack(side=tk.LEFT, padx=20)

        for num in range(1, 10):
            btn = tk.Button(
                panel_frame,
                text=str(num),
                font=("Arial", 14),
                width=4,
                height=1,
                bg="white"
            )
            btn.pack(pady=3)

        # 🔧 Botones de acción
        action_frame = tk.Frame(self, bg="#1e1e1e")
        action_frame.pack(pady=10)

        buttons = [
            ("INICIAR JUEGO", "#e91e63"),
            ("DESHACER JUGADA", "#c5e1a5"),
            ("BORRAR JUEGO", "#90caf9"),
            ("REHACER JUGADA", "#80deea"),
            ("TERMINAR JUEGO", "#80cbc4"),
            ("GUARDAR JUEGO", "#ffb74d"),
            ("CARGAR JUEGO", "#ff8a65"),
            ("RÉCORDS", "#fff176")
        ]

        for idx, (label, color) in enumerate(buttons):
            btn = tk.Button(
                action_frame,
                text=label,
                font=("Arial", 10, "bold"),
                width=18,
                height=2,
                bg=color,
                command=lambda l=label: print(f"{l} clicado")
            )
            btn.grid(row=idx // 4, column=idx % 4, padx=10, pady=5)

        # ⏱️ Reloj y Nivel
        footer_frame = tk.Frame(self, bg="#1e1e1e")
        footer_frame.pack(pady=10)

        time_labels = ["Horas", "Minutos", "Segundos"]
        for i, label in enumerate(time_labels):
            tk.Label(
                footer_frame,
                text=label,
                fg="white",
                bg="#1e1e1e",
                font=("Arial", 10)
            ).grid(row=0, column=i, padx=10)

        for i in range(3):
            tk.Entry(
                footer_frame,
                width=5,
                justify="center"
            ).grid(row=1, column=i, padx=10)

        level_label = tk.Label(
            self,
            text="NIVEL FÁCIL",
            font=("Arial", 12, "bold"),
            fg="white",
            bg="#1e1e1e"
        )
        level_label.pack(pady=10)
