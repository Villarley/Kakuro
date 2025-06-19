# Kakuro 2025

Un juego de lógica Kakuro implementado en Python con interfaz gráfica usando Tkinter.

## Descripción

Kakuro es un juego de lógica matemática donde el objetivo es completar un tablero con números del 1 al 9 de manera que cada fila y columna sume el valor indicado, sin repetir números en la misma fila o columna.

## Características

- **Interfaz gráfica intuitiva** con Tkinter
- **Múltiples niveles de dificultad** (Fácil, Normal, Difícil)
- **Sistema de guardado** de partidas
- **Funciones de deshacer/rehacer** jugadas
- **Cronómetro opcional** para seguimiento del tiempo
- **Sistema de récords** para guardar mejores puntuaciones
- **Configuración personalizable** (tema, sonido, etc.)

## Requisitos

- Python 3.7 o superior
- Tkinter (incluido con Python en la mayoría de instalaciones)

### Instalación de Tkinter

Si Tkinter no está disponible en tu sistema:

#### En macOS:
```bash
# Si usas Homebrew
brew install python-tk

# Si usas pyenv
pyenv install 3.11.4 --enable-framework
```

#### En Ubuntu/Debian:
```bash
sudo apt-get install python3-tk
```

#### En CentOS/RHEL/Fedora:
```bash
sudo yum install python3-tkinter
# o
sudo dnf install python3-tkinter
```

#### En Windows:
Tkinter generalmente viene incluido con la instalación oficial de Python.

## Instalación

1. Clona o descarga este repositorio
2. Navega al directorio del proyecto:
   ```bash
   cd kakuro
   ```
3. Instala las dependencias (si las hay):
   ```bash
   pip install -r requirements.txt
   ```

## Cómo ejecutar

### Método 1: Ejecutar directamente
```bash
python main.py
```

### Método 2: Ejecutar con Python 3 específicamente
```bash
python3 main.py
```

### Método 3: Ejecutar como módulo
```bash
python -m main
```

### Verificar que Tkinter esté disponible
Antes de ejecutar, puedes verificar que Tkinter esté instalado:
```bash
python3 -c "import tkinter; print('Tkinter disponible:', tkinter.TkVersion)"
```

## Estructura del Proyecto

```
kakuro/
│
├── data/                    # Datos del juego (JSON)
│   ├── kakuro2025_partidas.json
│   ├── kakuro2025_récords.json
│   ├── kakuro2025_configuración.json
│   └── kakuro2025_juego_actual.json
│
├── gui/                     # Interfaz gráfica
│   ├── main_window.py       # Ventana principal
│   ├── game_screen.py       # Pantalla del juego
│   └── components.py        # Componentes reutilizables
│
├── logic/                   # Lógica del juego
│   ├── validator.py         # Validación de jugadas
│   ├── game_manager.py      # Manejo del estado
│   ├── pila_jugadas.py      # Deshacer/rehacer
│   └── partida_loader.py    # Carga de partidas
│
├── utils/                   # Utilidades
│   ├── file_manager.py      # Manejo de archivos
│   └── timer.py             # Cronómetro
│
├── docs/                    # Documentación
├── tests/                   # Pruebas unitarias
├── main.py                  # Script principal
├── README.md               # Este archivo
└── requirements.txt        # Dependencias
```

## Cómo jugar

1. **Selecciona un nivel** de dificultad
2. **Completa el tablero** con números del 1 al 9
3. **Asegúrate** de que cada fila y columna sume el valor indicado
4. **No repitas** números en la misma fila o columna
5. **Usa las funciones** de deshacer/rehacer si te equivocas
6. **Guarda tu progreso** cuando sea necesario

## Controles

- **Clic izquierdo**: Seleccionar celda
- **Teclas numéricas**: Insertar número
- **Backspace/Delete**: Borrar número
- **Ctrl+Z**: Deshacer jugada
- **Ctrl+Y**: Rehacer jugada

## Desarrollo

### Ejecutar pruebas
```bash
python -m unittest tests/test_validator.py
```

### Estructura de desarrollo
El proyecto está organizado en módulos separados para facilitar el mantenimiento y las pruebas:

- **gui/**: Contiene toda la lógica de interfaz de usuario
- **logic/**: Contiene la lógica del juego y validaciones
- **utils/**: Contiene utilidades y manejo de archivos
- **tests/**: Contiene las pruebas unitarias

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, asegúrate de:
1. Seguir el estilo de código existente
2. Añadir pruebas para nuevas funcionalidades
3. Actualizar la documentación según sea necesario

## Contacto

Para preguntas o sugerencias, por favor abre un issue en el repositorio. 