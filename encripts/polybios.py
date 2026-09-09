from .base import BaseCipher

class PolybiosCipher(BaseCipher):
    name = "Cifrado por Polybios"
    description = "Sustitución monográmica que mapea cada letra a coordenadas en una cuadrícula 5x5."
    icon_symbol = "🔲"

    def __init__(self):
        # Matriz 5x5 clásica (I y J comparten casilla)
        self.grid = [
            [' ','1', '2', '3', '4', '5'],
            ['1','A', 'B', 'C', 'D', 'E'],
            ['2','F', 'G', 'H', 'I', 'K'],
            ['3','L', 'M', 'N', 'O', 'P'],
            ['4','Q', 'R', 'S', 'T', 'U'],
            ['5','V', 'W', 'X', 'Y', 'Z']
        ]

    def encrypt_steps(self, text: str, key: str = ""):
        text = text.upper().replace('J', 'I')
        steps = []
        result = []

        for char in text:
            if not char.isalpha():
                result.append(char)
                steps.append({
                    'char': char,
                    'coords': None,
                    'explanation': f"'{char}' no es alfabético, se mantiene igual.",
                    'current_result': " ".join(result)
                })
                continue

            # Buscar coordenadas en la matriz
            found = False
            for r_idx, row in enumerate(self.grid):
                for c_idx, val in enumerate(row):
                    if val == char:
                        r_num = r_idx 
                        c_num = c_idx 
                        coord_str = f"{r_num}{c_num}"
                        result.append(coord_str)
                        steps.append({
                            'char': char,
                            'coords': (r_idx, c_idx),
                            'explanation': f"'{char}' ➔ Fila {r_num}, Columna {c_num} ({coord_str})",
                            'current_result': " ".join(result)
                        })
                        found = True
                        break
                if found:
                    break

        return steps