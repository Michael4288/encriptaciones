from .base import BaseCipher

class PermutationCipher(BaseCipher):
    name = "Cifrado de transposición por grupos"
    description = "Cifrado por transposición que divide el texto en bloques de tamaño N y permuta las posiciones internas según una clave numérica."
    icon_symbol = "🧩"

    def encrypt_steps(self, text: str, key_str: str):
        text = text.upper().replace(" ", "")
        
        # Procesamiento de la clave (ej. "3 1 4 2")
        try:
            key = [int(x) for x in key_str.strip().split()]
            if not key:
                key = [2, 1]
        except ValueError:
            key = [2, 1]

        key_len = len(key)

        # Padding con 'X'
        padding_needed = (key_len - (len(text) % key_len)) % key_len
        padded_text = text + ("X" * padding_needed)

        steps = []
        result = []

        # Procesar bloque por bloque
        for block_idx, i in enumerate(range(0, len(padded_text), key_len)):
            block = padded_text[i : i + key_len]
            permuted_block = [""] * key_len

            for p_idx, pos in enumerate(key):
                # Validar que el índice no exceda el tamaño del bloque
                target_idx = (pos - 1) % key_len
                char = block[target_idx]
                result.append(char)

                steps.append({
                    'block': block,
                    'block_num': block_idx + 1,
                    'key': key,
                    'active_char': char,
                    'active_pos_in_block': target_idx,
                    'explanation': f"Bloque {block_idx + 1} '{block}': Posición {pos} ➔ Tomar '{char}'",
                    'current_result': "".join(result)
                })

        return steps