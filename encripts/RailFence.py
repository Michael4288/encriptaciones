from .base import BaseCipher

class RailFenceCipher(BaseCipher):
    name = "Cifrado Rail Fence"
    description = "Cifrado de transposición por traslación en zig-zag. Distribuye el texto a través de rieles verticales y lee el resultado fila por fila."
    icon_symbol = "🎢"
    

    def encrypt_steps(self, text: str, rails_str: str, descifrar: bool = False):
        try:
            num_rails = int(rails_str)
            if num_rails < 2:
                num_rails = 2
        except ValueError:
            num_rails = 3

        text = text.replace(" ", "").upper()
        if not text:
            return []

        if descifrar:
            return self._decrypt_steps(text, num_rails)
        else:
            return self._encrypt_steps(text, num_rails)

    def _encrypt_steps(self, text: str, num_rails: int):
        fence = [[] for _ in range(num_rails)]
        rail = 0
        direction = 1  # 1 para bajar, -1 para subir
        steps = []

        for idx, char in enumerate(text):
            fence[rail].append(char)
            
            grid_representation = []
            for r in range(num_rails):
                row_str = "".join([fence[r][i] if i < len(fence[r]) else "." for i in range(len(fence[r]))])
                grid_representation.append(f"Riel {r+1}: {row_str}")

            steps.append({
                'char': char,
                'rail': rail + 1,
                'direction': "Abajo ⬇️" if direction == 1 else "Arriba ⬆️",
                'explanation': f"Carácter '{char}' ubicado en el Riel {rail + 1} (Dirección: {'Abajo' if direction==1 else 'Arriba'})",
                'grid': "\n".join(grid_representation),
                'current_result': "".join(["".join(row) for row in fence])
            })

            # Cambiar dirección al golpear los bordes superior/inferior
            if rail == 0 and direction == -1:
                direction = 1
            elif rail == num_rails - 1 and direction == 1:
                direction = -1

            rail += direction

        return steps

    def _decrypt_steps(self, cipher_text: str, num_rails: int):
        # Malla vacía para marcar posiciones
        length = len(cipher_text)
        fence = [['\n' for _ in range(length)] for _ in range(num_rails)]
        
        rail = 0
        direction = 1
        for i in range(length):
            fence[rail][i] = '*'
            if rail == 0:
                direction = 1
            elif rail == num_rails - 1:
                direction = -1
            rail += direction

        # Llenar la malla con los caracteres del criptograma
        idx = 0
        for r in range(num_rails):
            for c in range(length):
                if fence[r][c] == '*' and idx < length:
                    fence[r][c] = cipher_text[idx]
                    idx += 1

        # Reconstruir el mensaje siguiendo la ruta zigzag
        result = []
        rail = 0
        direction = 1
        steps = []

        for i in range(length):
            char = fence[rail][i]
            result.append(char)
            
            steps.append({
                'char': char,
                'rail': rail + 1,
                'direction': "Zig-Zag",
                'explanation': f"Leyendo Riel {rail + 1}, Posición {i + 1} ➔ '{char}'",
                'grid': f"Reconstruyendo mediante trazado en Riel {rail + 1}",
                'current_result': "".join(result)
            })

            if rail == 0:
                direction = 1
            elif rail == num_rails - 1:
                direction = -1
            rail += direction

        return steps