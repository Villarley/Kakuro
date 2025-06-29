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
    
    Intenta leer el archivo "data/configuracion.json" y devuelve
    la configuración del juego. Si el archivo no existe o está incompleto,
    devuelve valores por defecto.
    
    Returns:
        Dict[str, Any]: Diccionario con la configuración del juego.
            Estructura esperada:
            {
                "nivel": str,           # "FÁCIL", "MEDIO", "DIFÍCIL"
                "tipo_reloj": str,      # "SIN RELOJ", "CRONÓMETRO", "TEMPORIZADOR"
                "tiempo_limite": int,   # Tiempo en segundos (solo para TEMPORIZADOR)
                "horas": int,           # 0-23
                "minutos": int,         # 0-59
                "segundos": int         # 0-59
            }
    
    Example:
        >>> config = load_configuracion()
        >>> print(config["nivel"])
        "FÁCIL"
    """
    # Valores por defecto
    config_default = {
        "nivel": "FÁCIL",
        "tipo_reloj": "CRONÓMETRO",
        "tiempo_limite": 1800,  # 30 minutos por defecto
        "horas": 0,
        "minutos": 30,
        "segundos": 0
    }
    
    # Intentar diferentes rutas de archivo
    config_file_paths = [
        "data/configuracion.json",
        "data/kakuro2025_configuración.json",
        "data/kakuro2025_configuracion.json"
    ]
    
    for config_file_path in config_file_paths:
        try:
            # Verificar si el archivo existe
            if not os.path.exists(config_file_path):
                continue
            
            # Leer el archivo JSON
            with open(config_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            
            print(f"[CONFIG] Archivo cargado: {config_file_path}")
            
            # Validar que data es un diccionario
            if not isinstance(data, dict):
                continue
            
            # Extraer configuración
            result = {}
            
            # Nivel de dificultad
            result["nivel"] = data.get("nivel", config_default["nivel"])
            if result["nivel"] not in ["FÁCIL", "MEDIO", "DIFÍCIL"]:
                result["nivel"] = config_default["nivel"]
            
            # Tipo de reloj (nueva estructura)
            result["tipo_reloj"] = data.get("tipo_reloj", config_default["tipo_reloj"])
            if result["tipo_reloj"] not in ["SIN RELOJ", "CRONÓMETRO", "TEMPORIZADOR"]:
                result["tipo_reloj"] = config_default["tipo_reloj"]
            
            # Compatibilidad con estructura antigua
            if "reloj" in data and "tipo_reloj" not in data:
                old_reloj = data.get("reloj")
                if old_reloj == "SIN RELOJ":
                    result["tipo_reloj"] = "SIN RELOJ"
                elif old_reloj == "TEMPORIZADOR":
                    result["tipo_reloj"] = "TEMPORIZADOR"
                else:
                    result["tipo_reloj"] = "CRONÓMETRO"
            
            # Tiempo límite (para temporizador)
            result["tiempo_limite"] = data.get("tiempo_limite", config_default["tiempo_limite"])
            if not isinstance(result["tiempo_limite"], int) or result["tiempo_limite"] <= 0:
                result["tiempo_limite"] = config_default["tiempo_limite"]
            
            # Tiempo desglosado (horas, minutos, segundos)
            result["horas"] = data.get("horas", config_default["horas"])
            if not isinstance(result["horas"], int) or result["horas"] < 0 or result["horas"] > 23:
                result["horas"] = config_default["horas"]
            
            result["minutos"] = data.get("minutos", config_default["minutos"])
            if not isinstance(result["minutos"], int) or result["minutos"] < 0 or result["minutos"] > 59:
                result["minutos"] = config_default["minutos"]
            
            result["segundos"] = data.get("segundos", config_default["segundos"])
            if not isinstance(result["segundos"], int) or result["segundos"] < 0 or result["segundos"] > 59:
                result["segundos"] = config_default["segundos"]
            
            # Calcular tiempo límite si no está definido pero sí las horas/minutos/segundos
            if result["tipo_reloj"] == "TEMPORIZADOR" and result["tiempo_limite"] == config_default["tiempo_limite"]:
                calculated_time = result["horas"] * 3600 + result["minutos"] * 60 + result["segundos"]
                if calculated_time > 0:
                    result["tiempo_limite"] = calculated_time
            
            print(f"[CONFIG] Configuración cargada: {result}")
            return result
            
        except (json.JSONDecodeError, IOError, OSError) as e:
            print(f"[CONFIG] Error al cargar {config_file_path}: {e}")
            continue
        except Exception as e:
            print(f"[CONFIG] Error inesperado al cargar {config_file_path}: {e}")
            continue
    
    # Si no se pudo cargar ningún archivo, devolver valores por defecto
    print(f"[CONFIG] No se pudo cargar configuración, usando valores por defecto: {config_default}")
    return config_default


def save_configuracion(config: Dict[str, Any]) -> bool:
    """
    Guarda la configuración del juego en el archivo JSON.
    
    Args:
        config (Dict[str, Any]): Configuración a guardar
        
    Returns:
        bool: True si se guardó correctamente, False en caso contrario
    """
    try:
        # Crear directorio data si no existe
        os.makedirs("data", exist_ok=True)
        
        # Guardar en el archivo principal
        config_file_path = "data/configuracion.json"
        with open(config_file_path, 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=4, ensure_ascii=False)
        
        print(f"[CONFIG] Configuración guardada en {config_file_path}")
        return True
        
    except Exception as e:
        print(f"[CONFIG] Error al guardar configuración: {e}")
        return False


if __name__ == "__main__":
    # Código de prueba para verificar el funcionamiento
    config = load_configuracion()
    print("Configuración cargada:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    
    # Probar guardado
    test_config = {
        "nivel": "MEDIO",
        "tipo_reloj": "TEMPORIZADOR",
        "tiempo_limite": 900,
        "horas": 0,
        "minutos": 15,
        "segundos": 0
    }
    
    if save_configuracion(test_config):
        print("✅ Configuración de prueba guardada correctamente")
    else:
        print("❌ Error al guardar configuración de prueba") 