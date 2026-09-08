from .base import BaseCipher

class ColumnarTranspositionCipher(BaseCipher):
    name = "Transposición Columnar"
    description = "Cifrado por transposición que reordena los caracteres escribiéndolos en una cuadrícula por filas y leyéndolos por columnas."
    icon_symbol = "🔀"

    def encrypt_steps(self, text: str, key: str):
        text = text.upper().replace(" ", "")
        
        # Validación de la clave (número de columnas)
        try:
            cols = int(key)
            if cols < 1:
                cols = 3
        except ValueError:
            cols = 3

        # Padding con 'X' para completar la matriz
        padding_needed = (cols - (len(text) % cols)) % cols
        padded_text = text + ("X" * padding_needed)

        num_rows = len(padded_text) // cols
        
        # Construcción de la matriz visual
        matrix = []
        for r in range(num_rows):
            row = list(padded_text[r * cols : (r + 1) * cols])
            matrix.append(row)

        steps = []
        result = []

        # Recorrido por columnas (cifrado)
        for col_idx in range(cols):
            col_chars = []
            for row_idx in range(num_rows):
                char = matrix[row_idx][col_idx]
                result.append(char)
                col_chars.append(char)
                
                steps.append({
                    'matrix': matrix,
                    'active_pos': (row_idx, col_idx),
                    'active_col': col_idx,
                    'cols': cols,
                    'rows': num_rows,
                    'explanation': f"Leyendo Fila {row_idx + 1}, Columna {col_idx + 1} ('{char}')",
                    'current_result': "".join(result)
                })

        return steps