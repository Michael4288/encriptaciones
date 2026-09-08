import customtkinter as ctk
import time

class CaesarWorkspaceView(ctk.CTkFrame):
    def __init__(self, parent, cipher_instance, on_back_callback):
        super().__init__(parent, fg_color="transparent")
        self.cipher = cipher_instance
        self.on_back = on_back_callback
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.orig_labels = {}
        self.shift_labels = {}

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
        self.entry_text.insert(0, "JULIO CESAR")
        self.entry_text.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(ctrl_frame, text="Desplazamiento (Clave):").grid(row=0, column=2, padx=10, pady=10)
        self.entry_shift = ctk.CTkEntry(ctrl_frame, width=60)
        self.entry_shift.insert(0, "3")
        self.entry_shift.grid(row=0, column=3, padx=10, pady=10)

        ctk.CTkButton(
            ctrl_frame, text="Iniciar Animación", command=self.run_animation
        ).grid(row=0, column=4, padx=20, pady=10)

        # Cintas Alfabéticas Dinámicas
        self.strips_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        self.strips_frame.pack(fill="x", padx=20, pady=15)

        self.lbl_orig_title = ctk.CTkLabel(
            self.strips_frame, text="Alfabeto Original:", font=ctk.CTkFont(size=12, weight="bold")
        )
        self.lbl_orig_title.pack(anchor="w", padx=10, pady=(10, 2))

        self.orig_strip = ctk.CTkFrame(self.strips_frame, fg_color="transparent")
        self.orig_strip.pack(padx=10, pady=5)

        self.lbl_shift_title = ctk.CTkLabel(
            self.strips_frame, text="Alfabeto Desplazado (+0):", font=ctk.CTkFont(size=12, weight="bold")
        )
        self.lbl_shift_title.pack(anchor="w", padx=10, pady=(10, 2))

        self.shift_strip = ctk.CTkFrame(self.strips_frame, fg_color="transparent")
        self.shift_strip.pack(padx=10, pady=(5, 15))

        self.render_strips(shift_val=3)

        # Panel de Estado y Resultado
        res_frame = ctk.CTkFrame(self)
        res_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.lbl_explanation = ctk.CTkLabel(
            res_frame, text="Ingresa los datos y haz clic en Iniciar Animación.", 
            font=ctk.CTkFont(size=14)
        )
        self.lbl_explanation.pack(pady=15)

        self.lbl_result = ctk.CTkLabel(
            res_frame, text="", font=ctk.CTkFont(size=28, weight="bold"), text_color="#3B82F6"
        )
        self.lbl_result.pack(pady=10)

    def render_strips(self, shift_val=0):
        for widget in self.orig_strip.winfo_children():
            widget.destroy()
        for widget in self.shift_strip.winfo_children():
            widget.destroy()

        self.orig_labels.clear()
        self.shift_labels.clear()

        self.lbl_shift_title.configure(text=f"Alfabeto Desplazado (+{shift_val}):")

        for idx, char in enumerate(self.alphabet):
            # Casilla Original
            lbl_o = ctk.CTkLabel(
                self.orig_strip, text=char, width=28, height=28, 
                fg_color="#2b2b2b", corner_radius=4, font=ctk.CTkFont(size=11)
            )
            lbl_o.grid(row=0, column=idx, padx=1)
            self.orig_labels[char] = lbl_o

            # Casilla Desplazada
            shifted_char = self.alphabet[(idx + shift_val) % len(self.alphabet)]
            lbl_s = ctk.CTkLabel(
                self.shift_strip, text=shifted_char, width=28, height=28, 
                fg_color="#2b2b2b", corner_radius=4, font=ctk.CTkFont(size=11)
            )
            lbl_s.grid(row=0, column=idx, padx=1)
            self.shift_labels[char] = lbl_s

    def reset_strip_colors(self):
        for lbl in self.orig_labels.values():
            lbl.configure(fg_color="#2b2b2b")
        for lbl in self.shift_labels.values():
            lbl.configure(fg_color="#2b2b2b")

    def run_animation(self):
        text = self.entry_text.get()
        shift_str = self.entry_shift.get()

        try:
            shift = int(shift_str)
        except ValueError:
            shift = 3

        self.render_strips(shift)
        steps = self.cipher.encrypt_steps(text, shift)

        for step in steps:
            self.reset_strip_colors()

            char = step.get('char', '').upper()
            if char in self.orig_labels:
                self.orig_labels[char].configure(fg_color="#1f538d")
                self.shift_labels[char].configure(fg_color="#10b981")

            self.lbl_explanation.configure(text=step['explanation'])
            self.lbl_result.configure(text=step['current_result'])
            self.update()
            time.sleep(0.6)