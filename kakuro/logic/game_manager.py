"""
Manejo del estado general del juego Kakuro
Controla el flujo del juego y el estado actual
"""

from .validator import KakuroValidator
from .pila_jugadas import PilaJugadas


class GameManager:
    def __init__(self):
        self.validator = KakuroValidator()
        self.pila_jugadas = PilaJugadas()
        self.current_board = None
        self.game_state = "menu"  # menu, playing, paused, completed
        self.current_level = None
        self.score = 0
        self.time_elapsed = 0
    
    def start_new_game(self, level):
        """Inicia una nueva partida"""
        self.current_level = level
        self.game_state = "playing"
        self.score = 0
        self.time_elapsed = 0
        # TODO: Cargar tablero del nivel
        self.pila_jugadas.clear()
    
    def make_move(self, row, col, value):
        """Realiza una jugada"""
        if self.game_state != "playing":
            return False
        
        # Validar la jugada
        if not self.validator.validate_cell_value(value):
            return False
        
        # Guardar jugada en la pila
        self.pila_jugadas.push((row, col, self.current_board[row][col]))
        
        # Aplicar la jugada
        self.current_board[row][col] = value
        
        # Verificar si el juego está completo
        if self.is_game_complete():
            self.game_state = "completed"
        
        return True
    
    def undo_move(self):
        """Deshace la última jugada"""
        if self.pila_jugadas.is_empty():
            return False
        
        row, col, previous_value = self.pila_jugadas.pop()
        self.current_board[row][col] = previous_value
        return True
    
    def is_game_complete(self):
        """Verifica si el juego está completo"""
        # TODO: Implementar verificación de completitud
        return False
    
    def pause_game(self):
        """Pausa el juego"""
        if self.game_state == "playing":
            self.game_state = "paused"
    
    def resume_game(self):
        """Reanuda el juego"""
        if self.game_state == "paused":
            self.game_state = "playing" 