from .base import BaseCipher

class VigenereCipher(BaseCipher):
    name = "Cifrado Vigenère"
    description = "Cifrado polialfabético usando una palabra clave repetida."
    icon_symbol = "📊"

    def encrypt_steps(self, text: str, key: str):
        text = text.upper()
        key = str(key).upper().replace(" ", "")
        
        if not key.isalpha():
            key = "CLAVE"  # Clave por defecto si ingresan números o está vacía
            
        steps = []
        result = []
        alphabet = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        key_length = len(key)
        key_index = 0
        
        for char in text:
            if char in alphabet:
                k_char = key[key_index % key_length]
                shift = alphabet.index(k_char)
                orig_idx = alphabet.index(char)
                new_idx = (orig_idx + shift) % len(alphabet)
                new_char = alphabet[new_idx]
                
                result.append(new_char)
                key_index += 1
                
                steps.append({
                    'char': char,
                    'explanation': f"'{char}' + Clave '{k_char}' (shift +{shift}) -> '{new_char}'",
                    'current_result': "".join(result)
                })
            else:
                result.append(char)
                steps.append({
                    'char': char,
                    'explanation': f"'{char}' se mantiene igual",
                    'current_result': "".join(result)
                })
                
        return steps