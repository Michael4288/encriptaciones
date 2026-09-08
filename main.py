import customtkinter as ctk

# Ciphers
from ciphers.caesar import CaesarCipher
from ciphers.vigenere import VigenereCipher
from ciphers.polybios import PolybiosCipher

# Views
from vistas.menu_view import MenuView
from vistas.caesar_view import CaesarWorkspaceView
from vistas.vigenere_view import VigenereWorkspaceView
from vistas.polybios_view import PolybiosWorkspaceView

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
            "polybios": PolybiosCipher()
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

        self.current_view.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()