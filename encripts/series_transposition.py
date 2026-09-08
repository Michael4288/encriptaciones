from .base import BaseCipher

class SelectiveSeriesCipher(BaseCipher):
    name = "Transposición por Series"
    description = "Cifrado que extrae los caracteres de posiciones específicas (primos, pares, impares, múltiplos o personalizada) y agrupa el resto."
    icon_symbol = "🔢"

    def _es_primo(self, n: int) -> bool:
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    def _obtener_posiciones(self, tipo: str, cantidad: int, extra_param: str) -> list[int]:
        posiciones = []
        tipo = str(tipo).strip()

        if tipo == "1":  # Primos
            posiciones = [i for i in range(1, cantidad + 1) if self._es_primo(i)]
        elif tipo == "2":  # Pares
            posiciones = [i for i in range(1, cantidad + 1) if i % 2 == 0]
        elif tipo == "3":  # Impares
            posiciones = [i for i in range(1, cantidad + 1) if i % 2 != 0]
        elif tipo == "4":  # Múltiplos
            try:
                num = int(extra_param)
                if num > 0:
                    posiciones = [i for i in range(1, cantidad + 1) if i % num == 0]
            except ValueError:
                posiciones = []
        elif tipo == "5":  # Personalizada
            try:
                posiciones = [int(x) for x in extra_param.replace(',', ' ').split() if x.isdigit()]
            except ValueError:
                posiciones = []

        return posiciones

    def encrypt_steps(self, text: str, mode_str: str = "1", extra_param: str = ""):
        text = text.upper().replace(" ", "")
        cantidad = len(text)
        
        posiciones = self._obtener_posiciones(mode_str, cantidad, extra_param)

        serie = []
        resto = []
        steps = []

        for idx, char in enumerate(text):
            pos = idx + 1
            is_selected = pos in posiciones

            if is_selected:
                serie.append(char)
            else:
                resto.append(char)

            current_crypto = "".join(serie) + "".join(resto)

            steps.append({
                'char': char,
                'pos': pos,
                'is_selected': is_selected,
                'posiciones': posiciones,
                'serie': "".join(serie),
                'resto': "".join(resto),
                'explanation': f"Posición {pos} ('{char}'): {'Pertenece a la serie ➔ Grupo A' if is_selected else 'No pertenece ➔ Grupo B'}",
                'current_result': current_crypto
            })

        return steps