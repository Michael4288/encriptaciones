import customtkinter as ctk

class CaesarKeyWorkspaceView(ctk.CTkFrame):
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

        # Contenedor Desplazable (Scroll)
        self.scroll_body = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_body.pack(fill="both", expand=True, padx=15, pady=5)

        # Panel de Controles
        ctrl_frame = ctk.CTkFrame(self.scroll_body)
        ctrl_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(ctrl_frame, text="Texto:").grid(row=0, column=0, padx=8, pady=10)
        self.entry_text = ctk.CTkEntry(ctrl_frame, width=180)
        self.entry_text.insert(0, "MENSAJE SECRETO")
        self.entry_text.grid(row=0, column=1, padx=8, pady=10)

        ctk.CTkLabel(ctrl_frame, text="Clave:").grid(row=0, column=2, padx=8, pady=10)
        self.entry_key = ctk.CTkEntry(ctrl_frame, width=100)
        self.entry_key.insert(0, "CLAVE")
        self.entry_key.grid(row=0, column=3, padx=8, pady=10)

        self.switch_mode = ctk.CTkSwitch(ctrl_frame, text="Modo Descifrar")
        self.switch_mode.grid(row=0, column=4, padx=12, pady=10)

        ctk.CTkButton(
            ctrl_frame, text="Iniciar Animación", command=self.run_animation
        ).grid(row=0, column=5, padx=15, pady=10)

        # Tarjeta Visualizadora
        self.display_card = ctk.CTkFrame(self.scroll_body, fg_color="#1a1a1a")
        self.display_card.pack(fill="both", expand=True, padx=10, pady=10)

        # Resultados
        res_frame = ctk.CTkFrame(self.scroll_body)
        res_frame.pack(fill="x", padx=10, pady=10)

        self.lbl_explanation = ctk.CTkLabel(
            res_frame, text="Ingresa un texto y una clave alfabética para iniciar.", 
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
        is_descifrar = bool(self.switch_mode.get())

        steps = self.cipher.encrypt_steps(text, key_str, descifrar=is_descifrar)
        if not steps:
            return

        self._execute_step(steps, 0)

    def _execute_step(self, steps, current_index):
        if current_index < len(steps):
            step = steps[current_index]

            for widget in self.display_card.winfo_children():
                widget.destroy()

            card = ctk.CTkFrame(self.display_card, fg_color="#2b2b2b", corner_radius=10)
            card.pack(pady=30, padx=20)

            if step['p_idx'] is not None:
                box_frame = ctk.CTkFrame(card, fg_color="transparent")
                box_frame.pack(padx=20, pady=20)

                # Carácter Original
                box_p = ctk.CTkFrame(box_frame, fg_color="#1f538d", corner_radius=6)
                box_p.grid(row=0, column=0, padx=8)
                ctk.CTkLabel(box_p, text=step['char'], font=ctk.CTkFont(size=22, weight="bold"), width=45, height=45).pack()
                ctk.CTkLabel(box_p, text=f"Pos {step['p_idx']}", font=ctk.CTkFont(size=10)).pack(pady=(0, 2))

                # Clave Usada
                box_k = ctk.CTkFrame(box_frame, fg_color="#f59e0b", corner_radius=6)
                box_k.grid(row=0, column=1, padx=8)
                ctk.CTkLabel(box_k, text=step['key_char'], font=ctk.CTkFont(size=22, weight="bold"), width=45, height=45).pack()
                ctk.CTkLabel(box_k, text=f"Shift {step['shift']}", font=ctk.CTkFont(size=10)).pack(pady=(0, 2))

                ctk.CTkLabel(box_frame, text="➔", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=2, padx=8)

                # Carácter Destino
                box_c = ctk.CTkFrame(box_frame, fg_color="#10b981", corner_radius=6)
                box_c.grid(row=0, column=3, padx=8)
                ctk.CTkLabel(box_c, text=step['new_char'], font=ctk.CTkFont(size=22, weight="bold"), width=45, height=45).pack()
                ctk.CTkLabel(box_c, text=f"Pos {step['c_idx']}", font=ctk.CTkFont(size=10)).pack(pady=(0, 2))

            else:
                ctk.CTkLabel(card, text=f"Carácter '{step['char']}' no alfabético", font=ctk.CTkFont(size=16)).pack(padx=20, pady=20)

            self.lbl_explanation.configure(text=step['explanation'])
            self.lbl_result.configure(text=step['current_result'])

            self.after(500, lambda: self._execute_step(steps, current_index + 1))