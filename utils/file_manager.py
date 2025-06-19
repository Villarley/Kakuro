"""
Leer y escribir archivos JSON
Maneja la persistencia de datos del juego
"""

import json
from pathlib import Path
from typing import Any, Dict, List


class FileManager:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
    
    def read_json(self, filename: str) -> Dict[str, Any]:
        """Lee un archivo JSON"""
        file_path = self.data_dir / filename
        try:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            else:
                return {}
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def write_json(self, filename: str, data: Dict[str, Any]) -> bool:
        """Escribe datos en un archivo JSON"""
        file_path = self.data_dir / filename
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def save_game_state(self, game_data: Dict[str, Any]) -> bool:
        """Guarda el estado actual del juego"""
        return self.write_json("kakuro2025_juego_actual.json", {
            "juego_actual": game_data
        })
    
    def load_game_state(self) -> Dict[str, Any]:
        """Carga el estado guardado del juego"""
        data = self.read_json("kakuro2025_juego_actual.json")
        return data.get("juego_actual", {})
    
    def save_configuration(self, config: Dict[str, Any]) -> bool:
        """Guarda la configuración del juego"""
        return self.write_json("kakuro2025_configuración.json", {
            "configuracion": config
        })
    
    def load_configuration(self) -> Dict[str, Any]:
        """Carga la configuración del juego"""
        data = self.read_json("kakuro2025_configuración.json")
        return data.get("configuracion", {})
    
    def save_records(self, records: List[Dict[str, Any]]) -> bool:
        """Guarda los récords de jugadores"""
        return self.write_json("kakuro2025_récords.json", {
            "records": records
        })
    
    def load_records(self) -> List[Dict[str, Any]]:
        """Carga los récords de jugadores"""
        data = self.read_json("kakuro2025_récords.json")
        return data.get("records", []) 