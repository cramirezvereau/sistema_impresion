# widgets/autocomplete_widget.py
import customtkinter as ctk
import json
import os

class AutocompleteEntry(ctk.CTkEntry):
    """
    Buscador Estilo 'Google' Definitivo.
    Soluciona la ventana fantasma al cambiar de aplicación (Alt+Tab) 
    y se oculta automáticamente si mueves la ventana principal.
    """
    def __init__(self, parent, data_file, width=280, **kwargs):
        super().__init__(parent, width=width, height=26, font=("Segoe UI", 11), **kwargs)
        self.all_data = []
        self.load_data(data_file)
        
        self.dropdown = ctk.CTkToplevel(self)
        self.dropdown.withdraw() 
        self.dropdown.overrideredirect(True) 
        self.dropdown.attributes("-topmost", True) 
        
        self.list_frame = ctk.CTkScrollableFrame(
            self.dropdown, width=width-2, height=180, 
            corner_radius=0, fg_color=("white", "gray20"),
            border_width=1, border_color="gray"
        )
        self.list_frame.pack(fill="both", expand=True)
        
        # Eventos principales
        self.bind("<KeyRelease>", self._on_key_release)
        self.bind("<FocusOut>", self._on_focus_out)
        
        self._clicking_list = False
        self._mouse_in_dropdown = False 
        
        # Detectores de Mouse
        self.dropdown.bind("<Enter>", lambda e: self._set_mouse_in(True))
        self.dropdown.bind("<Leave>", lambda e: self._set_mouse_in(False))
        self.dropdown.bind("<MouseWheel>", self._prevent_bg_scroll)
        
        # --- NUEVO: Enganchar eventos a la ventana principal ---
        # Usamos after(100) para asegurar que la ventana principal ya cargó
        self.after(100, self._bind_toplevel_events)

    def _bind_toplevel_events(self):
        toplevel = self.winfo_toplevel()
        # Si la ventana principal se mueve, se oculta la lista flotante
        toplevel.bind("<Configure>", self._on_toplevel_configure, add="+")

    def _on_toplevel_configure(self, event):
        # Asegurarnos de que el evento viene de la ventana principal y no de un botón interno
        if event.widget == self.winfo_toplevel():
            self._hide_dropdown()

    def load_data(self, filename):
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    self.all_data = json.load(f)
            except: self.all_data = []

    def _set_mouse_in(self, val):
        self._mouse_in_dropdown = val

    def _prevent_bg_scroll(self, event):
        return "break"

    def _on_key_release(self, event):
        if event.keysym in ("Up", "Down", "Return", "Escape"): return
            
        typed = self.get().strip().lower()
        if len(typed) < 2:
            self._hide_dropdown()
            return
            
        matches = []
        for item in self.all_data:
            cod = item['codigo'].lower()
            desc = item['descripcion'].lower()
            if typed in cod or typed in desc:
                matches.append(item)
                if len(matches) >= 40: break 

        if matches:
            self._show_dropdown(matches)
        else:
            self._hide_dropdown()

    def _show_dropdown(self, matches):
        for widget in self.list_frame.winfo_children(): widget.destroy()
            
        for item in matches:
            text_full = f"{item['codigo']} - {item['descripcion']}"
            text_display = text_full if len(text_full) <= 45 else text_full[:42] + "..."
            
            btn = ctk.CTkButton(
                self.list_frame, 
                text=text_display,      
                font=("Segoe UI", 11),
                anchor="w",             
                fg_color="transparent", 
                text_color=("black", "white"),
                hover_color=("gray85", "gray30"),
                height=24,
                corner_radius=0,
                command=lambda t=text_full: self._on_select(t)
            )
            btn.bind("<Button-1>", lambda e: self._set_clicking_flag(True))
            btn.pack(fill="x", pady=0, padx=5) 

        x = self.winfo_rootx()
        y = self.winfo_rooty()
        height = self.winfo_height()
        width = self.winfo_width()
        
        self.dropdown.geometry(f"{width}x180+{x}+{y+height}")
        self.dropdown.deiconify()

    def _on_select(self, text):
        self._set_clicking_flag(False)
        self.delete(0, "end")
        self.insert(0, text)
        self._hide_dropdown()
        self.focus_set()

    def _hide_dropdown(self):
        self.dropdown.withdraw()

    def _set_clicking_flag(self, val): 
        self._clicking_list = val

    def _on_focus_out(self, event):
        def check_and_hide():
            # --- LA MAGIA ESTÁ AQUÍ ---
            # focus_displayof() devuelve 'None' si te cambiaste a Chrome, Gemini o al Escritorio
            active_widget = self.focus_displayof()
            
            if active_widget is None:
                # El usuario se fue a otra aplicación
                self._hide_dropdown()
            elif not self._clicking_list and not self._mouse_in_dropdown:
                # El usuario hizo clic en otro lado dentro de nuestro programa
                self._hide_dropdown()
            elif self._mouse_in_dropdown:
                # El usuario está moviendo el scrollbar, le devolvemos el foco al input
                self.focus_set()
                
        self.after(100, check_and_hide)

    def clear(self):
        self.delete(0, "end")
        self._hide_dropdown()