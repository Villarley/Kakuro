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

        # 🧩 Tablero (cargado dinámicamente desde JSON)
        # Crear Frame para el tablero
        self.board_frame = tk.Frame(body_frame, bg="black")
        self.board_frame.pack(side=tk.LEFT, padx=20)

        # Cargar configuración y partida
        self.load_game_data()
        
        # Construir tablero dinámicamente
        self.build_dynamic_board()

        # 🎯 Panel lateral de números
        panel_frame = tk.Frame(body_frame, bg="#2c2c2c")
        panel_frame.pack(side=tk.LEFT, padx=20)

        for num in range(1, 10):
            btn = tk.Button(
                panel_frame,
                text=str(num),
                font=("Segoe UI", 12, "bold"),
                width=4,
                height=1,
                bg="white"
            )
            btn.pack(pady=3)
            self.botones_numeros.append(btn)

        # 🔧 Botones de acción del juego (según documento oficial)
        # Estos botones representan las acciones disponibles durante el juego activo
        self.actions_frame = tk.Frame(body_frame, bg="#2c2c2c")
        self.actions_frame.pack(side=tk.LEFT, padx=20)

        # Lista para almacenar referencias a los botones de acción
        self.botones_accion = []

        # Definir botones de acción según el documento oficial del proyecto
        action_buttons = [
            ("DESHACER JUGADA", "#c5e1a5"),
            ("REHACER JUGADA", "#80deea"),
            ("BORRAR CASILLA", "#90caf9"),
            ("GUARDAR JUEGO", "#ffb74d"),
            ("TERMINAR JUEGO", "#80cbc4")
        ]

        # Crear botones de acción con estado inicial desactivado
        for i, (label, color) in enumerate(action_buttons):
            # Determinar el comando específico para cada botón
            if label == "DESHACER JUGADA":
                command = self.deshacer_jugada
            elif label == "REHACER JUGADA":
                command = self.rehacer_jugada
            elif label == "TERMINAR JUEGO":
                command = self.terminar_juego
            elif label == "GUARDAR JUEGO":
                command = self.guardar_partida_actual
            else:
                # Para otros botones, mantener el comportamiento genérico por ahora
                command = lambda l=label: print(f"Botón {l} clicado (funcionalidad pendiente)")
            
            btn = tk.Button(
                self.actions_frame,
                text=label,
                font=("Segoe UI", 10, "bold"),
                width=15,
                height=2,
                bg=color,
                state="disabled",  # Botones desactivados inicialmente
                command=command
            )
            btn.pack(pady=5)
            self.botones_accion.append(btn)

        # 🔢 Panel numérico (números del 1 al 9 para selección del jugador)
        # Este panel permite al jugador seleccionar qué número colocar en el tablero
        self.numeros_frame = tk.Frame(self, bg="#2c2c2c")
        self.numeros_frame.pack(side=tk.TOP, pady=20)

        # Limpiar la lista de botones numéricos para evitar duplicados
        self.botones_numeros.clear()

        # Crear 9 botones numerados del 1 al 9
        for n in range(1, 10):
            btn = tk.Button(
                self.numeros_frame,
                text=str(n),
                width=4,
                height=2,
                font=("Segoe UI", 12, "bold"),
                bg="#3a3a3a",
                fg="white",
                state="disabled",  # Desactivados al inicio
                command=lambda num=n: self.seleccionar_numero(num)
            )
            btn.grid(row=0, column=n-1, padx=2)
            self.botones_numeros.append(btn)  # Guardarlos en self.botones_numeros

        # 🔧 Botones de acción
        action_frame = tk.Frame(self, bg="#2c2c2c")
        action_frame.pack(pady=10)

        buttons = [
            ("INICIAR JUEGO", "#e91e63"),
            ("CARGAR JUEGO", "#ff8a65"),
            ("RÉCORDS", "#fff176"),
            ("VOLVER", "#a1a1a1")  # Botón para volver al menú principal
        ]

        for idx, (label, color) in enumerate(buttons):
            command = None
            if label == "INICIAR JUEGO":
                command = self.activar_juego
            elif label == "CARGAR JUEGO":
                command = self.cargar_partida_guardada
            elif label == "RÉCORDS":
                command = self.ver_records
            elif label == "VOLVER":
                command = lambda: self.controller.show_frame("HomeScreen")

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

            # Guardar referencia al botón INICIAR JUEGO para poder desactivarlo luego
            if label == "INICIAR JUEGO":
                self.boton_iniciar = btn

        # ⏱️ Reloj y Nivel
        footer_frame = tk.Frame(self, bg="#2c2c2c")
        footer_frame.pack(pady=10)

        time_labels = ["Horas", "Minutos", "Segundos"]
        for i, label in enumerate(time_labels):
            tk.Label(
                footer_frame,
                text=label,
                fg="white",
                bg="#2c2c2c",
                font=("Segoe UI", 10)
            ).grid(row=0, column=i, padx=10)

        for i in range(3):
            tk.Entry(
                footer_frame,
                width=5,
                justify="center"
            ).grid(row=1, column=i, padx=10)

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
        Este método se ejecuta cuando el usuario hace clic en "INICIAR JUEGO".
        Incluye validación para evitar múltiples activaciones.
        """
        from tkinter import simpledialog
        if self.juego_activo:
            print("El juego ya está activo. Ignorando clic adicional.")
            return
        # Pedir nombre del jugador
        self.nombre_jugador = simpledialog.askstring("Nombre", "¿Cuál es tu nombre?")
        if not self.nombre_jugador:
            self.nombre_jugador = "Jugador"
        # Paso 1: Cambiar el estado del juego a activo
        self.juego_activo = True
        print("Juego iniciado")
        
        # Paso 2: Desactivar el botón "INICIAR JUEGO" para evitar múltiples clics
        self.boton_iniciar.config(state="disabled")
        
        # Paso 3: Mostrar mensaje de confirmación al usuario
        try:
            messagebox.showinfo("Kakuro 2025", "¡El juego ha comenzado!")
        except Exception as e:
            print(f"Error al mostrar mensaje de confirmación: {e}")
        
        # Paso 4: Activar el tablero (reemplazar Labels por Entries interactivos)
        self.activar_tablero()
        
        # Paso 5: Activar botones de acción del juego
        self.activar_botones()
        
        # Paso 6: Activar botones numéricos
        self.activar_botones_numeros()
        
        # Paso 7: Configurar el reloj si es necesario
        self.setup_reloj()
        
        # Paso 8: Preparar para futuras funcionalidades
        # TODO: Implementar funcionalidad específica de cada botón
        
        # Paso 9: Validar que el juego se activó correctamente
        if self.juego_activo:
            print("Estado del juego: ACTIVO")
            print("Botón INICIAR JUEGO: DESACTIVADO")
            print("Mensaje de confirmación mostrado al usuario")
            print("Tablero activado: Labels reemplazados por Buttons interactivos")
            print("Botones de acción: ACTIVADOS")
            print("Botones numéricos: ACTIVADOS")
            print("Reloj configurado (si aplica)")
        else:
            print("Error: No se pudo activar el juego")

    def activar_tablero(self):
        """
        Activa el tablero reemplazando las celdas blancas (Labels visuales)
        por Buttons interactivos que permiten colocar números del jugador.
        Solo afecta a las celdas blancas simples, no toca celdas negras ni con claves.
        """
        print("Activando tablero: convirtiendo Labels a Buttons interactivos...")
        
        # Recorrer la matriz de celdas blancas
        for fila in range(9):
            for columna in range(9):
                celda = self.celdas_blancas[fila][columna]
                
                # Verificar que la celda existe y es un Label (celda blanca simple)
                if celda and isinstance(celda, tk.Label):
                    # Reemplazar el Label por un Button interactivo
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
                    
                    print(f"Celda interactiva creada en ({fila+1}, {columna+1}): Label → Button")
        
        print("Tablero activado: todas las celdas blancas ahora son interactivas")

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
                # Si no se pudo cargar la partida, mostrar error
                self.show_error_message("No se pudo cargar una partida válida para el nivel actual.")
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
        if not self.partida_data:
            return
            
        # Crear matriz para almacenar referencias a las celdas blancas
        # Por ahora todas las celdas blancas están bloqueadas (solo visuales)
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
        
        # Paso 2: Sobreescribir posiciones según las claves del juego
        self.apply_game_claves()
        
        print(f"Tablero 9x9 construido con {len(self.partida_data['claves'])} claves")

    def apply_game_claves(self):
        """
        Aplica las claves del juego al tablero, sobreescribiendo las celdas blancas
        con celdas negras o celdas con claves según corresponda.
        """
        for clave in self.partida_data["claves"]:
            fila = clave["fila"] - 1  # Convertir a índice base 0
            columna = clave["columna"] - 1
            tipo_clave = clave["tipo_de_clave"]
            valor_clave = clave["clave"]
            casillas = clave["casillas"]
            
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
        """
        Activa todos los botones de acción del juego.
        Este método se ejecuta cuando el juego se inicia para habilitar
        las acciones disponibles durante el juego activo.
        """
        print("Activando botones de acción del juego...")
        
        # Activar todos los botones de acción
        for boton in self.botones_accion:
            boton.config(state="normal")
        
        print(f"✓ {len(self.botones_accion)} botones de acción activados")
        print("Botones disponibles: DESHACER JUGADA, REHACER JUGADA, BORRAR CASILLA, GUARDAR JUEGO, TERMINAR JUEGO")

    def activar_botones_numeros(self):
        """
        Activa todos los botones numéricos del panel lateral.
        Este método se ejecuta cuando el juego se inicia para habilitar
        la selección de números durante el juego activo.
        """
        print("Activando botones numéricos...")
        
        # Activar todos los botones numéricos
        for boton in self.botones_numeros:
            boton.config(state="normal")
        
        print(f"✓ {len(self.botones_numeros)} botones numéricos activados")
        print("Botones numéricos disponibles: 1-9")

    def seleccionar_numero(self, numero):
        """
        Método para seleccionar un número para colocar en el tablero.
        Resalta el botón seleccionado y desresalta los demás.
        
        Args:
            numero (int): Número seleccionado por el jugador
        """
        # Asignar el número seleccionado
        self.numero_seleccionado = numero
        print(f"Número seleccionado: {numero}")
        
        # Recorrer todos los botones numéricos y resaltar solo el seleccionado
        for i, boton in enumerate(self.botones_numeros, 1):
            if i == numero:
                # Resaltar el botón seleccionado con color dorado
                boton.config(bg="#ffd700")
            else:
                # Mantener el color original para los demás botones
                boton.config(bg="#3a3a3a")
        
        print(f"Botón {numero} resaltado en dorado")

    def colocar_numero_en_celda(self, fila, columna):
        """
        Método para colocar un número en una celda blanca del tablero.
        Esta lógica permite colocar números en el tablero de juego.
        Requiere que el juego esté iniciado y que haya un número previamente seleccionado.
        
        Args:
            fila (int): Fila de la celda (0-8)
            columna (int): Columna de la celda (0-8)
        """
        # Verificar si el juego está activo
        if not self.juego_activo:
            print("El juego no está activo. No se puede colocar números.")
            return
        
        # Verificar si hay un número seleccionado
        if self.numero_seleccionado is None:
            try:
                messagebox.showwarning(
                    "Kakuro 2025", 
                    "Por favor, selecciona un número del panel numérico antes de colocarlo en el tablero."
                )
            except Exception as e:
                print(f"Error al mostrar mensaje de advertencia: {e}")
            print("No hay número seleccionado. Selecciona un número del panel numérico.")
            return
        
        # Obtener la celda correspondiente
        celda = self.celdas_blancas[fila][columna]
        
        # Verificar que la celda existe y es un Button
        if celda and isinstance(celda, tk.Button):
            # ✅ Capturar el valor actual antes de colocar el nuevo número
            valor_actual = self.estado_tablero[fila][columna]
            
            # ✅ Solo registrar la jugada si el valor realmente cambió
            if self.numero_seleccionado != valor_actual:
                # Registrar la jugada en el historial
                self.historial_jugadas.append({
                    "fila": fila,
                    "columna": columna,
                    "valor_anterior": valor_actual,
                    "valor_nuevo": self.numero_seleccionado
                })
                # Limpiar el historial de rehacer cuando se hace una nueva jugada
                self.historial_rehacer.clear()
                
                print(f"Jugada registrada: ({fila+1}, {columna+1}) {valor_actual} → {self.numero_seleccionado}")
            
            # Actualizar el texto del botón (la celda) con el número seleccionado
            celda.config(text=str(self.numero_seleccionado))
            
            # Actualizar la matriz de estado del tablero
            self.estado_tablero[fila][columna] = self.numero_seleccionado
            
            print(f"Número {self.numero_seleccionado} colocado en celda ({fila+1}, {columna+1})")
            print(f"Estado del tablero actualizado: fila {fila+1}, columna {columna+1} = {self.numero_seleccionado}")
        else:
            print(f"Error: No se pudo colocar número en celda ({fila+1}, {columna+1})")

    def deshacer_jugada(self):
        """
        🔁 Método para deshacer la última jugada realizada.
        Toma la última jugada del historial y revierte el valor en la celda correspondiente.
        """
        if not self.historial_jugadas:
            messagebox.showinfo("Deshacer", "No hay jugadas para deshacer.")
            return

        # Obtener la última jugada del historial
        jugada = self.historial_jugadas.pop()
        fila = jugada["fila"]
        columna = jugada["columna"]
        valor_anterior = jugada["valor_anterior"]

        # Revertir el valor en la celda
        celda = self.celdas_blancas[fila][columna]
        celda.config(text=str(valor_anterior) if valor_anterior else "")
        self.estado_tablero[fila][columna] = valor_anterior

        # Guardar esta jugada en el historial de rehacer
        self.historial_rehacer.append(jugada)

        print(f"Jugada deshecha: ({fila+1}, {columna+1}) → {valor_anterior}")
        print(f"Historial de jugadas: {len(self.historial_jugadas)} restantes")
        print(f"Historial de rehacer: {len(self.historial_rehacer)} disponibles")

    def rehacer_jugada(self):
        """
        🔁 Método para rehacer la última jugada deshecha.
        Toma la última jugada del historial de rehacer y vuelve a aplicarla.
        """
        if not self.historial_rehacer:
            messagebox.showinfo("Rehacer", "No hay jugadas para rehacer.")
            return

        # Obtener la última jugada del historial de rehacer
        jugada = self.historial_rehacer.pop()
        fila = jugada["fila"]
        columna = jugada["columna"]
        valor_nuevo = jugada["valor_nuevo"]

        # Reaplicar el valor en la celda
        celda = self.celdas_blancas[fila][columna]
        celda.config(text=str(valor_nuevo))
        self.estado_tablero[fila][columna] = valor_nuevo

        # Volver a registrar esta jugada en el historial principal
        self.historial_jugadas.append(jugada)

        print(f"Jugada rehecha: ({fila+1}, {columna+1}) → {valor_nuevo}")
        print(f"Historial de jugadas: {len(self.historial_jugadas)} disponibles")
        print(f"Historial de rehacer: {len(self.historial_rehacer)} restantes")

    def verificar_tablero(self):
        """
        🧮 Método para verificar si el tablero está completo y todas las claves numéricas se cumplen.
        
        Returns:
            bool: True si el tablero está correcto, False si hay errores
        """
        if not self.juego_activo:
            messagebox.showwarning("Validación", "El juego no está activo.")
            return False

        if not self.partida_data:
            messagebox.showerror("Error", "No hay datos de partida cargados.")
            return False

        print("🔍 Iniciando verificación del tablero...")

        # Paso 1: Validar que todas las celdas blancas estén completas
        print("Paso 1: Verificando que todas las celdas estén completas...")
        for fila in range(9):
            for col in range(9):
                celda = self.estado_tablero[fila][col]
                if celda is None:
                    print(f"❌ Celda vacía en fila {fila+1}, columna {col+1}")
                    messagebox.showwarning("Tablero Incompleto", f"Hay celdas vacías en el tablero.")
                    return False

        print("✅ Todas las celdas están completas")

        # Paso 2: Validar claves de filas y columnas
        print("Paso 2: Verificando claves de filas y columnas...")
        claves = self.partida_data.get("claves", [])
        
        if not claves:
            print("⚠️ No hay claves para validar")
            messagebox.showinfo("Sin Claves", "No hay claves para validar en esta partida.")
            return True

        for clave in claves:
            tipo = clave["tipo_de_clave"]
            fila = clave["fila"] - 1  # Convertir a índice base 0
            columna = clave["columna"] - 1
            esperado = clave["clave"]
            casillas = clave["casillas"]

            suma_real = 0
            valores_vistos = set()

            try:
                if tipo == "F":  # Clave de Fila
                    print(f"Validando clave de fila en ({fila+1}, {columna+1}): esperado={esperado}, casillas={casillas}")
                    for offset in range(1, casillas + 1):
                        valor = self.estado_tablero[fila][columna + offset]
                        if valor in valores_vistos:
                            print(f"❌ Valor duplicado {valor} en clave de fila ({fila+1}, {columna+1})")
                            messagebox.showwarning("Error de Validación", f"Valor duplicado {valor} en la clave de fila.")
                            return False
                        if not (1 <= valor <= 9):
                            print(f"❌ Valor fuera de rango {valor} en clave de fila ({fila+1}, {columna+1})")
                            messagebox.showwarning("Error de Validación", f"Valor fuera de rango {valor} en la clave de fila.")
                            return False
                        valores_vistos.add(valor)
                        suma_real += valor

                elif tipo == "C":  # Clave de Columna
                    print(f"Validando clave de columna en ({fila+1}, {columna+1}): esperado={esperado}, casillas={casillas}")
                    for offset in range(1, casillas + 1):
                        valor = self.estado_tablero[fila + offset][columna]
                        if valor in valores_vistos:
                            print(f"❌ Valor duplicado {valor} en clave de columna ({fila+1}, {columna+1})")
                            messagebox.showwarning("Error de Validación", f"Valor duplicado {valor} en la clave de columna.")
                            return False
                        if not (1 <= valor <= 9):
                            print(f"❌ Valor fuera de rango {valor} en clave de columna ({fila+1}, {columna+1})")
                            messagebox.showwarning("Error de Validación", f"Valor fuera de rango {valor} en la clave de columna.")
                            return False
                        valores_vistos.add(valor)
                        suma_real += valor

            except IndexError as e:
                print(f"❌ Error de índice al validar claves: {e}")
                messagebox.showerror("Error de Validación", "Error de índice al validar las claves del tablero.")
                return False

            if suma_real != esperado:
                print(f"❌ Clave incorrecta en ({fila+1},{columna+1}) tipo {tipo}: esperada={esperado}, actual={suma_real}")
                messagebox.showwarning("Error de Validación", f"Clave incorrecta en ({fila+1},{columna+1}): esperada={esperado}, actual={suma_real}")
                return False
            else:
                print(f"✅ Clave {tipo} en ({fila+1},{columna+1}): {suma_real} = {esperado}")

        print("✅ Tablero validado correctamente.")
        messagebox.showinfo("¡Felicidades!", "¡El tablero está completo y todas las claves son correctas!")
        return True

    def terminar_juego(self):
        """
        🎮 Método para terminar el juego y verificar el tablero.
        Este método se ejecuta cuando el usuario hace clic en "TERMINAR JUEGO".
        """
        print("🎯 Iniciando verificación del juego...")
        
        if self.verificar_tablero():
            print("🎉 ¡Juego terminado y tablero validado correctamente!")
            
            # Guardar récord si el juego fue ganado correctamente
            self.guardar_record_juego()
            
            # Mensaje final con nombre y tiempo
            nivel = self.partida_data.get("nivel_de_dificultad", "FÁCIL")
            tiempo_inicial = getattr(self, 'tiempo_inicial', 30*60)
            tiempo_usado = tiempo_inicial - getattr(self, 'tiempo_restante', 0)
            msg = f"🎉 ¡Felicidades {self.nombre_jugador}!\nCompletaste el juego en {tiempo_usado} segundos."
            messagebox.showinfo("¡Juego completado!", msg)
            print(f"[GAME] {self.nombre_jugador} terminó el juego con éxito en nivel {nivel} - tiempo usado: {tiempo_usado}")
        else:
            print("⚠️ Juego terminado pero el tablero no es válido")

    def guardar_record_juego(self):
        """
        🏆 Guarda el récord del jugador si el juego fue completado correctamente.
        Solo se guarda si hay un reloj activo y el juego fue ganado.
        """
        print("🏆 Verificando si se debe guardar récord...")
        
        if not hasattr(self, 'tiempo_restante') or self.tiempo_restante is None:
            print("[RECORDS] No hay reloj activo, no se guarda récord")
            return
        
        if self.partida_data.get("reloj", "SIN RELOJ") == "SIN RELOJ":
            print("[RECORDS] Modo sin reloj, no se guarda récord")
            return
        
        nombre_jugador = self.nombre_jugador
        tiempo_inicial = getattr(self, 'tiempo_inicial', 30*60)
        tiempo_usado = tiempo_inicial - self.tiempo_restante
        nivel = self.partida_data.get("nivel_de_dificultad", "FÁCIL")
        print(f"[RECORDS] Guardando récord: {nombre_jugador} - Nivel {nivel} - Tiempo {formatear_tiempo(tiempo_usado)}")
        
        if guardar_record(nombre_jugador, nivel, tiempo_usado):
            messagebox.showinfo("🏆 ¡Nuevo Récord!", f"¡Felicidades {nombre_jugador}!\nHas completado el nivel {nivel} en {formatear_tiempo(tiempo_usado)}")
        else:
            print("[RECORDS] Error al guardar el récord")

    def ver_records(self):
        """
        🏆 Muestra los mejores récords para el nivel actual.
        """
        print("🏆 Mostrando récords...")
        
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
        """
        💾 Método para guardar el estado actual del juego en un archivo JSON.
        Este método se ejecuta cuando el usuario hace clic en "GUARDAR JUEGO".
        
        Guarda:
        - El contenido de self.estado_tablero
        - Nivel de dificultad
        - Claves de la partida
        - Tiempo restante (si aplica)
        - Información adicional del juego
        """
        import json
        import os
        
        print("💾 Iniciando guardado de la partida actual...")
        
        if not self.juego_activo:
            messagebox.showwarning("Guardar Juego", "No hay una partida activa para guardar.")
            return

        if not self.partida_data:
            messagebox.showerror("Error", "No hay datos de partida cargados.")
            return

        try:
            # Preparar los datos para guardar
            datos_guardado = {
                "nivel": self.partida_data.get("nivel_de_dificultad", "FÁCIL"),
                "partida": self.partida_data.get("partida", 1),
                "tablero": self.estado_tablero,
                "claves": self.partida_data.get("claves", []),
                "reloj": self.partida_data.get("reloj", "SIN RELOJ"),
                "tiempo_restante": {
                    "horas": getattr(self, "tiempo_restante_horas", 0),
                    "minutos": getattr(self, "tiempo_restante_minutos", 0),
                    "segundos": getattr(self, "tiempo_restante_segundos", 0)
                },
                "fecha_guardado": "2025-01-01",  # Se puede implementar datetime después
                "jugador": self.name_entry.get() if hasattr(self, 'name_entry') else "Jugador",
                "historial_jugadas": len(self.historial_jugadas),
                "historial_rehacer": len(self.historial_rehacer)
            }

            # Si hay un reloj activo, guardar el tiempo restante actual
            if hasattr(self, 'tiempo_restante') and self.tiempo_restante is not None:
                horas_restantes = self.tiempo_restante // 3600
                minutos_restantes = (self.tiempo_restante % 3600) // 60
                segundos_restantes = self.tiempo_restante % 60
                
                datos_guardado["tiempo_restante"] = {
                    "horas": horas_restantes,
                    "minutos": minutos_restantes,
                    "segundos": segundos_restantes
                }
                
                print(f"[LOG] Tiempo restante guardado: {horas_restantes:02}:{minutos_restantes:02}:{segundos_restantes:02}")

            # Crear el directorio data si no existe
            os.makedirs("data", exist_ok=True)
            
            # Guardar en el archivo JSON
            archivo_guardado = "data/kakuro2025_guardado.json"
            with open(archivo_guardado, "w", encoding="utf-8") as f:
                json.dump(datos_guardado, f, indent=4, ensure_ascii=False)

            messagebox.showinfo("Guardar Juego", "✅ Partida guardada exitosamente.")
            print(f"[LOG] Partida guardada en {archivo_guardado}")
            print(f"[LOG] Nivel: {datos_guardado['nivel']}")
            print(f"[LOG] Jugador: {datos_guardado['jugador']}")
            print(f"[LOG] Celdas llenas: {sum(1 for fila in self.estado_tablero for celda in fila if celda is not None)}/81")

        except Exception as e:
            print(f"[ERROR] No se pudo guardar la partida: {e}")
            messagebox.showerror("Guardar Juego", f"❌ Error al guardar la partida: {str(e)}")

    def cargar_partida_guardada(self):
        """
        📂 Método para cargar una partida guardada desde data/kakuro2025_guardado.json
        y restaurar la partida completa en el tablero.
        
        Restaura:
        - El estado del tablero (self.estado_tablero)
        - Nivel de dificultad y claves
        - Tiempo restante (si hay)
        - Información del jugador
        - Historial de jugadas
        """
        import json
        import os
        
        print("📂 Iniciando carga de partida guardada...")
        
        ruta = "data/kakuro2025_guardado.json"

        if not os.path.exists(ruta):
            messagebox.showwarning("Cargar Partida", "No hay partida guardada disponible.")
            print(f"[WARNING] Archivo no encontrado: {ruta}")
            return

        try:
            # Leer el archivo guardado
            with open(ruta, "r", encoding="utf-8") as f:
                partida = json.load(f)

            print(f"[LOG] Archivo cargado: {ruta}")
            print(f"[LOG] Nivel: {partida.get('nivel', 'FÁCIL')}")
            print(f"[LOG] Jugador: {partida.get('jugador', 'Desconocido')}")

            # Paso 1: Restaurar estado del juego
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
                
                # Calcular tiempo total en segundos
                self.tiempo_restante = horas * 3600 + minutos * 60 + segundos
                
                print(f"[LOG] Tiempo restante restaurado: {horas:02}:{minutos:02}:{segundos:02} ({self.tiempo_restante} segundos)")
            else:
                self.tiempo_restante = None

            # Restaurar información adicional
            if hasattr(self, 'name_entry') and partida.get("jugador"):
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, partida.get("jugador"))

            # Restaurar historial de jugadas (opcional)
            historial_jugadas_count = partida.get("historial_jugadas", 0)
            historial_rehacer_count = partida.get("historial_rehacer", 0)
            
            # Limpiar historiales existentes
            self.historial_jugadas.clear()
            self.historial_rehacer.clear()
            
            print(f"[LOG] Historial restaurado: {historial_jugadas_count} jugadas, {historial_rehacer_count} rehacer")

            # Paso 2: Borrar tablero anterior y recrearlo
            print("Paso 2: Reconstruyendo tablero...")
            for widget in self.board_frame.winfo_children():
                widget.destroy()

            self.build_dynamic_board()         # Reconstruye 9x9 celdas blancas
            self.apply_game_claves()           # Aplica claves guardadas
            self.activar_tablero()             # Hace celdas interactivas

            # Paso 3: Volver a insertar los valores guardados en la UI
            print("Paso 3: Restaurando valores en el tablero...")
            celdas_restauradas = 0
            for fila in range(9):
                for col in range(9):
                    valor = self.estado_tablero[fila][col]
                    if isinstance(valor, int) and 1 <= valor <= 9:
                        celda = self.celdas_blancas[fila][col]
                        if isinstance(celda, tk.Button):
                            celda.config(text=str(valor))
                            celdas_restauradas += 1

            print(f"[LOG] Celdas restauradas: {celdas_restauradas}")

            # Paso 4: Activar panel numérico y botones
            print("Paso 4: Activando interfaz de juego...")
            self.juego_activo = True
            self.activar_botones()
            self.activar_botones_numeros()
            
            # Desactivar botón de iniciar juego
            if hasattr(self, 'boton_iniciar'):
                self.boton_iniciar.config(state="disabled")

            # Mostrar información de la partida cargada
            nivel_actual = self.partida_data["nivel_de_dificultad"]
            print(f"[LOG] Partida cargada: Nivel {nivel_actual}, {celdas_restauradas} celdas llenas")

            messagebox.showinfo("Cargar Juego", f"✅ Partida restaurada correctamente.\nNivel: {nivel_actual}\nCeldas llenas: {celdas_restauradas}/81")
            print("[LOG] Partida cargada con éxito desde JSON.")

            # Configurar el reloj
            self.setup_reloj()

        except json.JSONDecodeError as e:
            print(f"[ERROR] Error al decodificar JSON: {e}")
            messagebox.showerror("Cargar Juego", "❌ Error al leer el archivo guardado (formato inválido).")
        except Exception as e:
            print(f"[ERROR] Error al cargar partida: {e}")
            messagebox.showerror("Cargar Juego", f"❌ Error al cargar la partida: {str(e)}")

    def setup_reloj(self):
        """
        ⏱️ Configura el reloj si la partida lo requiere.
        Muestra el temporizador visual en pantalla.
        """
        print("[RELOJ] Configurando temporizador...")
        
        # Verificar si la partida requiere reloj
        if not self.partida_data:
            print("[RELOJ] No hay datos de partida. No se inicializa temporizador.")
            return
            
        reloj_config = self.partida_data.get("reloj", "SIN RELOJ")
        if reloj_config == "SIN RELOJ":
            print("[RELOJ] Modo sin reloj. No se inicializa temporizador.")
            return

        # Obtener tiempo inicial desde la configuración o usar valores por defecto
        horas = self.partida_data.get("horas", 0)
        minutos = self.partida_data.get("minutos", 30)  # 30 minutos por defecto
        segundos = self.partida_data.get("segundos", 0)
        
        # Calcular tiempo total en segundos
        self.tiempo_restante = horas * 3600 + minutos * 60 + segundos
        
        print(f"[RELOJ] Tiempo inicial configurado: {horas:02}:{minutos:02}:{segundos:02} ({self.tiempo_restante} segundos)")

        # Crear widget visual del reloj si no existe
        if not hasattr(self, "reloj_label"):
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

        # Iniciar el contador
        self.actualizar_reloj()
        print("[RELOJ] Temporizador iniciado")

    def actualizar_reloj(self):
        """
        ⏱️ Disminuye el tiempo restante y actualiza el label visual.
        Finaliza el juego si llega a cero.
        """
        if not self.juego_activo or not hasattr(self, 'tiempo_restante') or self.tiempo_restante is None:
            return

        # Calcular horas, minutos y segundos restantes
        horas = self.tiempo_restante // 3600
        minutos = (self.tiempo_restante % 3600) // 60
        segundos = self.tiempo_restante % 60

        # Formatear tiempo para mostrar
        tiempo_str = f"⏳ Tiempo restante: {horas:02}:{minutos:02}:{segundos:02}"
        
        # Cambiar color según el tiempo restante
        if self.tiempo_restante <= 300:  # 5 minutos o menos
            color = "#ff0000"  # Rojo
        elif self.tiempo_restante <= 600:  # 10 minutos o menos
            color = "#ff6b6b"  # Rojo claro
        else:
            color = "#ffffff"  # Blanco
        
        if hasattr(self, 'reloj_label'):
            self.reloj_label.config(text=tiempo_str, fg=color)

        # Verificar si el tiempo se agotó
        if self.tiempo_restante <= 0:
            print("[RELOJ] ⏱️ Tiempo agotado!")
            messagebox.showinfo("⏱️ Tiempo agotado", "El tiempo ha terminado. El juego se finalizará automáticamente.")
            self.terminar_juego()
            return

        # Decrementar tiempo y programar próxima actualización
        self.tiempo_restante -= 1
        self.after(1000, self.actualizar_reloj)  # Actualizar cada segundo
