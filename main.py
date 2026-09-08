import customtkinter as ctk

# Ciphers
from encripts.caesar import CaesarCipher
from encripts.vigenere import VigenereCipher
from encripts.polybios import PolybiosCipher
from encripts.columnar_transposition import ColumnarTranspositionCipher
from encripts.groups_transposition import PermutationCipher
from encripts.series_transposition import SelectiveSeriesCipher
from encripts.additive import AdditiveCipher
from encripts.Francmassion import FrancmasonCipher
from encripts.cesar_posicitions import CaesarPositionsCipher
from encripts.cesar_wkey import CaesarKeyCipher
# Views
from vistas.groups_transposition import PermutationWorkspaceView
from vistas.menu_view import MenuView
from vistas.caesar_view import CaesarWorkspaceView
from vistas.vigenere_view import VigenereWorkspaceView
from vistas.polybios_view import PolybiosWorkspaceView
from vistas.columnar_view import ColumnarWorkspaceView
from vistas.series_transposition_view import SeriesWorkspaceView
from vistas.additive_view import AdditiveWorkspaceView
from vistas.franccmassion_view import FrancmasonWorkspaceView
from vistas.cesar_positicions_view import CaesarPositionsWorkspaceView
from vistas.cesar_wkey import CaesarKeyWorkspaceView

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CriptoViz - Entorno Educativo")
        self.geometry("980x680")

        self.algorithms = {
            "caesar": CaesarCipher(),
            "vigenere": VigenereCipher(),
            "polybios": PolybiosCipher(),
            "columnar": ColumnarTranspositionCipher(),  
            "permutation": PermutationCipher(),
            "series": SelectiveSeriesCipher(),
            "additive": AdditiveCipher(), 
            "francmassion": FrancmasonCipher(),
            "caesar_positions": CaesarPositionsCipher(),
            "caesar_wkey": CaesarKeyCipher(),
        }

        self.container = ctk.CTkFrame(self, corner_radius=0)
        self.container.pack(fill="both", expand=True)

        self.current_view = None
        self.show_menu()

    def clear_container(self):
        if self.current_view:
            self.current_view.destroy()

    def show_menu(self):
        self.clear_container()
        self.current_view = MenuView(self.container, self.algorithms, self.open_workspace)
        self.current_view.pack(fill="both", expand=True)

    def open_workspace(self, key):
        self.clear_container()

        if key == "caesar":
            self.current_view = CaesarWorkspaceView(
                self.container, self.algorithms[key], self.show_menu
            )
        elif key == "vigenere":
            self.current_view = VigenereWorkspaceView(
                self.container, self.algorithms[key], self.show_menu
            )
        elif key == "polybios":
            self.current_view = PolybiosWorkspaceView(
                self.container, self.algorithms[key], self.show_menu
            )
        elif key == "columnar":
            self.current_view = ColumnarWorkspaceView(
                self.container, self.algorithms[key], self.show_menu
            )
        elif key == "permutation":
            self.current_view = PermutationWorkspaceView(
                self.container, self.algorithms[key], self.show_menu
            )
        elif key == "series":
            self.current_view = SeriesWorkspaceView(
                self.container, self.algorithms[key], self.show_menu
        )
        elif key == "additive":
            self.current_view = AdditiveWorkspaceView(
                self.container, self.algorithms[key], self.show_menu
        )
        elif key == "francmassion":
            self.current_view = FrancmasonWorkspaceView(
                self.container, self.algorithms[key], self.show_menu
        )
        elif key == "caesar_positions":
            self.current_view = CaesarPositionsWorkspaceView(
                self.container, self.algorithms[key], self.show_menu
        )
        elif key == "caesar_wkey":
            self.current_view = CaesarKeyWorkspaceView(
                self.container, self.algorithms[key], self.show_menu
        )
        else:
            raise ValueError(f"Algoritmo desconocido: {key}")
        self.current_view.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()