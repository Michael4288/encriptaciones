from .base import BaseCipher

class CaesarKeyCipher(BaseCipher):
    name = "Cifrado de César con Clave"
    description = "Sustitución polialfabética mediante una clave alfabética. El desplazamiento de cada letra depende de la posición alfabética del carácter correspondiente de la clave."
    icon_symbol = "🔑"

    def __init__(self):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def _limpiar(self, texto: str) -> str:
        return "".join([c for c in texto.upper() if c in self.alphabet])

    def encrypt_steps(self, text: str, key_str: str, descifrar: bool = False):
        clave = self._limpiar(key_str)
        if not clave:
            clave = "CLAVE"

        text = text.upper()
        n = len(self.alphabet)
        steps = []
        result = []
        i = 0

        for char in text:
            if char in self.alphabet:
                key_char = clave[i % len(clave)]
                d = self.alphabet.index(key_char)
                actual_shift = -d if descifrar else d
                
                p_idx = self.alphabet.index(char)
                c_idx = (p_idx + actual_shift) % n
                new_char = self.alphabet[c_idx]
                
                result.append(new_char)

                steps.append({
                    'char': char,
                    'key_char': key_char,
                    'key_idx': d,
                    'p_idx': p_idx,
                    'shift': actual_shift,
                    'c_idx': c_idx,
                    'new_char': new_char,
                    'explanation': f"'{char}' + Clave '{key_char}' (Pos {d}) ➔ ({p_idx} {'+' if actual_shift>=0 else ''}{actual_shift}) mod {n} = Pos {c_idx} ➔ '{new_char}'",
                    'current_result': "".join(result)
                })
                i += 1
            else:
                result.append(char)
                steps.append({
                    'char': char,
                    'key_char': '-',
                    'key_idx': None,
                    'p_idx': None,
                    'shift': 0,
                    'c_idx': None,
                    'new_char': char,
                    'explanation': f"'{char}' no es alfabético ➔ Se mantiene igual",
                    'current_result': "".join(result)
                })

        return steps