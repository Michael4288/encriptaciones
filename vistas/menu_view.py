import customtkinter as ctk
import random

class AnimatedBackgroundCanvas(ctk.CTkCanvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, highlightthickness=0, bd=0, **kwargs)
        self.bind("<Configure>", self._on_resize)
        
        # Caracteres temáticos de criptografía
        self.symbols = "01101001010101001ABCDEFXYZ$#%&*@!?"
        self.columns = []
        self.font_size = 14
        self.running = False

    def _on_resize(self, event):
        self.width = event.width
        self.height = event.height
        
        num_cols = int(self.width / self.font_size) if self.font_size else 1
        # Cada columna tiene: [posicion_y, velocidad, caracter]
        self.columns = [
            [random.randint(-self.height if self.height > 0 else -500, 0), random.randint(2, 6), random.choice(self.symbols)] 
            for _ in range(num_cols)
        ]

    def start_animation(self):
        if not self.running:
            self.running = True
            self.animate()

    def stop_animation(self):
        self.running = False

    def animate(self):
        if not self.running:
            return

        self.delete("all")
        
        for i in range(len(self.columns)):
            x = i * self.font_size
            y = self.columns[i][0]
            char = self.columns[i][2]

            self.create_text(
                x, y, 
                text=char, 
                fill="#1e3a8a",  # Azul tenue criptográfico
                font=("Courier", self.font_size, "bold"), 
                anchor="nw"
            )

            # Mover posición hacia abajo
            self.columns[i][0] += self.columns[i][1]

            # Reiniciar al llegar abajo
            if self.columns[i][0] > getattr(self, 'height', 600):
                self.columns[i][0] = random.randint(-50, 0)
                self.columns[i][1] = random.randint(2, 6)
                self.columns[i][2] = random.choice(self.symbols)

        # Reprogramar cuadro (~30 FPS)
        self.after(33, self.animate)


class MenuView(ctk.CTkFrame):
    def __init__(self, parent, algorithms, on_select_callback):
        super().__init__(parent, fg_color="transparent")
        self.algorithms = algorithms
        self.on_select = on_select_callback
        
        self.build_ui()

    def build_ui(self):
        # 1. Canvas de Fondo Animado
        self.bg_canvas = AnimatedBackgroundCanvas(self, bg="#111111")
        self.bg_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.bg_canvas.start_animation()

        # 2. Contenedor de Interfaz
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        lbl_title = ctk.CTkLabel(
            content_frame, 
            text="Encriptación, Primer parcial", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#ffffff"
        )
        lbl_title.pack(pady=(20, 5))

        lbl_subtitle = ctk.CTkLabel(
            content_frame, 
            text="Selecciona un algoritmo para visualizar su funcionamiento en tiempo real", 
            font=ctk.CTkFont(size=13),
            text_color="#9ca3af"
        )
        lbl_subtitle.pack(pady=(0, 10))

        # 3. Grid de Tarjetas dentro de un CTkScrollableFrame
        cards_frame = ctk.CTkScrollableFrame(
            content_frame, 
            fg_color="transparent",
            scrollbar_button_color="#1f538d",
            scrollbar_button_hover_color="#2563eb"
        )
        cards_frame.pack(expand=True, fill="both", padx=20, pady=(5, 15))

        # Configurar 3 columnas adaptables para el scrollable frame
        for i in range(3):
            cards_frame.grid_columnconfigure(i, weight=1)

        col, row = 0, 0
        for key, cipher in self.algorithms.items():
            card = self.create_card(cards_frame, key, cipher)
            card.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")
            col += 1
            if col > 2:
                col = 0
                row += 1

    def create_card(self, parent, key, cipher):
        card = ctk.CTkFrame(
            parent, 
            corner_radius=15, 
            border_width=2, 
            border_color="#1f538d",
            fg_color="#1e1e1e"
        )

        icon_text = getattr(cipher, 'icon_symbol', '🔐')
        ctk.CTkLabel(card, text=icon_text, font=ctk.CTkFont(size=40)).pack(pady=(15, 5))
        ctk.CTkLabel(card, text=cipher.name, font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)
        ctk.CTkLabel(
            card, text=cipher.description, wraplength=190, 
            font=ctk.CTkFont(size=11), text_color="#9ca3af"
        ).pack(pady=5, padx=15, fill="both", expand=True)

        ctk.CTkButton(
            card, text="Iniciar ➔", command=lambda k=key: self.on_select(k)
        ).pack(pady=(10, 15))

        return card

    def destroy(self):
        if hasattr(self, 'bg_canvas'):
            self.bg_canvas.stop_animation()
        super().destroy()