import customtkinter as ctk
import time

class VigenereWorkspaceView(ctk.CTkFrame):
    def __init__(self, parent, cipher_instance, on_back_callback):
        super().__init__(parent, fg_color="transparent")
        self.cipher = cipher_instance
        self.on_back = on_back_callback
        self.char_cards = []

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
        self.entry_text.insert(0, "CRIPTOGRAFIA")
        self.entry_text.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(ctrl_frame, text="Palabra Clave:").grid(row=0, column=2, padx=10, pady=10)
        self.entry_key = ctk.CTkEntry(ctrl_frame, width=100)
        self.entry_key.insert(0, "SOL")
        self.entry_key.grid(row=0, column=3, padx=10, pady=10)

        ctk.CTkButton(
            ctrl_frame, text="Iniciar Animación", command=self.run_animation
        ).grid(row=0, column=4, padx=20, pady=10)

        # Panel de Alineación de Clave (Visualizador)
        self.alignment_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        self.alignment_frame.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(
            self.alignment_frame, text="Alineación Texto / Clave:", 
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))

        self.cards_container = ctk.CTkFrame(self.alignment_frame, fg_color="transparent")
        self.cards_container.pack(padx=10, pady=(0, 15))

        # Resultado y Explicación
        res_frame = ctk.CTkFrame(self)
        res_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.lbl_explanation = ctk.CTkLabel(
            res_frame, text="Ingresa un texto y clave para simular el cifrado polialfabético.", 
            font=ctk.CTkFont(size=14)
        )
        self.lbl_explanation.pack(pady=15)

        self.lbl_result = ctk.CTkLabel(
            res_frame, text="", font=ctk.CTkFont(size=28, weight="bold"), text_color="#3B82F6"
        )
        self.lbl_result.pack(pady=10)

    def run_animation(self):
        text = self.entry_text.get().upper()
        key = self.entry_key.get().upper().replace(" ", "")

        if not key:
            key = "CLAVE"

        for widget in self.cards_container.winfo_children():
            widget.destroy()

        self.char_cards.clear()

        key_idx = 0
        for idx, char in enumerate(text):
            card = ctk.CTkFrame(self.cards_container, fg_color="#2b2b2b", corner_radius=6)
            card.grid(row=0, column=idx, padx=2, pady=5)

            lbl_t = ctk.CTkLabel(card, text=char, font=ctk.CTkFont(size=14, weight="bold"), width=32)
            lbl_t.pack(pady=(4, 2))

            if char.isalpha():
                k_char = key[key_idx % len(key)]
                key_idx += 1
            else:
                k_char = "-"

            lbl_k = ctk.CTkLabel(
                card, text=k_char, font=ctk.CTkFont(size=12), text_color="#3B82F6", width=32
            )
            lbl_k.pack(pady=(2, 4))

            self.char_cards.append((card, lbl_t, lbl_k))

        # Ejecutar Pasos
        steps = self.cipher.encrypt_steps(text, key)

        for idx, step in enumerate(steps):
            if idx < len(self.char_cards):
                card, lbl_t, lbl_k = self.char_cards[idx]

                # Restaurar previos
                for c, _, _ in self.char_cards:
                    c.configure(fg_color="#2b2b2b")

                # Resaltar actual
                card.configure(fg_color="#1f538d")

            self.lbl_explanation.configure(text=step['explanation'])
            self.lbl_result.configure(text=step['current_result'])
            self.update()
            time.sleep(0.6)