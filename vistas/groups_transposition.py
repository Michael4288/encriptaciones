import customtkinter as ctk
import time

class PermutationWorkspaceView(ctk.CTkFrame):
    def __init__(self, parent, cipher_instance, on_back_callback):
        super().__init__(parent, fg_color="transparent")
        self.cipher = cipher_instance
        self.on_back = on_back_callback

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

        # Controles
        ctrl_frame = ctk.CTkFrame(self)
        ctrl_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(ctrl_frame, text="Texto:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_text = ctk.CTkEntry(ctrl_frame, width=180)
        self.entry_text.insert(0, "TRANS POSI CION")
        self.entry_text.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(ctrl_frame, text="Clave (índices):").grid(row=0, column=2, padx=10, pady=10)
        self.entry_key = ctk.CTkEntry(ctrl_frame, width=120)
        self.entry_key.insert(0, "3 1 4 2")
        self.entry_key.grid(row=0, column=3, padx=10, pady=10)

        ctk.CTkButton(
            ctrl_frame, text="Iniciar Animación", command=self.run_animation
        ).grid(row=0, column=4, padx=20, pady=10)

        # Contenedor Visual
        self.blocks_container = ctk.CTkFrame(self, fg_color="#1a1a1a")
        self.blocks_container.pack(fill="both", expand=True, padx=20, pady=15)

        # Explicación y Salida
        res_frame = ctk.CTkFrame(self)
        res_frame.pack(fill="x", padx=20, pady=10)

        self.lbl_explanation = ctk.CTkLabel(
            res_frame, text="Ingresa los índices de clave (separados por espacio) para permutar los bloques.", 
            font=ctk.CTkFont(size=14)
        )
        self.lbl_explanation.pack(pady=10)

        self.lbl_result = ctk.CTkLabel(
            res_frame, text="", font=ctk.CTkFont(size=24, weight="bold"), text_color="#3B82F6"
        )
        self.lbl_result.pack(pady=(0, 10))

    def run_animation(self):
        text = self.entry_text.get()
        key_str = self.entry_key.get()

        steps = self.cipher.encrypt_steps(text, key_str)
        if not steps:
            return

        for step in steps:
            # Renderizar bloques de la fase actual
            for widget in self.blocks_container.winfo_children():
                widget.destroy()

            # Renderizar bloque activo
            block = step['block']
            active_idx = step['active_pos_in_block']

            block_card = ctk.CTkFrame(self.blocks_container, fg_color="#2b2b2b", corner_radius=10)
            block_card.pack(pady=30, padx=20)

            ctk.CTkLabel(
                block_card, text=f"Bloque #{step['block_num']}", 
                font=ctk.CTkFont(size=12, weight="bold"), text_color="#9ca3af"
            ).pack(pady=(10, 5))

            chars_frame = ctk.CTkFrame(block_card, fg_color="transparent")
            chars_frame.pack(padx=15, pady=10)

            for idx, char in enumerate(block):
                is_active = (idx == active_idx)
                color = "#10b981" if is_active else "#333333"

                box = ctk.CTkFrame(chars_frame, fg_color=color, corner_radius=6)
                box.grid(row=0, column=idx, padx=5)

                ctk.CTkLabel(
                    box, text=char, width=40, height=40, 
                    font=ctk.CTkFont(size=18, weight="bold")
                ).pack()

                ctk.CTkLabel(
                    box, text=f"Pos {idx+1}", font=ctk.CTkFont(size=10), text_color="#d1d5db"
                ).pack(pady=(0, 2))

            self.lbl_explanation.configure(text=step['explanation'])
            self.lbl_result.configure(text=step['current_result'])
            self.update()
            time.sleep(0.6)