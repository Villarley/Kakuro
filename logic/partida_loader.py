"""
Cargar partidas de forma aleatoria desde el archivo JSON
Maneja la selección y carga de niveles del juego
"""

import json
import random
from pathlib import Path


class PartidaLoader:
    def __init__(self, data_path="data/kakuro2025_partidas.json"):
        self.data_path = Path(data_path)
        self.partidas = self.load_partidas()
    
    def load_partidas(self):
        """Carga las partidas desde el archivo JSON"""
        try:
            if self.data_path.exists():
                with open(self.data_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    return data.get('partidas', [])
            else:
                return []
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def get_random_partida(self, dificultad=None):
        """Obtiene una partida aleatoria"""
        if not self.partidas:
            return None
        
        if dificultad:
            filtered_partidas = [p for p in self.partidas if p.get('dificultad') == dificultad]
            if not filtered_partidas:
                return None
            return random.choice(filtered_partidas)
        
        return random.choice(self.partidas)
    
    def get_partida_by_id(self, partida_id):
        """Obtiene una partida específica por ID"""
        for partida in self.partidas:
            if partida.get('id') == partida_id:
                return partida
        return None
    
    def get_partidas_by_dificultad(self, dificultad):
        """Obtiene todas las partidas de una dificultad específica"""
        return [p for p in self.partidas if p.get('dificultad') == dificultad]
    
    def get_available_difficulties(self):
        """Obtiene las dificultades disponibles"""
        difficulties = set()
        for partida in self.partidas:
            if 'dificultad' in partida:
                difficulties.add(partida['dificultad'])
        return list(difficulties) 