# widgets/dynamic_list.py
import customtkinter as ctk

class DynamicListEntry(ctk.CTkFrame):
    """Widget para crear múltiples campos de texto con un botón '+'"""
    
    def __init__(self, parent, width=280, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.width = width
        self.entries = []
        
        # Contenedor para los inputs
        self.entries_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.entries_frame.pack(fill="x")
        
        # Agregar el primer input por defecto
        self.add_entry()
        
        # Botón de Agregar (Mejorado)
        self.add_btn = ctk.CTkButton(
            self, 
            text="+ Añadir Medicamento", 
            width=self.width, 
            height=28,  # Mismo alto que los inputs estándar
            font=("Segoe UI", 12, "bold"),
            fg_color=("#00bcd4", "#00838f"), # Azul agua para coincidir con la pestaña
            hover_color=("#0097a7", "#006064"),
            command=self.add_entry,
            corner_radius=4,
            anchor="center"  # Texto centrado
        )
        self.add_btn.pack(pady=(6, 0))

    def add_entry(self):
        # Límite de 6 medicamentos para que no se salga del ticket
        if len(self.entries) >= 6:
            return
            
        entry = ctk.CTkEntry(
            self.entries_frame, 
            width=self.width, 
            height=28, 
            font=("Segoe UI", 12),
            placeholder_text=f"Medicamento {len(self.entries) + 1}"
        )
        entry.pack(fill="x", pady=(0, 3))
        self.entries.append(entry)

    def get(self):
        """Devuelve todos los textos separados por el símbolo '|'"""
        vals = [e.get().strip() for e in self.entries if e.get().strip()]
        return "|".join(vals)

    def set(self, val):
        """Limpia la lista al usar el botón 'Limpiar'"""
        for e in self.entries:
            e.destroy()
        self.entries.clear()
        self.add_entry()