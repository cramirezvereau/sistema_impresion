# widgets/hora_widget.py
import customtkinter as ctk
from datetime import datetime

class HoraEntry(ctk.CTkFrame):
    """Widget personalizado para entrada de hora con formato HH:MM:SS"""
    
    def __init__(self, parent, variable=None, width=200, height=32, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        
        self.variable = variable or ctk.StringVar()
        self.width = width
        self.height = height
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="x", expand=True)
        
        # Variables para cada parte
        self.hh_var = ctk.StringVar(value="00")
        self.mm_var = ctk.StringVar(value="00")
        self.ss_var = ctk.StringVar(value="00")
        
        # Configurar el ancho de cada campo
        entry_width = 45
        
        # Campo HH (horas)
        self.hh_entry = ctk.CTkEntry(
            self.main_frame,
            textvariable=self.hh_var,
            width=entry_width,
            height=self.height,
            font=("Segoe UI", 12),
            justify="center",
            placeholder_text="HH"
        )
        self.hh_entry.pack(side="left")
        
        # Separador
        ctk.CTkLabel(
            self.main_frame, 
            text=":", 
            font=("Segoe UI", 14),
            text_color=("gray40", "gray60")
        ).pack(side="left", padx=2)
        
        # Campo MM (minutos)
        self.mm_entry = ctk.CTkEntry(
            self.main_frame,
            textvariable=self.mm_var,
            width=entry_width,
            height=self.height,
            font=("Segoe UI", 12),
            justify="center",
            placeholder_text="MM"
        )
        self.mm_entry.pack(side="left")
        
        # Separador
        ctk.CTkLabel(
            self.main_frame, 
            text=":", 
            font=("Segoe UI", 14),
            text_color=("gray40", "gray60")
        ).pack(side="left", padx=2)
        
        # Campo SS (segundos)
        self.ss_entry = ctk.CTkEntry(
            self.main_frame,
            textvariable=self.ss_var,
            width=entry_width,
            height=self.height,
            font=("Segoe UI", 12),
            justify="center",
            placeholder_text="SS"
        )
        self.ss_entry.pack(side="left")
        
        # Botón para hora actual
        self.now_btn = ctk.CTkButton(
            self.main_frame,
            text="🕒",
            width=36,
            height=self.height,
            font=("Segoe UI", 13),
            command=self.set_current_time,
            fg_color=("#3498db", "#2980b9"),
            hover_color=("#2980b9", "#21618c")
        )
        self.now_btn.pack(side="left", padx=(8, 0))
        
        # Configurar validaciones
        self.setup_validation()
        
        # Vincular con variable principal
        self.setup_variable_binding()
        
        # Establecer hora actual por defecto
        self.set_current_time()
    
    def setup_validation(self):
        """Configurar validación para cada campo de hora"""
        
        def validate_hours(*args):
            text = self.hh_var.get()
            if text:
                # Solo números
                if not text.isdigit():
                    self.hh_var.set(''.join(filter(str.isdigit, text)))
                    return
                
                # Limitar a 2 dígitos
                if len(text) > 2:
                    self.hh_var.set(text[:2])
                
                # Validar rango 00-23
                if text.isdigit():
                    horas = int(text)
                    if horas < 0 or horas > 23:
                        self.hh_entry.configure(border_color="red")
                    else:
                        self.hh_entry.configure(border_color="green")
                        # Auto-completar con 0
                        if len(text) == 1:
                            self.hh_var.set(f"0{text}")
                else:
                    self.hh_entry.configure(border_color=("gray75", "gray25"))
            else:
                self.hh_entry.configure(border_color=("gray75", "gray25"))
        
        def validate_minutes_seconds(var, entry, max_val):
            def validator(*args):
                text = var.get()
                if text:
                    # Solo números
                    if not text.isdigit():
                        var.set(''.join(filter(str.isdigit, text)))
                        return
                    
                    # Limitar a 2 dígitos
                    if len(text) > 2:
                        var.set(text[:2])
                    
                    # Validar rango 00-59
                    if text.isdigit():
                        valor = int(text)
                        if valor < 0 or valor > 59:
                            entry.configure(border_color="red")
                        else:
                            entry.configure(border_color="green")
                            # Auto-completar con 0
                            if len(text) == 1:
                                var.set(f"0{text}")
                    else:
                        entry.configure(border_color=("gray75", "gray25"))
                else:
                    entry.configure(border_color=("gray75", "gray25"))
            
            return validator
        
        # Configurar traces
        self.hh_var.trace_add('write', validate_hours)
        self.mm_var.trace_add('write', validate_minutes_seconds(self.mm_var, self.mm_entry, 59))
        self.ss_var.trace_add('write', validate_minutes_seconds(self.ss_var, self.ss_entry, 59))
    
    def setup_variable_binding(self):
        """Vincular las variables individuales con la variable principal"""
        
        def update_main_variable(*args):
            hh = self.hh_var.get().zfill(2)
            mm = self.mm_var.get().zfill(2)
            ss = self.ss_var.get().zfill(2)
            
            # Solo actualizar si todos tienen valores válidos
            if (hh.isdigit() and 0 <= int(hh) <= 23 and
                mm.isdigit() and 0 <= int(mm) <= 59 and
                ss.isdigit() and 0 <= int(ss) <= 59):
                hora_completa = f"{hh}:{mm}:{ss}"
                if self.variable.get() != hora_completa:
                    self.variable.set(hora_completa)
        
        # Actualizar cuando cambie cualquier campo
        self.hh_var.trace_add('write', update_main_variable)
        self.mm_var.trace_add('write', update_main_variable)
        self.ss_var.trace_add('write', update_main_variable)
        
        # También actualizar desde la variable principal hacia los campos
        if self.variable:
            def sync_from_main(*args):
                main_value = self.variable.get()
                if main_value and ':' in main_value:
                    try:
                        parts = main_value.split(':')
                        if len(parts) == 3:
                            hh, mm, ss = parts
                            if hh.isdigit() and mm.isdigit() and ss.isdigit():
                                if self.hh_var.get() != hh:
                                    self.hh_var.set(hh)
                                if self.mm_var.get() != mm:
                                    self.mm_var.set(mm)
                                if self.ss_var.get() != ss:
                                    self.ss_var.set(ss)
                    except:
                        pass
            
            self.variable.trace_add('write', sync_from_main)
    
    def set_current_time(self):
        """Establecer la hora actual del sistema"""
        now = datetime.now()
        self.hh_var.set(str(now.hour).zfill(2))
        self.mm_var.set(str(now.minute).zfill(2))
        self.ss_var.set(str(now.second).zfill(2))
    
    def get_hora(self):
        """Obtener la hora en formato HH:MM:SS"""
        hh = self.hh_var.get().zfill(2)
        mm = self.mm_var.get().zfill(2)
        ss = self.ss_var.get().zfill(2)
        return f"{hh}:{mm}:{ss}"
    
    def set_hora(self, hora_str):
        """Establecer la hora desde un string HH:MM:SS"""
        if hora_str and ':' in hora_str:
            parts = hora_str.split(':')
            if len(parts) == 3:
                hh, mm, ss = parts
                if hh.isdigit() and 0 <= int(hh) <= 23:
                    self.hh_var.set(hh.zfill(2))
                if mm.isdigit() and 0 <= int(mm) <= 59:
                    self.mm_var.set(mm.zfill(2))
                if ss.isdigit() and 0 <= int(ss) <= 59:
                    self.ss_var.set(ss.zfill(2))
    
    def clear(self):
        """Limpiar todos los campos"""
        self.hh_var.set("00")
        self.mm_var.set("00")
        self.ss_var.set("00")