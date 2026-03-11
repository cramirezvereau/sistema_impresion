import customtkinter as ctk

class RadioGroupEntry(ctk.CTkFrame):
    """Widget para opciones de selección única (agrega una X en el ticket)"""
    def __init__(self, parent, options, width=280, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.variable = ctk.StringVar(value="")
        
        for opt in options:
            rb = ctk.CTkRadioButton(
                self, 
                text=opt, 
                variable=self.variable, 
                value=opt,
                font=("Segoe UI", 12)
            )
            rb.pack(anchor="w", pady=3)
            
    def get(self): return self.variable.get()
    def set(self, val): self.variable.set(val)
    def clear(self): self.variable.set("")