"""
Módulo para cargar la configuración del juego Kakuro desde archivo JSON.

Este módulo se encarga de leer el archivo de configuración del juego
y proporcionar valores por defecto en caso de que el archivo no exista
o esté incompleto.
"""

import json
import os
from typing import Dict, Any


def load_configuracion() -> Dict[str, Any]:
    """
    Carga la configuración del juego desde el archivo JSON.
    
    Intenta leer el archivo "data/kakuro2025_configuración.json" y devuelve
    la configuración del juego. Si el archivo no existe o está incompleto,
    devuelve valores por defecto.
    
    Returns:
        Dict[str, Any]: Diccionario con la configuración del juego.
            Estructura esperada:
            {
                "nivel": str,      # "FÁCIL", "MEDIO", "DIFÍCIL"
                "reloj": str,      # "SIN RELOJ", "TEMPORIZADOR"
                "horas": int,      # 0-23
                "minutos": int,    # 0-59
                "segundos": int    # 0-59
            }
    
    Example:
        >>> config = load_configuracion()
        >>> print(config["nivel"])
        "FÁCIL"
    """
    # Valores por defecto
    config_default = {
        "nivel": "FÁCIL",
        "reloj": "SIN RELOJ",
        "horas": 0,
        "minutos": 0,
        "segundos": 0
    }
    
    config_file_path = "data/kakuro2025_configuración.json"
    
    try:
        # Verificar si el archivo existe
        if not os.path.exists(config_file_path):
            return config_default
        
        # Leer el archivo JSON
        with open(config_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Intentar extraer la configuración del juego
        # Primero intentamos la estructura esperada
        if isinstance(data, dict):
            # Buscar configuración en diferentes posibles ubicaciones
            config = None
            
            # Estructura esperada: {"nivel": "...", "reloj": "...", ...}
            if all(key in data for key in ["nivel", "reloj"]):
                config = data
            # Estructura alternativa: {"configuracion": {...}}
            elif "configuracion" in data and isinstance(data["configuracion"], dict):
                config = data["configuracion"]
            
            if config:
                # Validar y extraer cada campo con valores por defecto
                result = {}
                
                # Nivel
                result["nivel"] = config.get("nivel", config_default["nivel"])
                if result["nivel"] not in ["FÁCIL", "MEDIO", "DIFÍCIL"]:
                    result["nivel"] = config_default["nivel"]
                
                # Reloj
                result["reloj"] = config.get("reloj", config_default["reloj"])
                if result["reloj"] not in ["SIN RELOJ", "TEMPORIZADOR"]:
                    result["reloj"] = config_default["reloj"]
                
                # Tiempo (horas, minutos, segundos)
                result["horas"] = config.get("horas", config_default["horas"])
                if not isinstance(result["horas"], int) or result["horas"] < 0 or result["horas"] > 23:
                    result["horas"] = config_default["horas"]
                
                result["minutos"] = config.get("minutos", config_default["minutos"])
                if not isinstance(result["minutos"], int) or result["minutos"] < 0 or result["minutos"] > 59:
                    result["minutos"] = config_default["minutos"]
                
                result["segundos"] = config.get("segundos", config_default["segundos"])
                if not isinstance(result["segundos"], int) or result["segundos"] < 0 or result["segundos"] > 59:
                    result["segundos"] = config_default["segundos"]
                
                return result
        
        # Si no se pudo extraer la configuración, devolver valores por defecto
        return config_default
        
    except (json.JSONDecodeError, IOError, OSError) as e:
        # En caso de error al leer o parsear el archivo, devolver valores por defecto
        print(f"Error al cargar la configuración: {e}")
        return config_default
    except Exception as e:
        # Capturar cualquier otro error inesperado
        print(f"Error inesperado al cargar la configuración: {e}")
        return config_default


if __name__ == "__main__":
    # Código de prueba para verificar el funcionamiento
    config = load_configuracion()
    print("Configuración cargada:")
    for key, value in config.items():
        print(f"  {key}: {value}") 