"""
Implementación de una pila para deshacer/rehacer jugadas
Mantiene el historial de movimientos del jugador
"""


class PilaJugadas:
    def __init__(self, max_size=100):
        self.stack = []
        self.max_size = max_size
        self.redo_stack = []
    
    def push(self, jugada):
        """Añade una jugada a la pila"""
        if len(self.stack) >= self.max_size:
            self.stack.pop(0)  # Eliminar la jugada más antigua
        
        self.stack.append(jugada)
        self.redo_stack.clear()  # Limpiar pila de rehacer
    
    def pop(self):
        """Extrae la última jugada de la pila"""
        if self.is_empty():
            return None
        
        jugada = self.stack.pop()
        self.redo_stack.append(jugada)
        return jugada
    
    def peek(self):
        """Mira la última jugada sin extraerla"""
        if self.is_empty():
            return None
        return self.stack[-1]
    
    def is_empty(self):
        """Verifica si la pila está vacía"""
        return len(self.stack) == 0
    
    def size(self):
        """Retorna el tamaño de la pila"""
        return len(self.stack)
    
    def clear(self):
        """Limpia la pila"""
        self.stack.clear()
        self.redo_stack.clear()
    
    def can_redo(self):
        """Verifica si se puede rehacer una jugada"""
        return len(self.redo_stack) > 0
    
    def redo(self):
        """Rehace la última jugada deshecha"""
        if not self.can_redo():
            return None
        
        jugada = self.redo_stack.pop()
        self.stack.append(jugada)
        return jugada 