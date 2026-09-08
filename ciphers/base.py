from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseCipher(ABC):
    name: str = "Algoritmo"
    description: str = "Descripción breve del algoritmo."
    icon_symbol: str = "🔐"  # Puedes usar íconos Unicode, GIFs o imágenes PNG
    
    @abstractmethod
    def encrypt_steps(self, text: str, key: Any) -> List[Dict[str, Any]]:
        pass