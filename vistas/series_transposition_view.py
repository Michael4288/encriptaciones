import customtkinter as ctk
import time

class SeriesWorkspaceView(ctk.CTkFrame):
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

        # Panel de Controles
        ctrl_frame = ctk.CTkFrame(self)
        ctrl_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(ctrl_frame, text="Texto:").grid(row=0, column=0, padx=8, pady=10)
        self.entry_text = ctk.CTkEntry(ctrl_frame, width=150)
        self.entry_text.insert(0, "CRIPTOGRAFIA")
        self.entry_text.grid(row=0, column=1, padx=8, pady=10)

        ctk.CTkLabel(ctrl_frame, text="Modo:").grid(row=0, column=2, padx=8, pady=10)
        self.combo_mode = ctk.CTkOptionMenu(
            ctrl_frame, 
            values=["1. Primos", "2. Pares", "3. Impares", "4. Múltiplos", "5. Personalizada"],
            command=self._on_mode_change
        )
        self.combo_mode.grid(row=0, column=3, padx=8, pady=10)

        self.lbl_extra = ctk.CTkLabel(ctrl_frame, text="Parámetro:")
        self.entry_extra = ctk.CTkEntry(ctrl_frame, width=100, placeholder_text="Ej: 3")

        ctk.CTkButton(
            ctrl_frame, text="Iniciar Animación", command=self.run_animation
        ).grid(row=0, column=6, padx=15, pady=10)

        # Contenedor Visual de la Cinta de Posiciones
        self.tape_container = ctk.CTkFrame(self, fg_color="#1a1a1a")
        self.tape_container.pack(fill="both", expand=True, padx=20, pady=15)

        # Explicación y Salida
        res_frame = ctk.CTkFrame(self)
        res_frame.pack(fill="x", padx=20, pady=10)

        self.lbl_explanation = ctk.CTkLabel(
            res_frame, text="Selecciona el tipo de serie matemática y presiona 'Iniciar Animación'.", 
            font=ctk.CTkFont(size=14)
        )
        self.lbl_explanation.pack(pady=10)

        self.lbl_result = ctk.CTkLabel(
            res_frame, text="", font=ctk.CTkFont(size=24, weight="bold"), text_color="#3B82F6"
        )
        self.lbl_result.pack(pady=(0, 10))

        self._on_mode_change("1. Primos")

    def _on_mode_change(self, choice):
        if "4." in choice or "5." in choice:
            self.lbl_extra.grid(row=0, column=4, padx=5, pady=10)
            self.entry_extra.grid(row=0, column=5, padx=5, pady=10)
            if "4." in choice:
                self.entry_extra.configure(placeholder_text="Múltiplo (Ej: 3)")
            else:
                self.entry_extra.configure(placeholder_text="Ej: 1 4 7 9")
        else:
            self.lbl_extra.grid_forget()
            self.entry_extra.grid_forget()

    def run_animation(self):
        text = self.entry_text.get()
        mode_val = self.combo_mode.get().split(".")[0]
        extra_val = self.entry_extra.get()

        steps = self.cipher.encrypt_steps(text, mode_val, extra_val)
        if not steps:
            return

        for step in steps:
            for widget in self.tape_container.winfo_children():
                widget.destroy()

            # Renderizado de la Cinta con Posiciones
            pos_frame = ctk.CTkFrame(self.tape_container, fg_color="transparent")
            pos_frame.pack(pady=30, padx=10)

            for idx, char in enumerate(text.upper().replace(" ", "")):
                pos = idx + 1
                is_selected = pos in step['posiciones']
                is_current = (pos == step['pos'])

                # Elección de colores
                if is_current:
                    border_color = "#f59e0b"  # Amarillo de proceso activo
                else:
                    border_color = "#374151"

                if is_selected:
                    bg_color = "#10b981"  # Verde serie
                else:
                    bg_color = "#1f2937"  # Gris resto

                box = ctk.CTkFrame(
                    pos_frame, fg_color=bg_color, border_width=2, 
                    border_color=border_color, corner_radius=6
                )
                box.grid(row=0, column=idx, padx=4)

                ctk.CTkLabel(
                    box, text=char, width=38, height=38, 
                    font=ctk.CTkFont(size=16, weight="bold")
                ).pack()

                ctk.CTkLabel(
                    box, text=f"P{pos}", font=ctk.CTkFont(size=9), text_color="#d1d5db"
                ).pack(pady=(0, 2))

            self.lbl_explanation.configure(text=step['explanation'])
            self.lbl_result.configure(text=step['current_result'])
            self.update()
            time.sleep(0.5)