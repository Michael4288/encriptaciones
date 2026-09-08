import customtkinter as ctk

class FrancmasonWorkspaceView(ctk.CTkFrame):
    def __init__(self, parent, cipher_instance, on_back_callback):
        super().__init__(parent, fg_color="transparent")
        self.cipher = cipher_instance
        self.on_back = on_back_callback
        self.animation_running = False

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

        # Contenedor Desplazable para Evitar Desbordamiento de Pantalla
        self.scroll_body = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_body.pack(fill="both", expand=True, padx=15, pady=5)

        # Panel de Controles
        ctrl_frame = ctk.CTkFrame(self.scroll_body)
        ctrl_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(ctrl_frame, text="Texto:").grid(row=0, column=0, padx=10, pady=10)

        self.entry_text = ctk.CTkEntry(ctrl_frame, width=280)
        self.entry_text.insert(0, "HOLA")
        self.entry_text.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkButton(
            ctrl_frame, text="Iniciar Animación", command=self.run_animation
        ).grid(row=0, column=2, padx=20, pady=10)

        # Tabla de Símbolos / Alfabeto
        symbols_frame = ctk.CTkFrame(self.scroll_body)
        symbols_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            symbols_frame, text="Alfabeto Francmasón (Pigpen)",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=8)

        alphabet_frame = ctk.CTkFrame(symbols_frame, fg_color="transparent")
        alphabet_frame.pack(padx=10, pady=10)

        for index, (char, symbol) in enumerate(self.cipher.SYMBOLS.items()):
            box = ctk.CTkFrame(alphabet_frame, width=50, height=50)
            box.grid(row=index // 9, column=index % 9, padx=3, pady=3)

            ctk.CTkLabel(box, text=char, font=ctk.CTkFont(size=11, weight="bold")).pack(pady=(2, 0))
            ctk.CTkLabel(box, text=symbol, font=ctk.CTkFont(size=14), text_color="#3B82F6").pack(pady=(0, 2))

        # Cuadro de Resultados
        result_frame = ctk.CTkFrame(self.scroll_body)
        result_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.lbl_explanation = ctk.CTkLabel(
            result_frame, text="Ingresa un mensaje y presiona 'Iniciar Animación'.",
            font=ctk.CTkFont(size=14)
        )
        self.lbl_explanation.pack(pady=15)

        self.lbl_result = ctk.CTkLabel(
            result_frame, text="", font=ctk.CTkFont(size=26, weight="bold"), text_color="#10B981"
        )
        self.lbl_result.pack(pady=(0, 20))

    def run_animation(self):
        text = self.entry_text.get()
        steps = self.cipher.encrypt_steps(text)
        if not steps:
            return

        self._execute_step(steps, 0)

    def _execute_step(self, steps, current_index):
        if current_index < len(steps):
            step = steps[current_index]
            self.lbl_explanation.configure(text=step["explanation"])
            self.lbl_result.configure(text=step["current_result"])
            
            # Programar siguiente frame de animación sin congelar la GUI
            self.after(600, lambda: self._execute_step(steps, current_index + 1))