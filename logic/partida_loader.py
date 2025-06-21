"""
Módulo para cargar partidas aleatorias del juego Kakuro desde archivo JSON.

Este módulo se encarga de leer el archivo de partidas del juego,
filtrar por nivel de dificultad y devolver partidas aleatorias
sin repetir hasta que se agoten todas las disponibles.
"""

import json
import random
import os
from typing import Dict, List, Optional, Any


# Variables internas para trackear partidas usadas
_used_partidas = {
    "FÁCIL": set(),
    "MEDIO": set(),
    "DIFÍCIL": set(),
    "EXPERTO": set()
}

_partidas_cache = None
_partidas_shuffled = False


def _load_partidas_file() -> Optional[List[Dict[str, Any]]]:
    """
    Carga el archivo de partidas desde JSON.
    
    Returns:
        List[Dict[str, Any]]: Lista de partidas cargadas, o None si hay error
    """
    try:
        config_file_path = "data/kakuro2025_partidas.json"
        
        if not os.path.exists(config_file_path):
            print(f"Archivo de partidas no encontrado: {config_file_path}")
            return None
        
        with open(config_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Extraer la lista de partidas
        if isinstance(data, dict) and "partidas" in data:
            return data["partidas"]
        elif isinstance(data, list):
            return data
        else:
            print("Formato de archivo de partidas no válido")
            return None
            
    except (json.JSONDecodeError, IOError, OSError) as e:
        print(f"Error al cargar el archivo de partidas: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado al cargar partidas: {e}")
        return None


def _convert_partida_format(partida: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Convierte una partida del formato actual al formato esperado.
    
    Args:
        partida: Partida en formato actual
        
    Returns:
        Dict con la partida en formato esperado, o None si no se puede convertir
    """
    try:
        # Mapeo de dificultades
        dificultad_mapping = {
            "facil": "FÁCIL",
            "normal": "MEDIO", 
            "dificil": "DIFÍCIL",
            "experto": "EXPERTO"
        }
        
        # Obtener dificultad
        dificultad_original = partida.get("dificultad", "").lower()
        nivel = dificultad_mapping.get(dificultad_original, "FÁCIL")
        
        # Extraer información del tablero
        tablero = partida.get("tablero", [])
        sumas_filas = partida.get("sumas_filas", [])
        sumas_columnas = partida.get("sumas_columnas", [])
        
        if not tablero or not sumas_filas or not sumas_columnas:
            return None
        
        # Generar claves basadas en el tablero
        claves = []
        partida_num = 1  # Por defecto
        
        # Buscar claves en filas (horizontal)
        for fila_idx, fila in enumerate(tablero):
            for col_idx, celda in enumerate(fila):
                if celda == "\\":  # Es una clave horizontal
                    # Contar casillas vacías a la derecha
                    casillas = 0
                    for j in range(col_idx + 1, len(fila)):
                        if fila[j] == "?":
                            casillas += 1
                        elif fila[j] in ["#", "\\"]:
                            break
                    
                    if casillas > 0:
                        # Obtener la suma de la fila
                        suma = sumas_filas[fila_idx][col_idx] if sumas_filas[fila_idx][col_idx] is not None else 0
                        
                        claves.append({
                            "tipo_de_clave": "F",  # Fila
                            "fila": fila_idx + 1,
                            "columna": col_idx + 1,
                            "clave": suma,
                            "casillas": casillas
                        })
        
        # Buscar claves en columnas (vertical)
        for col_idx in range(len(tablero[0])):
            for fila_idx in range(len(tablero)):
                celda = tablero[fila_idx][col_idx]
                if celda == "\\":  # Es una clave vertical
                    # Contar casillas vacías abajo
                    casillas = 0
                    for i in range(fila_idx + 1, len(tablero)):
                        if tablero[i][col_idx] == "?":
                            casillas += 1
                        elif tablero[i][col_idx] in ["#", "\\"]:
                            break
                    
                    if casillas > 0:
                        # Obtener la suma de la columna
                        suma = sumas_columnas[fila_idx][col_idx] if sumas_columnas[fila_idx][col_idx] is not None else 0
                        
                        claves.append({
                            "tipo_de_clave": "C",  # Columna
                            "fila": fila_idx + 1,
                            "columna": col_idx + 1,
                            "clave": suma,
                            "casillas": casillas
                        })
        
        return {
            "nivel_de_dificultad": nivel,
            "partida": partida_num,
            "claves": claves
        }
        
    except Exception as e:
        print(f"Error al convertir formato de partida: {e}")
        return None


def reset_partidas(nivel: Optional[str] = None) -> None:
    """
    Resetea las partidas usadas para un nivel específico o todos los niveles.
    
    Args:
        nivel: Nivel a resetear ("FÁCIL", "MEDIO", "DIFÍCIL", "EXPERTO") o None para todos
    """
    global _used_partidas, _partidas_shuffled
    
    if nivel is None:
        # Resetear todos los niveles
        for nivel_key in _used_partidas:
            _used_partidas[nivel_key].clear()
        _partidas_shuffled = False
    elif nivel in _used_partidas:
        # Resetear solo el nivel especificado
        _used_partidas[nivel].clear()
        _partidas_shuffled = False


def load_random_partida(nivel: str) -> Optional[Dict[str, Any]]:
    """
    Carga una partida aleatoria para el nivel especificado.
    
    Args:
        nivel: Nivel de dificultad ("FÁCIL", "MEDIO", "DIFÍCIL", "EXPERTO")
        
    Returns:
        Dict con la partida en formato esperado, o None si no hay partidas disponibles
        
    Example:
        >>> partida = load_random_partida("FÁCIL")
        >>> print(partida["nivel_de_dificultad"])
        "FÁCIL"
    """
    global _partidas_cache, _partidas_shuffled, _used_partidas
    
    # Validar nivel
    if nivel not in ["FÁCIL", "MEDIO", "DIFÍCIL", "EXPERTO"]:
        print(f"Nivel no válido: {nivel}")
        return None
    
    # Cargar partidas si no están en caché
    if _partidas_cache is None:
        _partidas_cache = _load_partidas_file()
        if _partidas_cache is None:
            return None
    
    # Filtrar partidas por nivel
    partidas_nivel = []
    for partida in _partidas_cache:
        converted_partida = _convert_partida_format(partida)
        if converted_partida and converted_partida["nivel_de_dificultad"] == nivel:
            partidas_nivel.append(converted_partida)
    
    if not partidas_nivel:
        print(f"No hay partidas disponibles para el nivel: {nivel}")
        return None
    
    # Mezclar partidas solo una vez por ejecución
    if not _partidas_shuffled:
        random.shuffle(partidas_nivel)
        _partidas_shuffled = True
    
    # Buscar una partida no usada
    for partida in partidas_nivel:
        partida_id = f"{partida['nivel_de_dificultad']}_{partida['partida']}"
        if partida_id not in _used_partidas[nivel]:
            _used_partidas[nivel].add(partida_id)
            return partida
    
    # Si todas las partidas han sido usadas, resetear y devolver la primera
    print(f"Todas las partidas del nivel {nivel} han sido usadas. Reseteando...")
    reset_partidas(nivel)
    
    if partidas_nivel:
        partida = partidas_nivel[0]
        partida_id = f"{partida['nivel_de_dificultad']}_{partida['partida']}"
        _used_partidas[nivel].add(partida_id)
        return partida
    
    return None


def get_available_partidas_count(nivel: str) -> int:
    """
    Obtiene el número de partidas disponibles para un nivel.
    
    Args:
        nivel: Nivel de dificultad
        
    Returns:
        Número de partidas disponibles
    """
    global _partidas_cache
    
    if _partidas_cache is None:
        _partidas_cache = _load_partidas_file()
        if _partidas_cache is None:
            return 0
    
    partidas_nivel = []
    for partida in _partidas_cache:
        converted_partida = _convert_partida_format(partida)
        if converted_partida and converted_partida["nivel_de_dificultad"] == nivel:
            partidas_nivel.append(converted_partida)
    
    return len(partidas_nivel)


if __name__ == "__main__":
    # Código de prueba para verificar el funcionamiento
    print("=== Prueba del módulo partida_loader ===\n")
    
    # Probar cargar partidas de diferentes niveles
    niveles = ["FÁCIL", "MEDIO", "DIFÍCIL", "EXPERTO"]
    
    for nivel in niveles:
        print(f"Probando nivel: {nivel}")
        partida = load_random_partida(nivel)
        
        if partida:
            print(f"  ✓ Partida cargada: {partida['nivel_de_dificultad']} - Partida {partida['partida']}")
            print(f"  ✓ Número de claves: {len(partida['claves'])}")
            print(f"  ✓ Partidas disponibles: {get_available_partidas_count(nivel)}")
        else:
            print(f"  ✗ No hay partidas disponibles para {nivel}")
        print()
    
    # Probar resetear partidas
    print("Reseteando partidas de nivel FÁCIL...")
    reset_partidas("FÁCIL")
    
    partida = load_random_partida("FÁCIL")
    if partida:
        print(f"✓ Partida cargada después del reset: {partida['nivel_de_dificultad']} - Partida {partida['partida']}")
    
    print("\n=== Pruebas completadas ===") 