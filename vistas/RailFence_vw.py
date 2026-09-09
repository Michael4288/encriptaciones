import customtkinter as ctk

class RailFenceWorkspaceView(ctk.CTkFrame):
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
            fg_color="#1E293B", hover_color="#334155", command=self.on_back
        ).pack(side="left")

        ctk.CTkLabel(
            top_bar, text=f"{self.cipher.name} {self.cipher.icon_symbol}", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#F8FAFC"
        ).pack(side="left", padx=20)

        # Contenedor Desplazable estilo Glassmorphism
        self.scroll_body = ctk.CTkScrollableFrame(self, fg_color="#0F172A", corner_radius=15)
        self.scroll_body.pack(fill="both", expand=True, padx=15, pady=5)

        # Panel de Controles
        ctrl_frame = ctk.CTkFrame(self.scroll_body, fg_color="#1E293B", corner_radius=10)
        ctrl_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(ctrl_frame, text="Texto:", text_color="#E2E8F0").grid(row=0, column=0, padx=8, pady=12)
        self.entry_text = ctk.CTkEntry(ctrl_frame, width=180, fg_color="#0F172A", border_color="#3B82F6")
        self.entry_text.insert(0, "CRIPTOGRAFIA")
        self.entry_text.grid(row=0, column=1, padx=8, pady=12)

        ctk.CTkLabel(ctrl_frame, text="Rieles (Filas):", text_color="#E2E8F0").grid(row=0, column=2, padx=8, pady=12)
        self.entry_rails = ctk.CTkEntry(ctrl_frame, width=70, fg_color="#0F172A", border_color="#3B82F6")
        self.entry_rails.insert(0, "3")
        self.entry_rails.grid(row=0, column=3, padx=8, pady=12)

        self.switch_mode = ctk.CTkSwitch(ctrl_frame, text="Modo Descifrar", progress_color="#3B82F6")
        self.switch_mode.grid(row=0, column=4, padx=12, pady=12)

        ctk.CTkButton(
            ctrl_frame, text="Iniciar Animación",
            fg_color="#2563EB", hover_color="#1D4ED8",
            command=self.run_animation
        ).grid(row=0, column=5, padx=15, pady=12)

        # Monitor Visual del Riel (Grid)
        self.display_card = ctk.CTkFrame(self.scroll_body, fg_color="#090D16", corner_radius=12)
        self.display_card.pack(fill="both", expand=True, padx=10, pady=10)

        # Explicación y Resultados
        res_frame = ctk.CTkFrame(self.scroll_body, fg_color="#1E293B", corner_radius=10)
        res_frame.pack(fill="x", padx=10, pady=10)

        self.lbl_explanation = ctk.CTkLabel(
            res_frame, text="Ingresa un mensaje y el número de rieles para iniciar la animación.", 
            font=ctk.CTkFont(size=14), text_color="#E2E8F0"
        )
        self.lbl_explanation.pack(pady=10)

        self.lbl_result = ctk.CTkLabel(
            res_frame, text="", font=ctk.CTkFont(size=24, weight="bold"), text_color="#10B981"
        )
        self.lbl_result.pack(pady=(0, 10))

    def run_animation(self):
        text = self.entry_text.get()
        rails_str = self.entry_rails.get()
        is_descifrar = bool(self.switch_mode.get())

        steps = self.cipher.encrypt_steps(text, rails_str, descifrar=is_descifrar)
        if not steps:
            return

        self._execute_step(steps, 0)

    def _execute_step(self, steps, current_index):
        if current_index < len(steps):
            step = steps[current_index]

            for widget in self.display_card.winfo_children():
                widget.destroy()

            card = ctk.CTkFrame(self.display_card, fg_color="#2b2b2b", corner_radius=10)
            card.pack(pady=20, padx=20, fill="x")

            # Indicadores visuales
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(pady=10)

            box_char = ctk.CTkFrame(info_frame, fg_color="#1f538d", corner_radius=6)
            box_char.grid(row=0, column=0, padx=8)
            ctk.CTkLabel(box_char, text=step['char'], font=ctk.CTkFont(size=20, weight="bold"), width=40, height=40).pack()

            ctk.CTkLabel(info_frame, text=f"➔ Riel {step['rail']} ({step['direction']})", font=ctk.CTkFont(size=15, weight="bold")).grid(row=0, column=1, padx=10)

            # Estado actual de los Rieles
            grid_box = ctk.CTkTextbox(card, height=100, font=ctk.CTkFont(family="Courier", size=13), fg_color="#0F172A")
            grid_box.pack(fill="x", padx=15, pady=10)
            grid_box.insert("1.0", step['grid'])
            grid_box.configure(state="disabled")

            self.lbl_explanation.configure(text=step['explanation'])
            self.lbl_result.configure(text=f"Resultado acumulado: {step['current_result']}")

            self.after(600, lambda: self._execute_step(steps, current_index + 1))