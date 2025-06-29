import tkinter as tk
from tkinter import messagebox
from logic.config_loader import load_configuracion
from logic.partida_loader import load_random_partida
from logic.record_manager import guardar_record, obtener_top_records, formatear_tiempo
from gui.components.cell_components import create_white_cell, create_black_cell, create_key_cell


class GameScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2c2c2c")
        self.controller = controller
        self.parent = parent
        self.nombre_jugador = "Jugador"  # Minitask 14
        self.partida_data = None  # Almacenar datos de la partida cargada
        self.board_size = 9  # Tamaño del tablero (9x9)
        self.juego_activo = False  # Bandera para controlar el estado del juego
        self.numero_seleccionado = None  # Número actualmente seleccionado por el jugador
        self.botones_numeros = []  # Lista para almacenar referencias a los botones numéricos
        self.estado_tablero = [[None for _ in range(9)] for _ in range(9)]  # Matriz para trackear el estado del tablero
        
        # 🧠 Estructura de datos para historial de jugadas
        self.historial_jugadas = []  # Stack principal para deshacer
        self.historial_rehacer = []  # Stack auxiliar para rehacer
        
        self.setup_ui()

    def setup_ui(self):
        # Título superior y entrada de nombre
        top_frame = tk.Frame(self, bg="#2c2c2c")
        top_frame.pack(pady=10)

        title = tk.Label(
            top_frame,
            text="KAKURO 2025",
            font=("Segoe UI", 24, "bold"),
            fg="#ffcc80",
            bg="#2c2c2c"
        )
        title.pack(side=tk.LEFT, padx=10)

        name_label = tk.Label(top_frame, text="Jugador:", fg="white", bg="#2c2c2c")
        name_label.pack(side=tk.LEFT, padx=5)

        self.name_entry = tk.Entry(top_frame, width=30)
        self.name_entry.pack(side=tk.LEFT)

        # Cuerpo principal: tablero + panel lateral
        body_frame = tk.Frame(self, bg="#2c2c2c")
        body_frame.pack(pady=10)

        # Tablero
        self.board_frame = tk.Frame(body_frame, bg="black")
        self.board_frame.pack(side=tk.LEFT, padx=20)

        # Cargar configuración y partida
        self.load_game_data()
        
        # Construir tablero dinámicamente
        self.build_dynamic_board()

        # Panel lateral de números
        panel_frame = tk.Frame(body_frame, bg="#2c2c2c")
        panel_frame.pack(side=tk.LEFT, padx=20)

        # Crear botones numéricos
        self.botones_numeros = []
        for num in range(1, 10):
            btn = tk.Button(
                panel_frame,
                text=str(num),
                width=4,
                height=2,
                font=("Segoe UI", 12, "bold"),
                bg="#3a3a3a",
                fg="white",
                state="disabled",
                command=lambda num=num: self.seleccionar_numero(num)
            )
            btn.pack(pady=3)
            self.botones_numeros.append(btn)

        # Botones de acción del juego
        self.actions_frame = tk.Frame(body_frame, bg="#2c2c2c")
        self.actions_frame.pack(side=tk.LEFT, padx=20)

        self.botones_accion = []

        action_buttons = [
            ("DESHACER JUGADA", "#c5e1a5", self.deshacer_jugada),
            ("REHACER JUGADA", "#80deea", self.rehacer_jugada),
            ("BORRAR CASILLA", "#90caf9", self.borrar_casilla),
            ("GUARDAR JUEGO", "#ffb74d", self.guardar_partida_actual),
            ("TERMINAR JUEGO", "#80cbc4", self.terminar_juego)
        ]

        for label, color, command in action_buttons:
            btn = tk.Button(
                self.actions_frame,
                text=label,
                font=("Segoe UI", 10, "bold"),
                width=15,
                height=2,
                bg=color,
                state="disabled",
                command=command
            )
            btn.pack(pady=5)
            self.botones_accion.append(btn)

        # Botones principales
        action_frame = tk.Frame(self, bg="#2c2c2c")
        action_frame.pack(pady=10)

        buttons = [
            ("INICIAR JUEGO", "#e91e63", self.activar_juego),
            ("CARGAR JUEGO", "#ff8a65", self.cargar_partida_guardada),
            ("RÉCORDS", "#fff176", self.ver_records),
            ("VOLVER", "#a1a1a1", lambda: self.controller.show_frame("HomeScreen"))
        ]

        for idx, (label, color, command) in enumerate(buttons):
            btn = tk.Button(
                action_frame,
                text=label,
                font=("Segoe UI", 10, "bold"),
                width=18,
                height=2,
                bg=color,
                command=command
            )
            btn.grid(row=idx // 4, column=idx % 4, padx=10, pady=5)

            if label == "INICIAR JUEGO":
                self.boton_iniciar = btn

        # Mostrar nivel actual
        nivel_actual = self.partida_data["nivel_de_dificultad"] if self.partida_data else "FÁCIL"
        level_label = tk.Label(
            self,
            text=f"NIVEL {nivel_actual}",
            font=("Segoe UI", 12, "bold"),
            fg="white",
            bg="#2c2c2c"
        )
        level_label.pack(pady=10)

    def activar_juego(self):
        """
        Activa el juego y cambia el estado de la interfaz.
        """
        from tkinter import simpledialog
        
        if self.juego_activo:
            print("El juego ya está activo. Ignorando clic adicional.")
            return
        
        # Pedir nombre del jugador
        self.nombre_jugador = simpledialog.askstring("Nombre", "¿Cuál es tu nombre?")
        if not self.nombre_jugador:
            self.nombre_jugador = "Jugador"
        
        # Activar el juego
        self.juego_activo = True
        self.boton_iniciar.config(state="disabled")
        
        # Mostrar confirmación
        try:
            messagebox.showinfo("Kakuro 2025", "¡El juego ha comenzado!")
        except Exception as e:
            print(f"Error al mostrar mensaje de confirmación: {e}")
        
        # Activar componentes
        self.activar_tablero()
        self.activar_botones()
        self.activar_botones_numeros()
        self.setup_reloj()
        
        print("Juego iniciado correctamente")

    def activar_tablero(self):
        """
        Activa el tablero reemplazando las celdas blancas por Buttons interactivos.
        """
        print("Activando tablero...")
        
        for fila in range(9):
            for columna in range(9):
                celda = self.celdas_blancas[fila][columna]
                
                if celda and isinstance(celda, tk.Label):
                    entry_btn = tk.Button(
                        self.board_frame,
                        width=5,
                        height=2,
                        font=("Segoe UI", 14, "bold"),
                        bg="white",
                        text="",
                        command=lambda r=fila, c=columna: self.colocar_numero_en_celda(r, c)
                    )
                    entry_btn.grid(row=fila, column=columna)
                    self.celdas_blancas[fila][columna] = entry_btn
        
        print("Tablero activado")

    def load_game_data(self):
        """
        Carga la configuración del juego y una partida aleatoria.
        Si no se puede cargar una partida válida, muestra un error.
        """
        try:
            # Cargar configuración para obtener el nivel actual
            config = load_configuracion()
            nivel = config.get("nivel", "FÁCIL")
            
            # Cargar partida aleatoria para el nivel
            self.partida_data = load_random_partida(nivel)
            
            if not self.partida_data:
                # Si no se pudo cargar la partida, intentar con un nivel diferente
                print(f"No hay partidas disponibles para el nivel: {nivel}")
                
                # Intentar con otros niveles en orden de preferencia
                niveles_alternativos = ["FÁCIL", "MEDIO", "DIFÍCIL", "EXPERTO"]
                for nivel_alt in niveles_alternativos:
                    if nivel_alt != nivel:
                        print(f"Intentando cargar partida para nivel: {nivel_alt}")
                        self.partida_data = load_random_partida(nivel_alt)
                        if self.partida_data:
                            print(f"Partida cargada para nivel alternativo: {nivel_alt}")
                            break
                
                if not self.partida_data:
                    # Si no se pudo cargar ninguna partida, mostrar error
                    self.show_error_message("No se pudo cargar una partida válida. Verifica que el archivo de partidas contenga datos.")
                    return
                
            print(f"Partida cargada: {self.partida_data['nivel_de_dificultad']} - Partida {self.partida_data['partida']}")
            print(f"Número de claves: {len(self.partida_data['claves'])}")
            
        except Exception as e:
            print(f"Error al cargar datos del juego: {e}")
            self.show_error_message("Error al cargar los datos del juego.")
            self.partida_data = None

    def show_error_message(self, message):
        """
        Muestra un mensaje de error en la interfaz.
        
        Args:
            message (str): Mensaje de error a mostrar
        """
        error_label = tk.Label(
            self,
            text=message,
            font=("Segoe UI", 14, "bold"),
            fg="red",
            bg="#2c2c2c"
        )
        error_label.pack(pady=20)

    def build_dynamic_board(self):
        """
        Construye el tablero dinámicamente basado en los datos de la partida.
        Crea un tablero 9x9 con celdas blancas bloqueadas por defecto,
        luego sobreescribe posiciones según las claves del juego.
        """
        # Siempre inicializar celdas_blancas, incluso si no hay partida_data
        self.celdas_blancas = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        
        # Paso 1: Crear tablero 9x9 con celdas blancas bloqueadas por defecto
        for fila in range(self.board_size):
            for columna in range(self.board_size):
                # Por defecto, colocar una celda blanca "bloqueada" (solo visual)
                white = tk.Label(
                    self.board_frame, 
                    width=5, 
                    height=2, 
                    bg="white", 
                    relief="solid", 
                    bd=1
                )
                white.grid(row=fila, column=columna)
                self.celdas_blancas[fila][columna] = white
        
        # Paso 2: Si hay datos de partida, sobreescribir posiciones según las claves del juego
        if self.partida_data and self.partida_data.get('claves'):
            self.apply_game_claves()
            print(f"Tablero 9x9 construido con {len(self.partida_data['claves'])} claves")
        else:
            print("Tablero 9x9 construido sin claves (modo demo)")

    def apply_game_claves(self):
        """
        Aplica las claves del juego al tablero, sobreescribiendo las celdas blancas
        con celdas negras o celdas con claves según corresponda.
        """
        if not self.partida_data or not self.partida_data.get('claves'):
            print("No hay claves para aplicar al tablero")
            return
            
        for clave in self.partida_data["claves"]:
            fila = clave["fila"] - 1  # Convertir a índice base 0
            columna = clave["columna"] - 1
            tipo_clave = clave["tipo_de_clave"]
            valor_clave = clave["clave"]
            casillas = clave["casillas"]
            
            # Verificar que los índices estén dentro del rango del tablero
            if fila < 0 or fila >= self.board_size or columna < 0 or columna >= self.board_size:
                print(f"Índice fuera de rango: fila={fila}, columna={columna}")
                continue
            
            # Destruir la celda blanca existente en esta posición
            if self.celdas_blancas[fila][columna]:
                self.celdas_blancas[fila][columna].destroy()
                self.celdas_blancas[fila][columna] = None
            
            # Determinar qué tipo de celda colocar según los datos de la clave
            if valor_clave == 0 and casillas == 0:
                # Caso a): clave = 0 y casillas = 0 → celda negra
                cell = create_black_cell(self.board_frame, fila, columna)
                print(f"Celda negra colocada en ({fila+1}, {columna+1})")
            else:
                # Caso b): tipo_de_clave = "F" o "C" → celda con clave
                clave_fila = None
                clave_columna = None
                
                if tipo_clave == "F":
                    clave_fila = valor_clave
                elif tipo_clave == "C":
                    clave_columna = valor_clave
                
                # Crear texto para la celda con clave
                texto_clave = ""
                if clave_fila is not None and clave_columna is not None:
                    texto_clave = f"{clave_fila}\\{clave_columna}"
                elif clave_fila is not None:
                    texto_clave = f"{clave_fila}\\"
                elif clave_columna is not None:
                    texto_clave = f"\\{clave_columna}"
                
                cell = create_key_cell(self.board_frame, fila, columna, texto_clave)
                print(f"Celda con clave {tipo_clave}={valor_clave} colocada en ({fila+1}, {columna+1})")

    def activar_botones(self):
        """Activa todos los botones de acción del juego."""
        for boton in self.botones_accion:
            boton.config(state="normal")
        print("Botones de acción activados")

    def activar_botones_numeros(self):
        """Activa todos los botones numéricos."""
        for boton in self.botones_numeros:
            boton.config(state="normal")
        print("Botones numéricos activados")

    def seleccionar_numero(self, numero):
        """
        Selecciona un número para colocar en el tablero.
        """
        self.numero_seleccionado = numero
        
        # Resaltar el botón seleccionado
        for i, boton in enumerate(self.botones_numeros, 1):
            if i == numero:
                boton.config(bg="#ffd700")  # Dorado
            else:
                boton.config(bg="#3a3a3a")  # Gris
        
        print(f"Número seleccionado: {numero}")

    def colocar_numero_en_celda(self, fila, columna):
        """
        Coloca un número en una celda blanca del tablero.
        """
        if not self.juego_activo:
            print("El juego no está activo.")
            return
        
        if self.numero_seleccionado is None:
            messagebox.showwarning(
                "Kakuro 2025", 
                "Por favor, selecciona un número del panel numérico antes de colocarlo en el tablero."
            )
            return
        
        celda = self.celdas_blancas[fila][columna]
        
        if celda and isinstance(celda, tk.Button):
            valor_actual = self.estado_tablero[fila][columna]
            
            # Solo registrar si el valor cambió
            if self.numero_seleccionado != valor_actual:
                self.historial_jugadas.append({
                    "fila": fila,
                    "columna": columna,
                    "valor_anterior": valor_actual,
                    "valor_nuevo": self.numero_seleccionado
                })
                self.historial_rehacer.clear()
            
            # Actualizar celda y estado
            celda.config(text=str(self.numero_seleccionado))
            self.estado_tablero[fila][columna] = self.numero_seleccionado
            
            print(f"Número {self.numero_seleccionado} colocado en ({fila+1}, {columna+1})")
            
            # Verificar si el jugador ha completado el tablero
            if self.verificar_victoria():
                self.declarar_victoria()

    def deshacer_jugada(self):
        """Deshace la última jugada realizada."""
        if not self.historial_jugadas:
            messagebox.showinfo("Deshacer", "No hay jugadas para deshacer.")
            return

        jugada = self.historial_jugadas.pop()
        fila = jugada["fila"]
        columna = jugada["columna"]
        valor_anterior = jugada["valor_anterior"]

        celda = self.celdas_blancas[fila][columna]
        celda.config(text=str(valor_anterior) if valor_anterior else "")
        self.estado_tablero[fila][columna] = valor_anterior

        self.historial_rehacer.append(jugada)
        print(f"Jugada deshecha: ({fila+1}, {columna+1}) → {valor_anterior}")

    def rehacer_jugada(self):
        """Rehace la última jugada deshecha."""
        if not self.historial_rehacer:
            messagebox.showinfo("Rehacer", "No hay jugadas para rehacer.")
            return

        jugada = self.historial_rehacer.pop()
        fila = jugada["fila"]
        columna = jugada["columna"]
        valor_nuevo = jugada["valor_nuevo"]

        celda = self.celdas_blancas[fila][columna]
        celda.config(text=str(valor_nuevo) if valor_nuevo else "")
        self.estado_tablero[fila][columna] = valor_nuevo

        self.historial_jugadas.append(jugada)
        print(f"Jugada rehecha: ({fila+1}, {columna+1}) → {valor_nuevo}")

    def verificar_tablero(self):
        """
        Verifica si el tablero está completo y todas las claves numéricas se cumplen.
        """
        if not self.juego_activo:
            messagebox.showwarning("Validación", "El juego no está activo.")
            return False

        if not self.partida_data:
            messagebox.showerror("Error", "No hay datos de partida cargados.")
            return False

        print("Iniciando verificación del tablero...")

        # Verificar que todas las celdas estén completas
        for fila in range(9):
            for col in range(9):
                celda = self.estado_tablero[fila][col]
                if celda is None:
                    messagebox.showwarning("Tablero Incompleto", "Hay celdas vacías en el tablero.")
                    return False

        # Validar claves de filas y columnas
        claves = self.partida_data.get("claves", [])
        
        if not claves:
            messagebox.showinfo("Sin Claves", "No hay claves para validar en esta partida.")
            return True

        for clave in claves:
            tipo = clave["tipo_de_clave"]
            fila = clave["fila"] - 1
            columna = clave["columna"] - 1
            esperado = clave["clave"]
            casillas = clave["casillas"]

            suma_real = 0
            valores_vistos = set()

            try:
                if tipo == "F":  # Clave de Fila
                    for offset in range(1, casillas + 1):
                        valor = self.estado_tablero[fila][columna + offset]
                        if valor in valores_vistos:
                            messagebox.showwarning("Error de Validación", f"Valor duplicado {valor} en la clave de fila.")
                            return False
                        if not (1 <= valor <= 9):
                            messagebox.showwarning("Error de Validación", f"Valor fuera de rango {valor} en la clave de fila.")
                            return False
                        valores_vistos.add(valor)
                        suma_real += valor

                elif tipo == "C":  # Clave de Columna
                    for offset in range(1, casillas + 1):
                        valor = self.estado_tablero[fila + offset][columna]
                        if valor in valores_vistos:
                            messagebox.showwarning("Error de Validación", f"Valor duplicado {valor} en la clave de columna.")
                            return False
                        if not (1 <= valor <= 9):
                            messagebox.showwarning("Error de Validación", f"Valor fuera de rango {valor} en la clave de columna.")
                            return False
                        valores_vistos.add(valor)
                        suma_real += valor

            except IndexError as e:
                messagebox.showerror("Error de Validación", "Error de índice al validar las claves del tablero.")
                return False

            if suma_real != esperado:
                messagebox.showwarning("Error de Validación", f"Clave incorrecta en ({fila+1},{columna+1}): esperada={esperado}, actual={suma_real}")
                return False

        print("Tablero validado correctamente.")
        messagebox.showinfo("¡Felicidades!", "¡El tablero está completo y todas las claves son correctas!")
        return True

    def verificar_victoria(self):
        """
        Verifica si el tablero está completo y correcto para declarar victoria.
        Este método se puede llamar cuando el jugador complete el tablero.
        """
        if not self.juego_activo:
            return False
        
        if not self.partida_data:
            return False
        
        # Verificar que todas las celdas estén completas
        for fila in range(9):
            for col in range(9):
                celda = self.estado_tablero[fila][col]
                if celda is None:
                    return False
        
        # Validar claves de filas y columnas
        claves = self.partida_data.get("claves", [])
        
        if not claves:
            return True
        
        for clave in claves:
            tipo = clave["tipo_de_clave"]
            fila = clave["fila"] - 1
            columna = clave["columna"] - 1
            esperado = clave["clave"]
            casillas = clave["casillas"]

            suma_real = 0
            valores_vistos = set()

            try:
                if tipo == "F":  # Clave de Fila
                    for offset in range(1, casillas + 1):
                        valor = self.estado_tablero[fila][columna + offset]
                        if valor in valores_vistos:
                            return False
                        if not (1 <= valor <= 9):
                            return False
                        valores_vistos.add(valor)
                        suma_real += valor

                elif tipo == "C":  # Clave de Columna
                    for offset in range(1, casillas + 1):
                        valor = self.estado_tablero[fila + offset][columna]
                        if valor in valores_vistos:
                            return False
                        if not (1 <= valor <= 9):
                            return False
                        valores_vistos.add(valor)
                        suma_real += valor

            except IndexError:
                return False

            if suma_real != esperado:
                return False
        
        return True

    def declarar_victoria(self):
        """
        Declara la victoria del jugador cuando el tablero está completo y correcto.
        """
        if self.verificar_victoria():
            print("¡Juego completado correctamente!")
            
            # Guardar récord si corresponde
            self.guardar_record_juego()
            
            # Mensaje de victoria
            nivel = self.partida_data.get("nivel_de_dificultad", "FÁCIL")
            tiempo_usado = 0
            if hasattr(self, 'game_timer'):
                tiempo_usado = self.game_timer.get_elapsed_time()
            
            msg = f"🎉 ¡Felicidades {self.nombre_jugador}!\nCompletaste el juego en {tiempo_usado} segundos."
            messagebox.showinfo("¡Juego completado!", msg)
            print(f"[GAME] {self.nombre_jugador} terminó el juego con éxito en nivel {nivel}")
            
            return True
        else:
            return False

    def terminar_juego(self):
        """
        Termina el juego según los requisitos del documento.
        - Pregunta confirmación SI/NO
        - Si SI: termina inmediatamente y muestra nuevo juego
        - Si NO: continúa jugando
        - Solo disponible si el juego ha iniciado
        """
        # Verificar que el juego esté activo
        if not self.juego_activo:
            messagebox.showwarning("Terminar Juego", "NO SE HA INICIADO EL JUEGO.")
            return
        
        # Preguntar confirmación
        respuesta = messagebox.askyesno(
            "Terminar Juego", 
            "¿ESTÁ SEGURO DE TERMINAR EL JUEGO (SI/NO)?"
        )
        
        if respuesta:  # SI - Terminar inmediatamente
            print("Jugador confirmó terminar el juego")
            
            # Terminar el juego actual
            self.juego_activo = False
            
            # Limpiar el tablero actual
            for widget in self.board_frame.winfo_children():
                widget.destroy()
            
            # Limpiar historiales
            self.historial_jugadas.clear()
            self.historial_rehacer.clear()
            
            # Limpiar estado del tablero
            self.estado_tablero = [[None for _ in range(9)] for _ in range(9)]
            
            # Detener temporizador si existe
            if hasattr(self, 'game_timer'):
                self.game_timer.stop()
                delattr(self, 'game_timer')
            
            # Ocultar reloj si existe
            if hasattr(self, 'reloj_label'):
                self.reloj_label.destroy()
                delattr(self, 'reloj_label')
            
            # Cargar nueva partida
            self.load_game_data()
            self.build_dynamic_board()
            
            # Reactivar botón de iniciar juego
            if hasattr(self, 'boton_iniciar'):
                self.boton_iniciar.config(state="normal")
            
            # Desactivar botones de juego
            self.activar_botones()
            self.activar_botones_numeros()
            for boton in self.botones_accion:
                boton.config(state="disabled")
            for boton in self.botones_numeros:
                boton.config(state="disabled")
            
            # Limpiar selección de número
            self.numero_seleccionado = None
            
            messagebox.showinfo("Nuevo Juego", "Se ha cargado un nuevo juego. Presiona 'INICIAR JUEGO' para comenzar.")
            
        else:  # NO - Continuar jugando
            print("Jugador canceló terminar el juego")
            # No hacer nada, el juego continúa normalmente

    def guardar_record_juego(self):
        """Guarda el récord del jugador si el juego fue completado correctamente."""
        if not hasattr(self, 'game_timer'):
            print("[RECORDS] No hay temporizador activo, no se guarda récord")
            return
        
        config = load_configuracion()
        if config.get("tipo_reloj") == "SIN RELOJ":
            print("[RECORDS] Modo sin reloj, no se guarda récord")
            return
        
        nombre_jugador = self.nombre_jugador
        tiempo_usado = self.game_timer.get_elapsed_time()
        nivel = self.partida_data.get("nivel_de_dificultad", "FÁCIL")
        
        print(f"[RECORDS] Guardando récord: {nombre_jugador} - Nivel {nivel} - Tiempo {formatear_tiempo(tiempo_usado)}")
        
        if guardar_record(nombre_jugador, nivel, tiempo_usado):
            messagebox.showinfo("🏆 ¡Nuevo Récord!", f"¡Felicidades {nombre_jugador}!\nHas completado el nivel {nivel} en {formatear_tiempo(tiempo_usado)}")
        else:
            print("[RECORDS] Error al guardar el récord")

    def ver_records(self):
        """Muestra los mejores récords para el nivel actual."""
        nivel = self.partida_data.get("nivel_de_dificultad", "FÁCIL") if self.partida_data else "FÁCIL"
        records = obtener_top_records(nivel)
        
        if not records:
            messagebox.showinfo("🏆 Récords", f"Aún no hay récords para el nivel {nivel}.")
            return

        msg = f"🏆 Mejores tiempos - Nivel {nivel}:\n\n"
        for i, r in enumerate(records, 1):
            tiempo_formateado = formatear_tiempo(r['tiempo'])
            msg += f"{i}. {r['jugador']} - {tiempo_formateado} - {r['fecha']}\n"

        messagebox.showinfo("🏆 Récords", msg)
        print(f"[RECORDS] Mostrados {len(records)} récords para nivel {nivel}")

    def guardar_partida_actual(self):
        """Guarda el estado actual del juego en un archivo JSON."""
        import json
        import os
        
        if not self.juego_activo:
            messagebox.showwarning("Guardar Juego", "No hay una partida activa para guardar.")
            return

        if not self.partida_data:
            messagebox.showerror("Error", "No hay datos de partida cargados.")
            return

        try:
            # Preparar datos para guardar
            datos_guardado = {
                "nivel": self.partida_data.get("nivel_de_dificultad", "FÁCIL"),
                "partida": self.partida_data.get("partida", 1),
                "tablero": self.estado_tablero,
                "claves": self.partida_data.get("claves", []),
                "reloj": self.partida_data.get("reloj", "SIN RELOJ"),
                "fecha_guardado": "2025-01-01",
                "jugador": self.name_entry.get() if hasattr(self, 'name_entry') else "Jugador",
                "historial_jugadas": len(self.historial_jugadas),
                "historial_rehacer": len(self.historial_rehacer)
            }

            # Guardar tiempo restante si hay temporizador activo
            if hasattr(self, 'game_timer'):
                tiempo_restante = self.game_timer.get_remaining_time()
                if tiempo_restante is not None:
                    horas = tiempo_restante // 3600
                    minutos = (tiempo_restante % 3600) // 60
                    segundos = tiempo_restante % 60
                    
                    datos_guardado["tiempo_restante"] = {
                        "horas": horas,
                        "minutos": minutos,
                        "segundos": segundos
                    }

            # Crear directorio y guardar archivo
            os.makedirs("data", exist_ok=True)
            archivo_guardado = "data/kakuro2025_guardado.json"
            
            with open(archivo_guardado, "w", encoding="utf-8") as f:
                json.dump(datos_guardado, f, indent=4, ensure_ascii=False)

            messagebox.showinfo("Guardar Juego", "✅ Partida guardada exitosamente.")
            print(f"[LOG] Partida guardada en {archivo_guardado}")

        except Exception as e:
            print(f"[ERROR] No se pudo guardar la partida: {e}")
            messagebox.showerror("Guardar Juego", f"❌ Error al guardar la partida: {str(e)}")

    def cargar_partida_guardada(self):
        """Carga una partida guardada desde el archivo JSON."""
        import json
        import os
        
        ruta = "data/kakuro2025_guardado.json"

        if not os.path.exists(ruta):
            messagebox.showwarning("Cargar Partida", "No hay partida guardada disponible.")
            return

        try:
            # Leer archivo guardado
            with open(ruta, "r", encoding="utf-8") as f:
                partida = json.load(f)

            # Restaurar estado del juego
            self.partida_data = {
                "nivel_de_dificultad": partida.get("nivel", "FÁCIL"),
                "partida": partida.get("partida", 1),
                "claves": partida.get("claves", []),
                "reloj": partida.get("reloj", "SIN RELOJ")
            }

            self.estado_tablero = partida.get("tablero", [[None]*9 for _ in range(9)])

            # Restaurar tiempo restante si existe
            tiempo_restante_data = partida.get("tiempo_restante", {})
            if tiempo_restante_data:
                horas = tiempo_restante_data.get("horas", 0)
                minutos = tiempo_restante_data.get("minutos", 0)
                segundos = tiempo_restante_data.get("segundos", 0)
                self.tiempo_restante = horas * 3600 + minutos * 60 + segundos
            else:
                self.tiempo_restante = None

            # Restaurar información del jugador
            if hasattr(self, 'name_entry') and partida.get("jugador"):
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, partida.get("jugador"))

            # Limpiar historiales
            self.historial_jugadas.clear()
            self.historial_rehacer.clear()

            # Reconstruir tablero
            for widget in self.board_frame.winfo_children():
                widget.destroy()

            self.build_dynamic_board()
            self.apply_game_claves()
            self.activar_tablero()

            # Restaurar valores en el tablero
            celdas_restauradas = 0
            for fila in range(9):
                for col in range(9):
                    valor = self.estado_tablero[fila][col]
                    if isinstance(valor, int) and 1 <= valor <= 9:
                        celda = self.celdas_blancas[fila][col]
                        if isinstance(celda, tk.Button):
                            celda.config(text=str(valor))
                            celdas_restauradas += 1

            # Activar interfaz
            self.juego_activo = True
            self.activar_botones()
            self.activar_botones_numeros()
            
            if hasattr(self, 'boton_iniciar'):
                self.boton_iniciar.config(state="disabled")

            # Mostrar confirmación
            nivel_actual = self.partida_data["nivel_de_dificultad"]
            messagebox.showinfo("Cargar Juego", f"✅ Partida restaurada correctamente.\nNivel: {nivel_actual}\nCeldas llenas: {celdas_restauradas}/81")

            # Configurar reloj
            self.setup_reloj()

        except json.JSONDecodeError as e:
            messagebox.showerror("Cargar Juego", "❌ Error al leer el archivo guardado (formato inválido).")
        except Exception as e:
            messagebox.showerror("Cargar Juego", f"❌ Error al cargar la partida: {str(e)}")

    def setup_reloj(self):
        """Configura el reloj según la configuración del juego."""
        config = load_configuracion()
        tipo_reloj = config.get("tipo_reloj", "CRONÓMETRO")
        
        if tipo_reloj == "SIN RELOJ":
            return
        
        try:
            from utils.timer import GameTimer
        except ImportError as e:
            print(f"[RELOJ] Error al importar GameTimer: {e}")
            return
        
        tiempo_limite = None
        if tipo_reloj == "TEMPORIZADOR":
            tiempo_limite = config.get("tiempo_limite", 1800)
        
        self.game_timer = GameTimer(time_limit=tiempo_limite)
        self.game_timer.set_time_update_callback(self.actualizar_reloj_ui)
        self.game_timer.set_time_limit_callback(self.tiempo_agotado)
        
        self._create_timer_display()
        self.game_timer.start()

    def _create_timer_display(self):
        """Crea el widget visual del reloj"""
        if not hasattr(self, 'reloj_label'):
            # Buscar un frame apropiado para colocar el reloj
            if hasattr(self, 'body_frame'):
                parent_frame = self.body_frame
            else:
                parent_frame = self
            
            self.reloj_label = tk.Label(
                parent_frame,
                text="",
                font=("Segoe UI", 16, "bold"),
                bg="#2c2c2c",
                fg="#ff6b6b"  # Color rojo para llamar la atención
            )
            self.reloj_label.pack(pady=10)
            print("[RELOJ] Widget visual del reloj creado")

    def actualizar_reloj_ui(self, tiempo_transcurrido):
        """Actualiza la interfaz del reloj según el tipo configurado."""
        config = load_configuracion()
        tipo_reloj = config.get("tipo_reloj", "CRONÓMETRO")
        
        if tipo_reloj == "TEMPORIZADOR":
            tiempo_restante = self.game_timer.get_remaining_time()
            if tiempo_restante is None:
                return
                
            horas = tiempo_restante // 3600
            minutos = (tiempo_restante % 3600) // 60
            segundos = tiempo_restante % 60

            tiempo_str = f"⏳ Tiempo restante: {horas:02}:{minutos:02}:{segundos:02}"
            
            if tiempo_restante <= 300:
                color = "#ff0000"
            elif tiempo_restante <= 600:
                color = "#ff6b6b"
            else:
                color = "#ffffff"
        else:
            horas = tiempo_transcurrido // 3600
            minutos = (tiempo_transcurrido % 3600) // 60
            segundos = tiempo_transcurrido % 60

            tiempo_str = f"⏱️ Tiempo transcurrido: {horas:02}:{minutos:02}:{segundos:02}"
            color = "#ffffff"
        
        if hasattr(self, 'reloj_label'):
            self.reloj_label.config(text=tiempo_str, fg=color)

    def tiempo_agotado(self):
        """Maneja cuando se agota el tiempo."""
        messagebox.showwarning("Tiempo Agotado", "¡Se ha agotado el tiempo!")
        self.terminar_juego()

    def borrar_casilla(self):
        """
        Borra el número de la celda seleccionada.
        """
        if not self.juego_activo:
            messagebox.showwarning("Borrar Casilla", "El juego no está activo.")
            return
        
        if self.numero_seleccionado is None:
            messagebox.showwarning("Borrar Casilla", "Por favor, selecciona un número del panel numérico.")
            return
        
        # Buscar la celda que contiene el número seleccionado
        for fila in range(9):
            for columna in range(9):
                celda = self.celdas_blancas[fila][columna]
                if (isinstance(celda, tk.Button) and 
                    celda.cget("text") == str(self.numero_seleccionado)):
                    
                    # Capturar el valor actual antes de borrar
                    valor_actual = self.estado_tablero[fila][columna]
                    
                    # Registrar la jugada en el historial
                    self.historial_jugadas.append({
                        "fila": fila,
                        "columna": columna,
                        "valor_anterior": valor_actual,
                        "valor_nuevo": None
                    })
                    # Limpiar el historial de rehacer
                    self.historial_rehacer.clear()
                    
                    # Borrar el número
                    celda.config(text="")
                    self.estado_tablero[fila][columna] = None
                    
                    print(f"Casilla borrada en ({fila+1}, {columna+1})")
                    return
        
        messagebox.showinfo("Borrar Casilla", f"No se encontró el número {self.numero_seleccionado} en el tablero.")
