import customtkinter as ctk
import time

class AdditiveWorkspaceView(ctk.CTkFrame):
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

        ctk.CTkLabel(ctrl_frame, text="Texto:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_text = ctk.CTkEntry(ctrl_frame, width=180)
        self.entry_text.insert(0, "SUMA MODULAR")
        self.entry_text.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(ctrl_frame, text="Valor K (Clave):").grid(row=0, column=2, padx=10, pady=10)
        self.entry_key = ctk.CTkEntry(ctrl_frame, width=80)
        self.entry_key.insert(0, "7")
        self.entry_key.grid(row=0, column=3, padx=10, pady=10)

        ctk.CTkButton(
            ctrl_frame, text="Iniciar Animación", command=self.run_animation
        ).grid(row=0, column=4, padx=20, pady=10)

        # Visualizador Modular
        self.math_container = ctk.CTkFrame(self, fg_color="#1a1a1a")
        self.math_container.pack(fill="both", expand=True, padx=20, pady=15)

        # Explicación y Salida
        res_frame = ctk.CTkFrame(self)
        res_frame.pack(fill="x", padx=20, pady=10)

        self.lbl_explanation = ctk.CTkLabel(
            res_frame, text="Ingresa un valor numérico para la clave K y presiona 'Iniciar Animación'.", 
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
            for widget in self.math_container.winfo_children():
                widget.destroy()

            # Renderizar tarjeta de cálculo matemático
            card = ctk.CTkFrame(self.math_container, fg_color="#2b2b2b", corner_radius=12)
            card.pack(pady=40, padx=20)

            if step['p_idx'] is not None:
                # Fórmula visual: P + K ➔ C (mod N)
                formula_frame = ctk.CTkFrame(card, fg_color="transparent")
                formula_frame.pack(padx=25, pady=20)

                # Carácter Original
                box_p = ctk.CTkFrame(formula_frame, fg_color="#1f538d", corner_radius=8)
                box_p.grid(row=0, column=0, padx=10)
                ctk.CTkLabel(box_p, text=step['char'], font=ctk.CTkFont(size=22, weight="bold"), width=50, height=50).pack()
                ctk.CTkLabel(box_p, text=f"P = {step['p_idx']}", font=ctk.CTkFont(size=10)).pack(pady=(0, 4))

                ctk.CTkLabel(formula_frame, text="+", font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=1)

                # Clave
                box_k = ctk.CTkFrame(formula_frame, fg_color="#374151", corner_radius=8)
                box_k.grid(row=0, column=2, padx=10)
                ctk.CTkLabel(box_k, text=str(step['k']), font=ctk.CTkFont(size=22, weight="bold"), width=50, height=50).pack()
                ctk.CTkLabel(box_k, text="Clave (K)", font=ctk.CTkFont(size=10)).pack(pady=(0, 4))

                ctk.CTkLabel(formula_frame, text=f"mod {step['mod']} = ", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=3)

                # Carácter Resultante
                box_c = ctk.CTkFrame(formula_frame, fg_color="#10b981", corner_radius=8)
                box_c.grid(row=0, column=4, padx=10)
                ctk.CTkLabel(box_c, text=step['new_char'], font=ctk.CTkFont(size=22, weight="bold"), width=50, height=50).pack()
                ctk.CTkLabel(box_c, text=f"C = {step['c_idx']}", font=ctk.CTkFont(size=10)).pack(pady=(0, 4))

            else:
                ctk.CTkLabel(card, text=f"Carácter '{step['char']}' no alfabético", font=ctk.CTkFont(size=16)).pack(padx=30, pady=30)

            self.lbl_explanation.configure(text=step['explanation'])
            self.lbl_result.configure(text=step['current_result'])
            self.update()
            time.sleep(0.5)