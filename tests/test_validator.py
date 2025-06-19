"""
Pruebas para el módulo de validación
Test unitarios para KakuroValidator
"""

import unittest
import sys
import os

# Añadir el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logic.validator import KakuroValidator


class TestKakuroValidator(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para cada prueba"""
        self.validator = KakuroValidator()
    
    def test_validate_cell_value_valid(self):
        """Prueba validación de valores válidos de celda"""
        for value in range(1, 10):
            self.assertTrue(self.validator.validate_cell_value(value))
    
    def test_validate_cell_value_invalid(self):
        """Prueba validación de valores inválidos de celda"""
        invalid_values = [0, 10, -1, 1.5, "a", None]
        for value in invalid_values:
            self.assertFalse(self.validator.validate_cell_value(value))
    
    def test_validate_row_sum_valid(self):
        """Prueba validación de suma de fila válida"""
        row_values = [1, 2, 3, None, 5]
        target_sum = 15
        self.assertTrue(self.validator.validate_row_sum(row_values, target_sum))
    
    def test_validate_row_sum_invalid_duplicate(self):
        """Prueba validación de fila con números duplicados"""
        row_values = [1, 2, 2, 3, 4]
        target_sum = 15
        self.assertFalse(self.validator.validate_row_sum(row_values, target_sum))
    
    def test_validate_row_sum_invalid_exceeds_target(self):
        """Prueba validación de fila que excede la suma objetivo"""
        row_values = [9, 8, 7, 6]
        target_sum = 20
        self.assertFalse(self.validator.validate_row_sum(row_values, target_sum))
    
    def test_validate_column_sum_valid(self):
        """Prueba validación de suma de columna válida"""
        col_values = [1, 2, 3, None, 5]
        target_sum = 15
        self.assertTrue(self.validator.validate_column_sum(col_values, target_sum))
    
    def test_validate_column_sum_invalid(self):
        """Prueba validación de columna inválida"""
        col_values = [1, 2, 2, 3, 4]
        target_sum = 15
        self.assertFalse(self.validator.validate_column_sum(col_values, target_sum))


if __name__ == '__main__':
    unittest.main() 