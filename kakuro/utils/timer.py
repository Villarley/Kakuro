"""
Lógica del cronómetro y temporizador
Maneja el tiempo de juego y límites de tiempo
"""

import time
import threading
from typing import Callable, Optional


class GameTimer:
    def __init__(self, time_limit: Optional[int] = None):
        self.time_limit = time_limit  # en segundos
        self.start_time = None
        self.elapsed_time = 0
        self.is_running = False
        self.is_paused = False
        self.timer_thread = None
        self.on_time_update: Optional[Callable] = None
        self.on_time_limit_reached: Optional[Callable] = None
    
    def start(self):
        """Inicia el cronómetro"""
        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True
            self.is_paused = False
            self.timer_thread = threading.Thread(target=self._timer_loop)
            self.timer_thread.daemon = True
            self.timer_thread.start()
    
    def pause(self):
        """Pausa el cronómetro"""
        if self.is_running and not self.is_paused:
            self.is_paused = True
            self.elapsed_time = time.time() - self.start_time
    
    def resume(self):
        """Reanuda el cronómetro"""
        if self.is_running and self.is_paused:
            self.is_paused = False
            self.start_time = time.time() - self.elapsed_time
    
    def stop(self):
        """Detiene el cronómetro"""
        self.is_running = False
        if self.timer_thread:
            self.timer_thread.join(timeout=1)
    
    def reset(self):
        """Reinicia el cronómetro"""
        self.stop()
        self.elapsed_time = 0
        self.start_time = None
    
    def get_elapsed_time(self) -> int:
        """Obtiene el tiempo transcurrido en segundos"""
        if not self.is_running:
            return int(self.elapsed_time)
        
        if self.is_paused:
            return int(self.elapsed_time)
        
        return int(time.time() - self.start_time)
    
    def get_remaining_time(self) -> Optional[int]:
        """Obtiene el tiempo restante si hay límite de tiempo"""
        if self.time_limit is None:
            return None
        
        elapsed = self.get_elapsed_time()
        remaining = self.time_limit - elapsed
        return max(0, remaining)
    
    def is_time_up(self) -> bool:
        """Verifica si se ha agotado el tiempo"""
        if self.time_limit is None:
            return False
        
        return self.get_remaining_time() <= 0
    
    def _timer_loop(self):
        """Bucle interno del temporizador"""
        while self.is_running:
            if not self.is_paused:
                if self.on_time_update:
                    self.on_time_update(self.get_elapsed_time())
                
                if self.is_time_up() and self.on_time_limit_reached:
                    self.on_time_limit_reached()
                    break
            
            time.sleep(1)
    
    def set_time_update_callback(self, callback: Callable[[int], None]):
        """Establece callback para actualizaciones de tiempo"""
        self.on_time_update = callback
    
    def set_time_limit_callback(self, callback: Callable[[], None]):
        """Establece callback para cuando se agota el tiempo"""
        self.on_time_limit_reached = callback 