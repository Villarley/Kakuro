"""
Pantalla de configuración del juego Kakuro 2025.
Permite configurar el tipo de reloj, nivel de dificultad y tiempo límite.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

CONFIG_FILE = "data/configuracion.json"


class ConfigScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#2c2c2c")
        self.controller = controller
        self.setup_ui()
        self.load_current_config()

    def setup_ui(self):
        """Configura la interfaz de usuario de la pantalla de configuración"""
        
        # Título principal
        title = tk.Label(
            self, 
            text="⚙️ CONFIGURACIÓN DE JUEGO", 
            font=("Segoe UI", 24, "bold"), 
            fg="#ffcc80", 
            bg="#2c2c2c"
        )
        title.pack(pady=30)

        # Frame principal para las opciones
        main_frame = tk.Frame(self, bg="#2c2c2c")
        main_frame.pack(pady=20)

        # 1. Nivel de dificultad
        self._create_difficulty_section(main_frame)
        
        # Separador
        separator1 = tk.Frame(main_frame, height=2, bg="#444444")
        separator1.pack(fill="x", pady=20)

        # 2. Tipo de reloj
        self._create_clock_section(main_frame)
        
        # Separador
        separator2 = tk.Frame(main_frame, height=2, bg="#444444")
        separator2.pack(fill="x", pady=20)

        # 3. Tiempo límite (para TEMPORIZADOR)
        self._create_time_limit_section(main_frame)

        # Frame para botones
        button_frame = tk.Frame(self, bg="#2c2c2c")
        button_frame.pack(pady=30)

        # Botón guardar configuración
        save_btn = tk.Button(
            button_frame,
            text="💾 GUARDAR CONFIGURACIÓN",
            font=("Segoe UI", 12, "bold"),
            bg="#4caf50",
            fg="white",
            width=25,
            height=2,
            command=self.guardar_config
        )
        save_btn.pack(pady=10)

        # Botón volver al menú principal
        back_btn = tk.Button(
            button_frame,
            text="🔙 VOLVER AL MENÚ",
            font=("Segoe UI", 12, "bold"),
            bg="#ff5722",
            fg="white",
            width=25,
            height=2,
            command=lambda: self.controller.show_frame("HomeScreen")
        )
        back_btn.pack(pady=10)

    def _create_difficulty_section(self, parent):
        """Crea la sección de nivel de dificultad"""
        # Título de sección
        section_title = tk.Label(
            parent,
            text="🎯 NIVEL DE DIFICULTAD",
            font=("Segoe UI", 16, "bold"),
            fg="white",
            bg="#2c2c2c"
        )
        section_title.pack(pady=10)

        # Descripción
        description = tk.Label(
            parent,
            text="Selecciona el nivel de dificultad para las partidas:",
            font=("Segoe UI", 10),
            fg="#cccccc",
            bg="#2c2c2c"
        )
        description.pack()

        # Combobox para nivel
        self.nivel_var = tk.StringVar(value="FÁCIL")
        nivel_combo = ttk.Combobox(
            parent, 
            textvariable=self.nivel_var, 
            values=["FÁCIL", "MEDIO", "DIFÍCIL"], 
            state="readonly",
            font=("Segoe UI", 12),
            width=20
        )
        nivel_combo.pack(pady=10)

        # Información de cada nivel
        info_text = """
        • FÁCIL: Puzzles simples con pocas claves
        • MEDIO: Puzzles moderados con claves variadas  
        • DIFÍCIL: Puzzles complejos con muchas claves
        """
        info_label = tk.Label(
            parent,
            text=info_text,
            font=("Segoe UI", 9),
            fg="#aaaaaa",
            bg="#2c2c2c",
            justify="left"
        )
        info_label.pack(pady=5)

    def _create_clock_section(self, parent):
        """Crea la sección de tipo de reloj"""
        # Título de sección
        section_title = tk.Label(
            parent,
            text="⏱️ TIPO DE RELOJ",
            font=("Segoe UI", 16, "bold"),
            fg="white",
            bg="#2c2c2c"
        )
        section_title.pack(pady=10)

        # Descripción
        description = tk.Label(
            parent,
            text="Elige cómo quieres que funcione el temporizador:",
            font=("Segoe UI", 10),
            fg="#cccccc",
            bg="#2c2c2c"
        )
        description.pack()

        # Combobox para tipo de reloj
        self.reloj_var = tk.StringVar(value="CRONÓMETRO")
        reloj_combo = ttk.Combobox(
            parent, 
            textvariable=self.reloj_var, 
            values=["SIN RELOJ", "CRONÓMETRO", "TEMPORIZADOR"], 
            state="readonly",
            font=("Segoe UI", 12),
            width=20
        )
        reloj_combo.pack(pady=10)
        reloj_combo.bind("<<ComboboxSelected>>", self.toggle_time_entry)

        # Información de cada tipo
        clock_info = """
        • SIN RELOJ: Juego sin límite de tiempo
        • CRONÓMETRO: Cuenta el tiempo transcurrido
        • TEMPORIZADOR: Cuenta hacia atrás desde un límite
        """
        clock_info_label = tk.Label(
            parent,
            text=clock_info,
            font=("Segoe UI", 9),
            fg="#aaaaaa",
            bg="#2c2c2c",
            justify="left"
        )
        clock_info_label.pack(pady=5)

    def _create_time_limit_section(self, parent):
        """Crea la sección de tiempo límite"""
        # Frame para tiempo límite
        self.time_frame = tk.Frame(parent, bg="#2c2c2c")
        self.time_frame.pack(pady=10)

        # Título de sección
        section_title = tk.Label(
            self.time_frame,
            text="⏳ TIEMPO LÍMITE",
            font=("Segoe UI", 16, "bold"),
            fg="white",
            bg="#2c2c2c"
        )
        section_title.pack(pady=10)

        # Descripción
        description = tk.Label(
            self.time_frame,
            text="Configura el tiempo límite para el temporizador:",
            font=("Segoe UI", 10),
            fg="#cccccc",
            bg="#2c2c2c"
        )
        description.pack()

        # Frame para entrada de tiempo
        time_input_frame = tk.Frame(self.time_frame, bg="#2c2c2c")
        time_input_frame.pack(pady=10)

        # Horas
        tk.Label(
            time_input_frame,
            text="Horas:",
            fg="white",
            bg="#2c2c2c",
            font=("Segoe UI", 10)
        ).grid(row=0, column=0, padx=5)
        
        self.horas_var = tk.StringVar(value="0")
        self.horas_entry = tk.Entry(
            time_input_frame,
            textvariable=self.horas_var,
            width=5,
            font=("Segoe UI", 12),
            justify="center"
        )
        self.horas_entry.grid(row=0, column=1, padx=5)

        # Minutos
        tk.Label(
            time_input_frame,
            text="Minutos:",
            fg="white",
            bg="#2c2c2c",
            font=("Segoe UI", 10)
        ).grid(row=0, column=2, padx=5)
        
        self.minutos_var = tk.StringVar(value="30")
        self.minutos_entry = tk.Entry(
            time_input_frame,
            textvariable=self.minutos_var,
            width=5,
            font=("Segoe UI", 12),
            justify="center"
        )
        self.minutos_entry.grid(row=0, column=3, padx=5)

        # Segundos
        tk.Label(
            time_input_frame,
            text="Segundos:",
            fg="white",
            bg="#2c2c2c",
            font=("Segoe UI", 10)
        ).grid(row=0, column=4, padx=5)
        
        self.segundos_var = tk.StringVar(value="0")
        self.segundos_entry = tk.Entry(
            time_input_frame,
            textvariable=self.segundos_var,
            width=5,
            font=("Segoe UI", 12),
            justify="center"
        )
        self.segundos_entry.grid(row=0, column=5, padx=5)

        # Información adicional
        info_text = """
        ⚠️ Solo se usa cuando el tipo de reloj es "TEMPORIZADOR"
        💡 Recomendado: 30 minutos para principiantes
        """
        info_label = tk.Label(
            self.time_frame,
            text=info_text,
            font=("Segoe UI", 9),
            fg="#ffcc80",
            bg="#2c2c2c",
            justify="left"
        )
        info_label.pack(pady=5)

        # Inicialmente ocultar la sección de tiempo
        self.time_frame.pack_forget()

    def toggle_time_entry(self, event=None):
        """Muestra u oculta la sección de tiempo límite según el tipo de reloj"""
        if self.reloj_var.get() == "TEMPORIZADOR":
            self.time_frame.pack(pady=10)
            print("[CONFIG] Sección de tiempo límite mostrada")
        else:
            self.time_frame.pack_forget()
            print("[CONFIG] Sección de tiempo límite ocultada")

    def load_current_config(self):
        """Carga la configuración actual desde el archivo"""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # Aplicar configuración cargada
                self.nivel_var.set(config.get("nivel", "FÁCIL"))
                self.reloj_var.set(config.get("tipo_reloj", "CRONÓMETRO"))
                
                # Configurar tiempo límite si existe
                if config.get("tipo_reloj") == "TEMPORIZADOR":
                    tiempo_limite = config.get("tiempo_limite", 1800)  # 30 min por defecto
                    horas = tiempo_limite // 3600
                    minutos = (tiempo_limite % 3600) // 60
                    segundos = tiempo_limite % 60
                    
                    self.horas_var.set(str(horas))
                    self.minutos_var.set(str(minutos))
                    self.segundos_var.set(str(segundos))
                
                print(f"[CONFIG] Configuración cargada: {config}")
            else:
                print("[CONFIG] No existe archivo de configuración, usando valores por defecto")
                
        except Exception as e:
            print(f"[CONFIG] Error al cargar configuración: {e}")
            messagebox.showerror("Error", f"Error al cargar la configuración:\n{str(e)}")

    def guardar_config(self):
        """Guarda la configuración actual en el archivo JSON"""
        try:
            # Validar entrada de tiempo si es temporizador
            if self.reloj_var.get() == "TEMPORIZADOR":
                try:
                    horas = int(self.horas_var.get())
                    minutos = int(self.minutos_var.get())
                    segundos = int(self.segundos_var.get())
                    
                    if horas < 0 or minutos < 0 or segundos < 0:
                        raise ValueError("Los valores de tiempo no pueden ser negativos")
                    
                    if minutos > 59 or segundos > 59:
                        raise ValueError("Minutos y segundos deben estar entre 0 y 59")
                    
                    # Calcular tiempo total en segundos
                    tiempo_limite = horas * 3600 + minutos * 60 + segundos
                    
                    if tiempo_limite == 0:
                        raise ValueError("El tiempo límite debe ser mayor a 0")
                        
                except ValueError as e:
                    messagebox.showerror("Error", f"Error en el tiempo límite:\n{str(e)}")
                    return

            # Preparar configuración
            config = {
                "nivel": self.nivel_var.get(),
                "tipo_reloj": self.reloj_var.get()
            }

            # Agregar tiempo límite si es temporizador
            if self.reloj_var.get() == "TEMPORIZADOR":
                config["tiempo_limite"] = tiempo_limite
                config["horas"] = horas
                config["minutos"] = minutos
                config["segundos"] = segundos

            # Crear directorio data si no existe
            os.makedirs("data", exist_ok=True)

            # Guardar en archivo
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4, ensure_ascii=False)

            # Mostrar mensaje de confirmación
            tiempo_str = ""
            if self.reloj_var.get() == "TEMPORIZADOR":
                tiempo_str = f"\n⏱️ Tiempo límite: {horas:02}:{minutos:02}:{segundos:02}"
            
            mensaje = f"✅ Configuración guardada exitosamente!\n\n" \
                     f"🎯 Nivel: {config['nivel']}\n" \
                     f"⏱️ Reloj: {config['tipo_reloj']}{tiempo_str}"
            
            messagebox.showinfo("Configuración Guardada", mensaje)
            print(f"[CONFIG] Configuración guardada: {config}")

        except Exception as e:
            print(f"[CONFIG] Error al guardar configuración: {e}")
            messagebox.showerror("Error", f"Error al guardar la configuración:\n{str(e)}")

    def get_current_config(self):
        """Obtiene la configuración actual sin guardar"""
        config = {
            "nivel": self.nivel_var.get(),
            "tipo_reloj": self.reloj_var.get()
        }
        
        if self.reloj_var.get() == "TEMPORIZADOR":
            try:
                horas = int(self.horas_var.get())
                minutos = int(self.minutos_var.get())
                segundos = int(self.segundos_var.get())
                tiempo_limite = horas * 3600 + minutos * 60 + segundos
                
                config["tiempo_limite"] = tiempo_limite
                config["horas"] = horas
                config["minutos"] = minutos
                config["segundos"] = segundos
            except ValueError:
                pass
        
        return config
