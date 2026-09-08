from .base import BaseCipher

class AdditiveCipher(BaseCipher):
    name = "Cifrado por Adición"
    description = "Sustitución monográmica aditiva. Suma un valor clave K al índice alfabético de cada letra usando aritmética modular (C = P + K mod N)."
    icon_symbol = "➕"

    def __init__(self):
        self.alphabet = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"

    def encrypt_steps(self, text: str, key_str: str):
        text = text.upper()
        
        try:
            k = int(key_str)
        except ValueError:
            k = 5  # Clave por defecto si la entrada es inválida

        n = len(self.alphabet)
        steps = []
        result = []

        for char in text:
            if char in self.alphabet:
                p_idx = self.alphabet.index(char)
                c_idx = (p_idx + k) % n
                new_char = self.alphabet[c_idx]
                
                result.append(new_char)

                steps.append({
                    'char': char,
                    'p_idx': p_idx,
                    'k': k,
                    'c_idx': c_idx,
                    'mod': n,
                    'new_char': new_char,
                    'explanation': f"'{char}' (Pos {p_idx}) ➔ ({p_idx} + {k}) mod {n} = {c_idx} ➔ '{new_char}'",
                    'current_result': "".join(result)
                })
            else:
                result.append(char)
                steps.append({
                    'char': char,
                    'p_idx': None,
                    'k': k,
                    'c_idx': None,
                    'mod': n,
                    'new_char': char,
                    'explanation': f"'{char}' no está en el alfabeto ➔ Se mantiene igual",
                    'current_result': "".join(result)
                })

        return steps