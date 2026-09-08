from .base import BaseCipher

class CaesarPositionsCipher(BaseCipher):
    name = "César con Posiciones"
    description = "Cifrado por desplazamiento alfabético con soporte explícito de dirección (cifrado/descifrado) y cálculo modular de posiciones."
    icon_symbol = "🔄"

    def __init__(self):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def encrypt_steps(self, text: str, shift_str: str, descifrado: bool = False):
        text = text.upper()
        try:
            shift = int(shift_str)
        except ValueError:
            shift = 3  # Valor por defecto si no es entero válido

        actual_shift = -shift if descifrado else shift
        n = len(self.alphabet)
        steps = []
        result = []

        for char in text:
            if char in self.alphabet:
                p_idx = self.alphabet.index(char)
                c_idx = (p_idx + actual_shift) % n
                new_char = self.alphabet[c_idx]
                result.append(new_char)

                action_str = "Descifrado" if descifrado else "Cifrado"
                steps.append({
                    'char': char,
                    'p_idx': p_idx,
                    'shift': actual_shift,
                    'c_idx': c_idx,
                    'mod': n,
                    'new_char': new_char,
                    'explanation': f"[{action_str}] '{char}' (Pos {p_idx}) ➔ ({p_idx} {'+' if actual_shift>=0 else ''}{actual_shift}) mod {n} = Pos {c_idx} ➔ '{new_char}'",
                    'current_result': "".join(result)
                })
            else:
                result.append(char)
                steps.append({
                    'char': char,
                    'p_idx': None,
                    'shift': actual_shift,
                    'c_idx': None,
                    'mod': n,
                    'new_char': char,
                    'explanation': f"'{char}' no está en el alfabeto (ABC) ➔ Se conserva intacto",
                    'current_result': "".join(result)
                })

        return steps