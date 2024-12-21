import customtkinter as ctk
import os

class Calculator(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x600")
        if os.path.exists("calculadora.ico"):
            self.iconbitmap('calculadora.ico')
        else:
            self.iconbitmap("calculadora/calculadora.ico")
        self.resizable(True, True) # Responsive Design
        self.title("Calculadora con Tkinter")
        ctk.set_appearance_mode("dark")
        
        self.bg_color = "#202020"
        self.button_color = "#303030"
        self.accent_color = "#ff4c69"
        
        self.configure(fg_color=self.bg_color)
        self.current_expression = "0"
        self.current_font_size = 64
        self.create_widgets()

    def create_widgets(self):
        # Pantalla
        display_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
        display_frame.pack(fill="x", padx=20, pady=(40, 10))

        # Signo Igual
        equal_sign = ctk.CTkLabel(display_frame, text="=", font=("Arial", 45), 
                                  text_color=self.accent_color)
        equal_sign.pack(side="left", padx=(0, 10))

        # Pantalla de Resultado
        self.result = ctk.CTkEntry(display_frame, font=("Arial", 64), 
                                   fg_color=self.bg_color, text_color="white", 
                                   border_width=0, justify="right",
                                   )
        self.result.pack(fill="x", expand=True)
        self.result.insert(0, "0")
        self.result.configure(state="readonly")

        # Pantalla de Operaciones
        self.operation = ctk.CTkLabel(self, text="", font=("Arial", 24), 
                                      fg_color=self.bg_color, text_color=self.accent_color, 
                                      anchor="e")
        self.operation.pack(pady=(0, 40), padx=20, fill="x")

        # Botones
        button_frame = ctk.CTkFrame(self, fg_color=self.bg_color)
        button_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        buttons = [
            'CE', '+/-', '%', '/',
            '7', '8', '9', '*',
            '4', '5', '6', '-',
            '1', '2', '3', '+',
            '0', '.', '=', 
        ]

        row, col = 0, 0
        for button in buttons:
            if button in ['CE', '+/-', '%', '/', '*', '-', '+', '=']:
                color = self.accent_color
                text_color = "black"
                hover_color = self.lighten_color(self.accent_color, 0.1)
            else:
                color = self.button_color
                text_color = "white"
                hover_color = self.lighten_color(self.button_color, 0.1)
            
            btn = ctk.CTkButton(button_frame, text=button, 
                                fg_color=color, text_color=text_color, 
                                font=("Arial", 24), corner_radius=10,
                                hover_color=hover_color,
                                command=lambda x=button: self.button_click(x))
            
            # Boton 0.
            if button == '0':
                btn.grid(row=row, column=col, columnspan=2, padx=5, pady=5, sticky="nsew")
                col += 2
            else:
                btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                col += 1
            
            if col > 3:
                col = 0
                row += 1

        # Configurar filas y columnas para que se expandan.
        for i in range(5):
            button_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            button_frame.grid_columnconfigure(i, weight=1)

    def lighten_color(self, color, factor=0.1):
        # Convertir HEX a RGB
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        
        # Efecto Hover
        new_rgb = [min(int(c + (255 - c) * factor), 255) for c in rgb]
        
        # Convertir back a HEX
        return '#{:02x}{:02x}{:02x}'.format(*new_rgb)

    def button_click(self, key):
        if key == "=":
            self.calculate()
        elif key == "CE":
            self.clear()
        elif key == "+/-":
            self.negate()
        elif key == "%":
            self.percentage()
        else:
            self.add_to_expression(key)

    def add_to_expression(self, value):
        if self.current_expression == "0" or self.current_expression == "":
            self.current_expression = str(value)
        else:
            self.current_expression += str(value)
        self.update_result()
        self.update_operation()

    def update_operation(self):
        self.operation.configure(text=self.current_expression)

    def calculate(self):
        try:
            result = eval(self.current_expression)
            self.current_expression = str(result)
        except:
            self.current_expression = "Error"
        self.update_result()
        self.update_operation()

    def clear(self):
        self.current_expression = "0"
        self.update_result()
        self.update_operation()

    def negate(self):
        try:
            value = float(self.result.get())
            self.current_expression = str(-value)
        except ValueError:
            pass
        self.update_result()
        self.update_operation()

    def percentage(self):
        try:
            value = float(self.result.get())
            self.current_expression = str(value / 100)
        except ValueError:
            pass
        self.update_result()
        self.update_operation()

    def update_result(self):
        self.result.configure(state="normal")
        self.result.delete(0, ctk.END)
        self.result.insert(0, self.current_expression)
        
        # Ajustar el tamaño del texto
        text_length = len(self.current_expression)
        if text_length > 7:
            new_font_size = 40  # Texto pequeño para texto largo.
        else:
            new_font_size = 64  # Texto grande para texto de menos 7 digitos.
        
        self.result.configure(font=("Arial", new_font_size))
        self.result.configure(state="readonly")

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
