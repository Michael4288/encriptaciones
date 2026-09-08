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
        
        num_cols = int(self.width / self.font_size)
        # Cada columna tiene: [posicion_y, velocidad, caracter]
        self.columns = [
            [random.randint(-self.height, 0), random.randint(2, 6), random.choice(self.symbols)] 
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

            # Dibuja el carácter con un tono tenue para no oscurecer la interfaz
            self.create_text(
                x, y, 
                text=char, 
                fill="#1e3a8a",  # Azul tenue criptográfico (puedes usar #15803d para verde matrix)
                font=("Courier", self.font_size, "bold"), 
                anchor="nw"
            )

            # Mover posición hacia abajo
            self.columns[i][0] += self.columns[i][1]

            # Reiniciar al llegar abajo
            if self.columns[i][0] > self.height:
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

        # 2. Contenedor de Interfaz (superpuesto con fondo transparente)
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        lbl_title = ctk.CTkLabel(
            content_frame, 
            text="Plataforma Educativa de Encriptación", 
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#ffffff"
        )
        lbl_title.pack(pady=(30, 10))

        lbl_subtitle = ctk.CTkLabel(
            content_frame, 
            text="Selecciona un algoritmo para visualizar su funcionamiento en tiempo real", 
            font=ctk.CTkFont(size=13),
            text_color="#9ca3af"
        )
        lbl_subtitle.pack(pady=(0, 20))

        # Grid de Tarjetas
        cards_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        cards_frame.pack(expand=True, fill="both", padx=30, pady=10)

        col, row = 0, 0
        for key, cipher in self.algorithms.items():
            card = self.create_card(cards_frame, key, cipher)
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            col += 1
            if col > 2:
                col = 0
                row += 1

        for i in range(3):
            cards_frame.grid_columnconfigure(i, weight=1)

    def create_card(self, parent, key, cipher):
        # Tarjeta con fondo oscuro semi-sólido para contrastar con la animación
        card = ctk.CTkFrame(
            parent, 
            corner_radius=15, 
            border_width=2, 
            border_color="#1f538d",
            fg_color="#1e1e1e"
        )

        ctk.CTkLabel(card, text=cipher.icon_symbol, font=ctk.CTkFont(size=45)).pack(pady=(20, 5))
        ctk.CTkLabel(card, text=cipher.name, font=ctk.CTkFont(size=17, weight="bold")).pack(pady=5)
        ctk.CTkLabel(
            card, text=cipher.description, wraplength=190, 
            font=ctk.CTkFont(size=12), text_color="#9ca3af"
        ).pack(pady=5, padx=15)

        ctk.CTkButton(
            card, text="Explorar ➔", command=lambda k=key: self.on_select(k)
        ).pack(pady=(15, 20))

        return card

    def destroy(self):
        # Detener animación antes de destruir la vista para liberar recursos
        if hasattr(self, 'bg_canvas'):
            self.bg_canvas.stop_animation()
        super().destroy()