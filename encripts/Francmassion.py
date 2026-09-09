from .base import BaseCipher

class FrancmasonCipher(BaseCipher):
    name = "Cifrado Francmasón"
    description = "Sustitución monográmica geométrica que reemplaza letras por símbolos según cuadrículas de cerciorado con o sin punto."
    icon_symbol = "📐"

    # Mapeo de caracteres a glifos/símbolos geométricos del Pigpen
    SYMBOLS = {
        'A': '┘', 'B': '└', 'C': '┐', 'D': '┌', 'E': '┴', 'F': '┬', 'G': '┤', 'H': '├', 'I': '┼',
        'J': '┘•', 'K': '└•', 'L': '┐•', 'M': '┌•', 'N': '┴•', 'O': '┬•', 'P': '┤•', 'Q': '├•', 'R': '┼•',
        'S': 'V', 'T': '>', 'U': '<', 'V': '^', 'W': 'V•', 'X': '>•', 'Y': '<•', 'Z': '^•'
    }

    def encrypt_steps(self, text: str, key=None):
        text = text.upper()
        steps = []
        result = []

        for char in text:
            if char in self.SYMBOLS:
                symbol = self.SYMBOLS[char]
                result.append(symbol)
                steps.append({
                    'char': char,
                    'symbol': symbol,
                    'explanation': f"Carácter '{char}' reemplazado por glifo Pigpen ➔ {symbol}",
                    'current_result': " ".join(result)
                })
            else:
                result.append(char)
                steps.append({
                    'char': char,
                    'symbol': char,
                    'explanation': f"'{char}' no forma parte del alfabeto geométrico ➔ Se mantiene igual",
                    'current_result': " ".join(result)
                })

        return steps