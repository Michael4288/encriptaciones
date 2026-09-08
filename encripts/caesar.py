from .base import BaseCipher
from typing import List, Dict, Any

class CaesarCipher(BaseCipher):
    name = "Cifrado César"
    description = "Desplazamiento alfabético clásico basado en una clave numérica."
    icon_symbol = "Poner img"

    def encrypt_steps(self, text: str, key: Any) -> List[Dict[str, Any]]:
        try:
            shift = int(key)
        except ValueError:
            shift = 3

        text = text.upper()
        steps = []
        result = []
        alphabet = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        
        for char in text:
            if char in alphabet:
                orig_idx = alphabet.index(char)
                new_idx = (orig_idx + shift) % len(alphabet)
                new_char = alphabet[new_idx]
                result.append(new_char)
                
                steps.append({
                    'char': char,
                    'explanation': f"'{char}' (pos {orig_idx}) + {shift} -> '{new_char}' (pos {new_idx})",
                    'current_result': "".join(result)
                })
            else:
                result.append(char)
                steps.append({
                    'char': char,
                    'explanation': f"'{char}' se mantiene igual (fuera de alfabeto)",
                    'current_result': "".join(result)
                })
                
        return steps