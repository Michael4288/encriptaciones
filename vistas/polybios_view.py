import customtkinter as ctk
import time

class PolybiosWorkspaceView(ctk.CTkFrame):
    def __init__(self, parent, cipher_instance, on_back_callback):
        super().__init__(parent, fg_color="transparent")
        self.cipher = cipher_instance
        self.on_back = on_back_callback
        self.cell_labels = {}

        self.build_ui()

    def build_ui(self):
        # Barra Superior
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", padx=20, pady=10)

        ctk.CTkButton(
            top_bar, text="← Volver", width=100, 
            fg_color="#333333", hover_color="#444444", command=self.on_back
        ).pack(side="left")

        ctk.CTkLabel(
            top_bar, text=f"{self.cipher.name} {self.cipher.icon_symbol}", 
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(side="left", padx=20)

        # Panel Principal Dividido (Izquierda: Controles/Grid, Derecha: Resultado)
        content_frame = ctk.CTkFrame(self)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Controles
        ctrl_frame = ctk.CTkFrame(content_frame)
        ctrl_frame.pack(side="left", fill="y", padx=15, pady=15)

        ctk.CTkLabel(ctrl_frame, text="Texto a Encriptar:").pack(anchor="w", padx=10, pady=(10,0))
        self.entry_text = ctk.CTkEntry(ctrl_frame, width=200)
        self.entry_text.insert(0, "HOLA")
        self.entry_text.pack(padx=10, pady=5)

        ctk.CTkButton(ctrl_frame, text="Iniciar Animación", command=self.run_animation).pack(padx=10, pady=15)

        self.lbl_explanation = ctk.CTkLabel(ctrl_frame, text="Listo para comenzar.", wraplength=200)
        self.lbl_explanation.pack(padx=10, pady=10)

        # Cuadrícula 5x5 de Polibio
        grid_frame = ctk.CTkFrame(content_frame, fg_color="#1a1a1a")
        grid_frame.pack(side="left", fill="both", expand=True, padx=15, pady=15)

        for r in range(5):
            for c in range(5):
                letter = self.cipher.grid[r][c]
                lbl = ctk.CTkLabel(
                    grid_frame, text=letter, font=ctk.CTkFont(size=18, weight="bold"),
                    width=45, height=45, fg_color="#2b2b2b", corner_radius=8
                )
                lbl.grid(row=r, column=c, padx=5, pady=5)
                self.cell_labels[(r, c)] = lbl

        # Área de Resultado
        result_frame = ctk.CTkFrame(content_frame)
        result_frame.pack(side="right", fill="both", expand=True, padx=15, pady=15)

        ctk.CTkLabel(result_frame, text="Coordenadas Salida:", font=ctk.CTkFont(size=14)).pack(pady=10)
        self.lbl_result = ctk.CTkLabel(
            result_frame, text="", font=ctk.CTkFont(size=24, weight="bold"), text_color="#3B82F6"
        )
        self.lbl_result.pack(pady=20)

    def run_animation(self):
        text = self.entry_text.get()
        steps = self.cipher.encrypt_steps(text)

        for step in steps:
            # Restaurar colores
            for lbl in self.cell_labels.values():
                lbl.configure(fg_color="#2b2b2b")

            # Resaltar casilla activa
            if step['coords']:
                r, c = step['coords']
                self.cell_labels[(r, c)].configure(fg_color="#1f538d")

            self.lbl_explanation.configure(text=step['explanation'])
            self.lbl_result.configure(text=step['current_result'])
            self.update()
            time.sleep(0.6)