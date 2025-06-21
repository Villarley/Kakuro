"""
Módulo para manejar la lectura, escritura y consulta del archivo de récords.
Este módulo gestiona los mejores tiempos de los jugadores por nivel de dificultad.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional


RECORDS_FILE = "data/kakuro2025_record.json"
NIVELES = ["FÁCIL", "MEDIO", "DIFÍCIL", "EXPERTO"]


def guardar_record(nombre_jugador: str, nivel: str, tiempo_usado: int) -> bool:
    """
    Guarda un nuevo récord para el jugador, nivel y tiempo.
    Solo guarda si el juego fue ganado correctamente.
    
    Args:
        nombre_jugador (str): Nombre del jugador
        nivel (str): Nivel de dificultad ("FÁCIL", "MEDIO", "DIFÍCIL", "EXPERTO")
        tiempo_usado (int): Tiempo usado en segundos
        
    Returns:
        bool: True si se guardó exitosamente, False en caso contrario
    """
    if not nombre_jugador or nivel not in NIVELES:
        print("[RECORDS] Datos inválidos, no se guarda récord.")
        return False

    # Crear el registro del récord
    record = {
        "jugador": nombre_jugador,
        "tiempo": tiempo_usado,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Cargar datos existentes
    data = {}

    if os.path.exists(RECORDS_FILE):
        try:
            with open(RECORDS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[RECORDS] Error leyendo archivo: {e}")
            data = {}

    # Inicializar nivel si no existe
    if nivel not in data:
        data[nivel] = []

    # Agregar nuevo récord
    data[nivel].append(record)
    
    # Ordenar por tiempo ascendente (mejor tiempo primero)
    data[nivel].sort(key=lambda r: r["tiempo"])
    
    # Solo mantener los 3 mejores
    data[nivel] = data[nivel][:3]

    # Guardar en archivo
    try:
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(RECORDS_FILE), exist_ok=True)
        
        with open(RECORDS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"[RECORDS] Récord guardado exitosamente para {nombre_jugador} en nivel {nivel}")
        return True
        
    except Exception as e:
        print(f"[RECORDS] Error escribiendo archivo: {e}")
        return False


def obtener_top_records(nivel: str) -> List[Dict[str, Any]]:
    """
    Devuelve la lista de los mejores 3 récords para un nivel dado.
    
    Args:
        nivel (str): Nivel de dificultad
        
    Returns:
        List[Dict[str, Any]]: Lista de récords ordenados por tiempo
    """
    if nivel not in NIVELES:
        print(f"[RECORDS] Nivel inválido: {nivel}")
        return []

    if not os.path.exists(RECORDS_FILE):
        print("[RECORDS] Archivo de récords no existe")
        return []

    try:
        with open(RECORDS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            records = data.get(nivel, [])
            
            # Ordenar por tiempo para asegurar orden correcto
            records.sort(key=lambda r: r["tiempo"])
            
            print(f"[RECORDS] Cargados {len(records)} récords para nivel {nivel}")
            return records
            
    except Exception as e:
        print(f"[RECORDS] Error cargando récords: {e}")
        return []


def formatear_tiempo(segundos: int) -> str:
    """
    Convierte segundos a formato legible HH:MM:SS.
    
    Args:
        segundos (int): Tiempo en segundos
        
    Returns:
        str: Tiempo formateado como HH:MM:SS
    """
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segs = segundos % 60
    
    return f"{horas:02}:{minutos:02}:{segs:02}"


def verificar_nuevo_record(nivel: str, tiempo_usado: int) -> bool:
    """
    Verifica si el tiempo usado es un nuevo récord para el nivel.
    
    Args:
        nivel (str): Nivel de dificultad
        tiempo_usado (int): Tiempo usado en segundos
        
    Returns:
        bool: True si es un nuevo récord, False en caso contrario
    """
    records = obtener_top_records(nivel)
    
    if not records:
        return True  # Es el primer récord
    
    # Verificar si el tiempo es mejor que el peor de los 3 mejores
    peor_tiempo = records[-1]["tiempo"] if len(records) >= 3 else float('inf')
    
    return tiempo_usado < peor_tiempo


def obtener_estadisticas_nivel(nivel: str) -> Dict[str, Any]:
    """
    Obtiene estadísticas del nivel (mejor tiempo, promedio, etc.).
    
    Args:
        nivel (str): Nivel de dificultad
        
    Returns:
        Dict[str, Any]: Estadísticas del nivel
    """
    records = obtener_top_records(nivel)
    
    if not records:
        return {
            "mejor_tiempo": None,
            "promedio_tiempo": None,
            "total_jugadores": 0,
            "ultima_fecha": None
        }
    
    tiempos = [r["tiempo"] for r in records]
    
    return {
        "mejor_tiempo": min(tiempos),
        "promedio_tiempo": sum(tiempos) / len(tiempos),
        "total_jugadores": len(records),
        "ultima_fecha": records[-1]["fecha"]
    }


def limpiar_records_nivel(nivel: str) -> bool:
    """
    Elimina todos los récords de un nivel específico.
    
    Args:
        nivel (str): Nivel de dificultad
        
    Returns:
        bool: True si se eliminaron exitosamente, False en caso contrario
    """
    if not os.path.exists(RECORDS_FILE):
        return True

    try:
        with open(RECORDS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if nivel in data:
            del data[nivel]
        
        with open(RECORDS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        
        print(f"[RECORDS] Récords del nivel {nivel} eliminados")
        return True
        
    except Exception as e:
        print(f"[RECORDS] Error eliminando récords: {e}")
        return False 