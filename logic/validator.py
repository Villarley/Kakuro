"""
Validación de jugadas según las reglas del Kakuro
Verifica que las jugadas cumplan con las restricciones del juego
"""


class KakuroValidator:
    def __init__(self):
        self.max_sum = 45  # Suma máxima posible con números 1-9
    
    def validate_cell_value(self, value):
        """Valida que el valor de una celda sea válido"""
        return isinstance(value, int) and 1 <= value <= 9
    
    def validate_row_sum(self, row_values, target_sum):
        """Valida que la suma de una fila sea correcta"""
        if not row_values or target_sum is None:
            return True
        
        # Filtrar valores no nulos
        valid_values = [v for v in row_values if v is not None and v != 0]
        
        # Verificar que no hay números repetidos
        if len(valid_values) != len(set(valid_values)):
            return False
        
        # Verificar que la suma no excede el objetivo
        current_sum = sum(valid_values)
        return current_sum <= target_sum
    
    def validate_column_sum(self, col_values, target_sum):
        """Valida que la suma de una columna sea correcta"""
        return self.validate_row_sum(col_values, target_sum)
    
    def is_complete_solution(self, board, row_sums, col_sums):
        """Verifica si la solución está completa y es correcta"""
        # TODO: Implementar validación completa
        pass 