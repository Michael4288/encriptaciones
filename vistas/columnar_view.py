import customtkinter as ctk
import time

class ColumnarWorkspaceView(ctk.CTkFrame):
    def __init__(self, parent, cipher_instance, on_back_callback):
        super().__init__(parent, fg_color="transparent")
        self.cipher = cipher_instance
        self.on_back = on_back_callback
        self.cell_widgets = {}

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
        self.entry_text.insert(0, "MENSAJESECRETO")
        self.entry_text.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(ctrl_frame, text="Columnas:").grid(row=0, column=2, padx=10, pady=10)
        self.entry_cols = ctk.CTkEntry(ctrl_frame, width=60)
        self.entry_cols.insert(0, "4")
        self.entry_cols.grid(row=0, column=3, padx=10, pady=10)

        ctk.CTkButton(
            ctrl_frame, text="Iniciar Animación", command=self.run_animation
        ).grid(row=0, column=4, padx=20, pady=10)

        # Panel de la Matriz Visual
        self.matrix_container = ctk.CTkFrame(self, fg_color="#1a1a1a")
        self.matrix_container.pack(fill="both", expand=True, padx=20, pady=15)

        # Explicación y Salida
        res_frame = ctk.CTkFrame(self)
        res_frame.pack(fill="x", padx=20, pady=10)

        self.lbl_explanation = ctk.CTkLabel(
            res_frame, text="Configura las columnas y presiona 'Iniciar Animación'.", 
            font=ctk.CTkFont(size=14)
        )
        self.lbl_explanation.pack(pady=10)

        self.lbl_result = ctk.CTkLabel(
            res_frame, text="", font=ctk.CTkFont(size=24, weight="bold"), text_color="#3B82F6"
        )
        self.lbl_result.pack(pady=(0, 10))

    def render_matrix(self, matrix, rows, cols):
        for widget in self.matrix_container.winfo_children():
            widget.destroy()

        self.cell_widgets.clear()

        # Renderizado de encabezados de columna
        for c in range(cols):
            lbl_header = ctk.CTkLabel(
                self.matrix_container, text=f"COL {c+1}", 
                font=ctk.CTkFont(size=11, weight="bold"), text_color="#3B82F6"
            )
            lbl_header.grid(row=0, column=c, padx=6, pady=(15, 5))

        # Renderizado de la matriz de caracteres
        for r in range(rows):
            for c in range(cols):
                char = matrix[r][c]
                cell = ctk.CTkLabel(
                    self.matrix_container, text=char, width=45, height=45,
                    fg_color="#2b2b2b", corner_radius=6, font=ctk.CTkFont(size=16, weight="bold")
                )
                cell.grid(row=r+1, column=c, padx=6, pady=6)
                self.cell_widgets[(r, c)] = cell

    def run_animation(self):
        text = self.entry_text.get()
        cols_str = self.entry_cols.get()

        steps = self.cipher.encrypt_steps(text, cols_str)
        if not steps:
            return

        # Dibujar matriz limpia
        first_step = steps[0]
        self.render_matrix(first_step['matrix'], first_step['rows'], first_step['cols'])

        for step in steps:
            # Limpiar resaltados previos
            for cell in self.cell_widgets.values():
                cell.configure(fg_color="#2b2b2b")

            # Resaltar la casilla actual
            r, c = step['active_pos']
            if (r, c) in self.cell_widgets:
                self.cell_widgets[(r, c)].configure(fg_color="#10b981")

            self.lbl_explanation.configure(text=step['explanation'])
            self.lbl_result.configure(text=step['current_result'])
            self.update()
            time.sleep(0.5)