# ui.py (interfaz más compacta)
import customtkinter as ctk
from tkinter import messagebox
from printer import PrinterManager
from formats.formato1 import FormatoEvaluacionRiesgo
from formats.formato2 import FormatoAtencionLaboratorio
from formats.formato3 import FormatoAtencionOdontologica
from formats.formato4 import FormatoPruebaVIHSifilis
from formats.formato5 import FormatoPruebaHepatitisB
from widgets.hora_widget import HoraEntry
import threading
import time
from tkcalendar import Calendar
from datetime import datetime
import os
import sys
from PIL import Image, ImageDraw,ImageFont
from typing import Dict, List
from formats.formato6 import FormatoHidratacion
from widgets.dynamic_list import DynamicListEntry
from formats.formato7 import FormatoReporteCamas
from formats.formato8 import FormatoEmeLaboratorio
from formats.formato9 import FormatoDescansoMedico
from widgets.radio_group import RadioGroupEntry
from widgets.autocomplete_widget import AutocompleteEntry
from widgets.api_dni_widget import DniApiEntry

def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class PrinterAppUI:
    def __init__(self, root):

       
        
        
        self.root = root
         # Configurar tema de customtkinter para mejor contraste
        ctk.set_appearance_mode("dark")  # "dark", "light", o "system"
        ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

        self.root.title("Sistema de Impresión EPSON TM-T20II")
        self.root.geometry("650x750")  # Reducido porque los campos serán más compactos
        self.root.resizable(False, False)
        
        # Inicializar gestores
        self.printer_manager = PrinterManager()
        self.formatos = {
            "formato1": FormatoEvaluacionRiesgo(),
            "formato2": FormatoAtencionLaboratorio(),
            "formato3": FormatoAtencionOdontologica(),
            "formato4": FormatoPruebaVIHSifilis(),
            "formato5": FormatoPruebaHepatitisB(),
            "formato6": FormatoHidratacion(),
            "formato7": FormatoReporteCamas(),
            "formato8": FormatoEmeLaboratorio(),
            "formato9": FormatoDescansoMedico()
        }
        
        # Variables
        self.current_format = "formato1"
        self.field_variables = {}
        self.fecha = ctk.StringVar()
        self.fecha.set(datetime.now().strftime('%d/%m/%Y'))
        
        # Diccionario para almacenar widgets especiales
        self.hora_widgets = {}
        self.combo_widgets = {}  # Nuevo diccionario para combos

        # Campos actuales
        self.current_fields = []
        
        self.setup_ui()
        self.load_printers()
        self.auto_verify_printer()
        
        # Cargar campos del formato por defecto
        self.load_format_fields("formato1")
    
    def setup_ui(self):
        # Frame principal CON scroll pero más compacto
        self.main_frame = ctk.CTkScrollableFrame(
            self.root,
            fg_color=("gray90", "gray13"),
            width=630,
            height=550  # Menos alto porque los campos son más compactos
        )
        self.main_frame.pack(fill="both", expand=True, padx=6, pady=6)
        
        # Header más compacto
        self.setup_compact_header()
        
        # Selector de formato compacto
        self.setup_compact_format_selector()
        
        # Frame para campos dinámicos más compacto
        self.data_frame = ctk.CTkFrame(self.main_frame, fg_color=("white", "gray20"), 
                                       corner_radius=8)
        self.data_frame.pack(fill="x", pady=(0, 6), padx=2)
        
        data_title = ctk.CTkLabel(self.data_frame, text="📝 DATOS", 
                                 font=("Segoe UI", 16, "bold"), anchor="w")
        data_title.pack(fill="x", padx=12, pady=(8, 4))
        
        # Contenedor de campos en GRID para más compacto
        self.fields_container = ctk.CTkFrame(self.data_frame, fg_color="transparent")
        self.fields_container.pack(fill="x", padx=10, pady=(0, 8))
        
        # Botones de acción compactos
        self.setup_compact_action_buttons()
        
        # Estado de impresora
        self.setup_status_section()
    
    def setup_compact_header(self):
        """Header más compacto sin imagen grande"""
        IMG_WIDTH = 630
        IMG_HEIGHT = 80  # Mucho más pequeño
        
        header_frame = ctk.CTkFrame(self.main_frame, fg_color=("white", "gray20"), 
                                   corner_radius=8)
        header_frame.pack(fill="x", pady=(0, 8), padx=2)
        
        # Título sin imagen de fondo
        titulo_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        titulo_frame.pack(fill="x", padx=10, pady=6)
        
        # Icono y título en línea
        icon_label = ctk.CTkLabel(
            titulo_frame,
            text="🖨️",
            font=("Segoe UI", 24)
        )
        icon_label.pack(side="left", padx=(0, 10))
        
        titulo = ctk.CTkLabel(
            titulo_frame,
            text="SISTEMA DE IMPRESIÓN EPSON TM-T20II",
            font=("Segoe UI", 18, "bold")
        )
        titulo.pack(side="left")
        
        # Subtítulo pequeño
        subtitulo = ctk.CTkLabel(
            header_frame,
            text="HB-CHAO - Impresión de Tickets",
            font=("Segoe UI", 12),
            text_color="gray"
        )
        subtitulo.pack(pady=(0, 6))
    
    def setup_compact_format_selector(self):
        """Selector de formato dinámico estilo pestañas"""
        selector_frame = ctk.CTkFrame(self.main_frame, fg_color=("white", "gray20"), 
                                    corner_radius=8)
        selector_frame.pack(fill="x", pady=(0, 8), padx=2)
        
        selector_title = ctk.CTkLabel(
            selector_frame, 
            text="FORMATO:", 
            font=("Segoe UI", 14, "bold"), 
            anchor="w"
        )
        selector_title.pack(fill="x", padx=12, pady=(8, 6))
        
        # Frame principal que contendrá todas las filas
        tabs_frame = ctk.CTkFrame(selector_frame, fg_color="transparent")
        tabs_frame.pack(fill="x", padx=10, pady=(0, 8))
        
        self.format_buttons = {}
        
        # Tu lista completa de formatos
        formatos_info = [
            ("formato1", "PCT-Evaluación Riesgo", ("#e74c3c", "#c0392b")),
            ("formato2", "LAB-Atención Laboratorio", ("#3498db", "#2980b9")),
            ("formato3", "ODONT-Registro Odontología", ("#9b59b6", "#8e44ad")),
            ("formato4", "PCT-VIH/Sífilis", ("#e67e22", "#d35400")),
            ("formato5", "PCT-Hepatitis B", ("#1abc9c", "#16a085")),
            ("formato6", "HOSP-Hidratación", ("#00bcd4", "#00838f")),
            ("formato7", "HOSP-Paciente", ("#d7ccc8", "#8d6e63")),    
            ("formato8", "EME-Laboratorio", ("#fbc02d", "#f57f17")),
            ("formato9", "MECO-Descanso", ("#4caf50", "#388e3c"))   
        ]
        
        inactive_bg_color = ("#ecf0f1", "#2c3e50")
        inactive_hover_color = ("#bdc3c7", "#34495e")
        inactive_text_color = ("#666666", "#aaaaaa")
        
        # LOGICA DINÁMICA: Crear filas de 3 botones automáticamente
        columnas_por_fila = 3
        current_row_frame = None
        
        for i, (key, text, color) in enumerate(formatos_info):
            # Si es el primer botón de una fila (0, 3, 6...), creamos un nuevo Frame
            if i % columnas_por_fila == 0:
                current_row_frame = ctk.CTkFrame(tabs_frame, fg_color="transparent")
                current_row_frame.pack(fill="x", pady=(0, 6)) # Espaciado vertical entre filas
                
            # Crear el botón y meterlo en la fila actual
            btn = ctk.CTkButton(
                current_row_frame,
                text=text,
                width=195,
                height=32,
                font=("Segoe UI", 12, "bold"),
                command=lambda k=key: self.switch_format(k),
                fg_color=color if key == "formato1" else inactive_bg_color,
                hover_color=color if key == "formato1" else inactive_hover_color,
                text_color="white" if key == "formato1" else inactive_text_color,
                corner_radius=6,
                anchor="center"
            )
            
            # Espaciado horizontal: A los dos primeros de cada fila les damos margen a la derecha
            if (i % columnas_por_fila) < (columnas_por_fila - 1):
                btn.pack(side="left", padx=(0, 8))
            else:
                btn.pack(side="left") # El último botón de la fila va sin margen
                
            self.format_buttons[key] = btn
    
    def switch_format(self, formato_key):
        """Cambiar entre formatos - TODOS LOS BOTONES FUNCIONAN COMO UNO SOLO"""
        if formato_key == self.current_format:
            return
        
        # Colores para cada formato cuando está activo
        active_colors = {
            "formato1": ("#e74c3c", "#c0392b"),
            "formato2": ("#3498db", "#2980b9"),
            "formato3": ("#9b59b6", "#8e44ad"),
            "formato4": ("#e67e22", "#d35400"),
            "formato5": ("#1abc9c", "#16a085"),
            "formato6": ("#00bcd4", "#00838f"),
            "formato7": ("#d7ccc8", "#8d6e63"),
            "formato8": ("#fbc02d", "#f57f17"),
            "formato9": ("#4caf50", "#388e3c")
        }
        
        # Colores unificados para estado inactivo
        inactive_bg_color = ("#ecf0f1", "#2c3e50")
        inactive_hover_color = ("#bdc3c7", "#34495e")
        inactive_text_color = ("#666666", "#aaaaaa")  # <-- Gris tenue
        
        # Actualizar TODOS los botones
        for key, btn in self.format_buttons.items():
            if key == formato_key:
                # Botón activo: color del formato + texto blanco
                btn.configure(
                    fg_color=active_colors[key],
                    hover_color=active_colors[key],
                    text_color="white"
                )
            else:
                # Botón inactivo: color gris + texto gris tenue
                btn.configure(
                    fg_color=inactive_bg_color,
                    hover_color=inactive_hover_color,
                    text_color=inactive_text_color  # <-- Gris tenue
                )
        
        # Cambiar formato actual
        self.current_format = formato_key
        
        # Cargar nuevos campos
        self.load_format_fields(formato_key)
    
    def load_format_fields(self, formato_key):
        """Cargar campos específicos del formato seleccionado - DISEÑO COMPACTO"""
        # Limpiar campos anteriores
        for widget in self.fields_container.winfo_children():
            widget.destroy()
        
        # Limpiar diccionario de widgets de hora y combos
        self.hora_widgets.clear()
        if hasattr(self, 'combo_widgets'):
            self.combo_widgets.clear()

        # Obtener formato
        formato = self.formatos.get(formato_key)
        if not formato:
            return
        
        # Obtener campos requeridos
        required_fields = formato.get_required_fields()
        self.current_fields = required_fields
        
        # ========================================================
        # 1. PRE-INICIALIZAR VARIABLES (Crucial para la API DNI)
        # ========================================================
        self.field_variables.clear()
        for field in required_fields:
            self.field_variables[field['name']] = ctk.StringVar()
        
        # Usar GRID para disposición más compacta
        row = 0
        col = 0
        max_cols = 2  # Máximo 2 campos por fila
        
        for field in required_fields:
            field_name = field['name']
            field_label = field['label']
            field_type = field.get('type', 'text')
            field_width = field.get('width', 280) 
            
            # Rescatar la variable pre-creada
            var = self.field_variables[field_name]
            
            # CREAR EL CONTENEDOR
            field_frame = ctk.CTkFrame(self.fields_container, fg_color="transparent")
            field_frame.grid(row=row, column=col, sticky="ew", padx=5, pady=4)
            
            # Dibujar la etiqueta (Solo si no es un campo vacío de relleno)
            if field_label:
                label = ctk.CTkLabel(
                    field_frame,
                    text=field_label,
                    font=("Segoe UI", 12, "bold"),
                    anchor="w",
                    height=20
                )
                label.pack(fill="x", pady=(0, 2))

            # ==========================================
            # EVALUAR LOS TIPOS DE CAMPO
            # ==========================================
            
            if field_type == 'api_dni':
                target_var_name = field.get('target', 'nombres')
                target_var = self.field_variables.get(target_var_name)
                
                widget = DniApiEntry(field_frame, target_var=target_var, width=field_width)
                widget.pack(fill="x", pady=(0, 2))
                self.field_variables[field_name] = widget
                
            elif field_type == 'radio':
                widget = RadioGroupEntry(field_frame, options=field.get('options', []), width=field_width)
                widget.pack(fill="x", pady=(0, 2))
                self.field_variables[field_name] = widget
                
            elif field_type == 'autocomplete':
                widget = AutocompleteEntry(field_frame, data_file="data/cie10.json", width=field_width)
                widget.pack(fill="x", pady=(0, 2))
                self.field_variables[field_name] = widget
                
            elif field_type == 'dynamic_list':
                widget = DynamicListEntry(field_frame, width=field_width)
                widget.pack(fill="x", pady=(0, 2))
                self.field_variables[field_name] = widget

            elif field_type == 'hora':
                hora_widget = HoraEntry(field_frame, variable=var, width=field_width, height=28)
                hora_widget.pack(fill="x", pady=(0, 2))
                self.hora_widgets[field_name] = hora_widget

            elif field_type == 'combo':
                options = field.get('options', [])
                option_values = [opt['value'] for opt in options]
                option_labels = [opt['label'] for opt in options]
                
                option_menu = ctk.CTkOptionMenu(
                    field_frame, values=option_labels, width=field_width, height=28,
                    font=("Segoe UI", 12), corner_radius=4,
                    fg_color=("white", "gray25"), button_color=("gray80", "gray30"),
                    button_hover_color=("gray70", "gray40"), dropdown_fg_color=("white", "gray20"),
                    dropdown_text_color=("black", "white"), dropdown_font=("Segoe UI", 11)
                )
                option_menu.pack(fill="x", pady=(0, 2))
                
                current_value = ctk.StringVar()
                def create_update_function(option_labels_list, option_values_list, target_var):
                    def update_func(selected_label):
                        if selected_label in option_labels_list:
                            index = option_labels_list.index(selected_label)
                            target_var.set(option_values_list[index])
                            current_value.set(option_values_list[index])
                    return update_func
                
                update_func = create_update_function(option_labels, option_values, var)
                option_menu.configure(command=update_func)
                
                if option_labels:
                    option_menu.set(option_labels[0])
                    var.set(option_values[0])
                    current_value.set(option_values[0])
                
                if not hasattr(self, 'combo_widgets'): self.combo_widgets = {}
                self.combo_widgets[field_name] = {
                    'widget': option_menu, 'values': option_values,
                    'labels': option_labels, 'current_value': current_value
                }

            elif field_type == 'date':
                entry_frame = ctk.CTkFrame(field_frame, fg_color="transparent", height=28)
                entry_frame.pack(fill="x")
                
                entry = ctk.CTkEntry(
                    entry_frame, textvariable=var, width=field_width, height=28,
                    font=("Segoe UI", 12), state="readonly"
                )
                entry.pack(side="left", fill="x", expand=True)
                
                if field_name == 'fecha':
                    var.set(self.fecha.get())
                else:
                    var.set(datetime.now().strftime('%d/%m/%Y'))
                
                calendar_btn = ctk.CTkButton(
                    entry_frame, text="📅", width=32, height=28, font=("Segoe UI", 14),
                    command=lambda fn=field_name: self.open_calendar_for_field(fn),
                )
                calendar_btn.pack(side="left", padx=(5, 0))

            else:
                # CAMPOS NORMALES (text, number, dni, etc.)
                if field_label:
                    entry = ctk.CTkEntry(
                        field_frame, textvariable=var, width=field_width, height=28,
                        font=("Segoe UI", 12), justify="left"
                    )
                    entry.pack(fill="x", pady=(0, 2))
                    
                    if field_type == 'dni': self.setup_dni_validation(entry, var)
                    elif field_type == 'number': self.setup_number_validation(entry, var)
                    elif field_type == 'edad': self.setup_edad_validation(entry, var)
                    elif field_type == 'single_letter': self.setup_single_letter_validation(entry, var)
                    elif field_type == 'sexo': self.setup_sexo_validation(entry, var)
                    else: self.setup_uppercase_binding(entry, var)

            # Tooltip
            tooltip = field.get('tooltip', '')
            if tooltip:
                tooltip_label = ctk.CTkLabel(
                    field_frame, text=tooltip, font=("Segoe UI", 10), text_color="gray", height=18
                )
                tooltip_label.pack(fill="x")

            # Actualizar posición en grid
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        # AGREGAR BOTÓN PARA HORA ACTUAL EN TODOS LOS CAMPOS
        if any(field.get('type') == 'hora' for field in required_fields):
            self.add_current_time_button(row + 1)        
        
        # Configurar pesos de columnas
        self.fields_container.grid_columnconfigure(0, weight=1)
        self.fields_container.grid_columnconfigure(1, weight=1)
        
    def add_current_time_button(self, row):
        """Agregar botón para establecer hora actual en todos los campos de hora"""
        hora_frame = ctk.CTkFrame(self.fields_container, fg_color="transparent")
        hora_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(10, 5))
        
        now_btn = ctk.CTkButton(
            hora_frame,
            text="🕒 Establecer hora actual en todos los campos de hora",
            height=30,
            font=("Segoe UI", 11),
            command=self.set_all_current_time,
            fg_color=("#2ecc71", "#27ae60"),
            hover_color=("#27ae60", "#229954")
        )
        now_btn.pack(fill="x")
        
        hora_frame.grid_columnconfigure(0, weight=1)
    
    def set_all_current_time(self):
        """Establecer hora actual en todos los campos de hora"""
        # Usar el método del widget personalizado
        for hora_widget in self.hora_widgets.values():
            hora_widget.set_current_time()
        
        messagebox.showinfo("Hora actual", "Hora actual establecida en todos los campos de hora")

    def setup_dni_validation(self, entry, variable):
        def validate_dni_input():
            current_text = variable.get()
            digits_only = ''.join(filter(str.isdigit, current_text))
            if len(digits_only) > 8:
                digits_only = digits_only[:8]
            if digits_only != current_text:
                variable.set(digits_only)
            
            if digits_only and len(digits_only) == 8:
                entry.configure(border_color="green")
            elif digits_only:
                entry.configure(border_color="orange")
            else:
                entry.configure(border_color=("gray75", "gray25"))
        
        variable.trace_add('write', lambda *args: validate_dni_input())
    
    def setup_number_validation(self, entry, variable):
        def validate_number_input():
            current_text = variable.get()
            digits_only = ''.join(filter(str.isdigit, current_text))
            if digits_only != current_text:
                variable.set(digits_only)
            
            if digits_only:
                entry.configure(border_color="green")
            else:
                entry.configure(border_color=("gray75", "gray25"))
        
        variable.trace_add('write', lambda *args: validate_number_input())
    
    def setup_edad_validation(self, entry, variable):
        def validate_edad_input():
            current_text = variable.get()
            digits_only = ''.join(filter(str.isdigit, current_text))
            
            if len(digits_only) > 3:
                digits_only = digits_only[:3]
            
            if digits_only != current_text:
                variable.set(digits_only)
            
            if digits_only:
                try:
                    edad = int(digits_only)
                    if 0 <= edad <= 100:
                        entry.configure(border_color="green")
                    else:
                        entry.configure(border_color="red")
                except:
                    entry.configure(border_color="red")
            else:
                entry.configure(border_color=("gray75", "gray25"))
        
        variable.trace_add('write', lambda *args: validate_edad_input())
    
    def setup_single_letter_validation(self, entry, variable):
        def validate_single_letter_input():
            current_text = variable.get()
            if len(current_text) > 1:
                current_text = current_text[:1]
                variable.set(current_text)
            
            if current_text and current_text != current_text.upper():
                variable.set(current_text.upper())
            
            if current_text:
                if current_text.isalpha() and len(current_text) == 1:
                    entry.configure(border_color="green")
                else:
                    entry.configure(border_color="orange")
            else:
                entry.configure(border_color=("gray75", "gray25"))
        
        variable.trace_add('write', lambda *args: validate_single_letter_input())
    
    def setup_sexo_validation(self, entry, variable):
        def validate_sexo_input():
            current_text = variable.get()
            
            if len(current_text) > 1:
                if current_text.upper() not in ['MASCULINO', 'FEMENINO']:
                    current_text = current_text[:1]
                    variable.set(current_text)
            
            if current_text and current_text != current_text.upper():
                variable.set(current_text.upper())
            
            if current_text:
                valid_values = ['M', 'F', 'H', 'MASCULINO', 'FEMENINO']
                if current_text.upper() in valid_values:
                    entry.configure(border_color="green")
                else:
                    entry.configure(border_color="orange")
            else:
                entry.configure(border_color=("gray75", "gray25"))
        
        variable.trace_add('write', lambda *args: validate_sexo_input())

    def setup_hora_validation(self, entry, variable):
        """Validación de hora en formato HH:MM:SS"""
        def validate_hora_input():
            current_text = variable.get()
            
            # Limpiar texto: solo números y :
            cleaned = ''.join(c for c in current_text if c.isdigit() or c == ':')
            
            # Autoformatear mientras se escribe
            if cleaned and ':' not in cleaned and len(cleaned) <= 6:
                # Autoinsertar : después de 2 y 4 dígitos
                formatted = cleaned
                if len(cleaned) > 2:
                    formatted = cleaned[:2] + ':' + cleaned[2:]
                if len(cleaned) > 4:
                    formatted = formatted[:5] + ':' + formatted[5:]
                if formatted != current_text:
                    variable.set(formatted[:8])  # Limitar a HH:MM:SS
            
            # Validar formato final
            final_text = variable.get()
            if final_text:
                # Patrón regex para HH:MM:SS
                import re
                pattern = r'^([01]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$'
                
                if re.match(pattern, final_text):
                    # Validar valores numéricos
                    try:
                        horas, minutos, segundos = map(int, final_text.split(':'))
                        if 0 <= horas <= 23 and 0 <= minutos <= 59 and 0 <= segundos <= 59:
                            entry.configure(border_color="green")
                        else:
                            entry.configure(border_color="red")
                    except:
                        entry.configure(border_color="red")
                else:
                    entry.configure(border_color="orange")
            else:
                entry.configure(border_color=("gray75", "gray25"))
        
        variable.trace_add('write', lambda *args: validate_hora_input())
    
    def setup_uppercase_binding(self, entry, variable):
        def force_uppercase(event=None):
            current = variable.get()
            if current != current.upper():
                variable.set(current.upper())
        entry.bind('<KeyRelease>', force_uppercase)
    
    def setup_compact_action_buttons(self):
        """Botones de acción más compactos"""
        action_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        action_frame.pack(fill="x", pady=6)
        
        # Frame para botones en línea
        buttons_row = ctk.CTkFrame(action_frame, fg_color="transparent")
        buttons_row.pack()
        
        # Botón de impresión
        print_btn = ctk.CTkButton(
            buttons_row,
            text="🖨️ IMPRIMIR",
            width=180,
            height=36,
            font=("Segoe UI", 14, "bold"),
            command=self.print_current_format,
            fg_color=("#27ae60", "#229954"),
            hover_color=("#229954", "#1e8449"),
            corner_radius=6
        )
        print_btn.pack(side="left", padx=(0, 10))
        
        # Botón de prueba
        test_btn = ctk.CTkButton(
            buttons_row,
            text="📄 PRUEBA",
            width=180,
            height=36,
            font=("Segoe UI", 14, "bold"),
            command=self.print_test,
            fg_color=("#f39c12", "#d68910"),
            hover_color=("#d68910", "#b9770e"),
            corner_radius=6
        )
        test_btn.pack(side="left")
        
        # Botón limpiar campos
        clear_btn = ctk.CTkButton(
            buttons_row,
            text="🗑️ LIMPIAR",
            width=180,
            height=36,
            font=("Segoe UI", 14, "bold"),
            command=self.clear_fields,
            fg_color=("#95a5a6", "#7f8c8d"),
            hover_color=("#7f8c8d", "#6c7b7d"),
            corner_radius=6
        )
        clear_btn.pack(side="left", padx=(10, 0))
    
    def clear_fields(self):
        """Limpiar todos los campos"""
        for var in self.field_variables.values():
            var.set("")
        self.fecha.set(datetime.now().strftime('%d/%m/%Y'))

                # Limpiar widgets de hora específicamente
        for hora_widget in self.hora_widgets.values():
            hora_widget.clear()
        
        self.fecha.set(datetime.now().strftime('%d/%m/%Y'))

        # Limpiar combos (establecer primera opción)
        if hasattr(self, 'combo_widgets'):
            for field_name, combo_info in self.combo_widgets.items():
                if combo_info['labels']:
                    combo_info['widget'].set(combo_info['labels'][0])
                    # Actualizar la variable del campo también
                    if field_name in self.field_variables:
                        self.field_variables[field_name].set(combo_info['values'][0])
                    combo_info['current_value'].set(combo_info['values'][0])


        # También actualizar variable de fecha si existe
        if 'fecha' in self.field_variables:
            self.field_variables['fecha'].set(self.fecha.get())
    
    def setup_status_section(self):
        """Estado de impresora compacto"""
        status_frame = ctk.CTkFrame(self.main_frame, fg_color=("white", "gray20"), 
                                    corner_radius=8, height=40)
        status_frame.pack(fill="x", pady=(6, 0), padx=2)
        status_frame.pack_propagate(False)  # Mantener altura fija
        
        status_content = ctk.CTkFrame(status_frame, fg_color="transparent")
        status_content.pack(fill="both", padx=12, pady=6)
        
        # Icono de estado
        self.status_icon = ctk.CTkLabel(
            status_content,
            text="●",
            font=("Segoe UI", 14),
            text_color="gray"
        )
        self.status_icon.pack(side="left", padx=(0, 8))
        
        # Texto de estado
        self.status_text = ctk.CTkLabel(
            status_content,
            text="Verificando impresora...",
            font=("Segoe UI", 12),
            text_color="gray"
        )
        self.status_text.pack(side="left")
        
        # Botón de verificación
        verify_btn = ctk.CTkButton(
            status_content,
            text="Verificar",
            width=80,
            height=28,
            font=("Segoe UI", 11),
            command=self.manual_verify_printer,
            fg_color=("#3498db", "#2980b9"),
            hover_color=("#2980b9", "#21618c")
        )
        verify_btn.pack(side="right")
    
    def manual_verify_printer(self):
        """Verificación manual de impresora"""
        self.update_printer_status(manual=True)
    
    def open_calendar(self):
        """Abrir calendario compacto"""
        cal_window = ctk.CTkToplevel(self.root)
        cal_window.title("Seleccionar Fecha")
        cal_window.geometry("280x320")  # Más pequeño
        cal_window.resizable(False, False)
        cal_window.transient(self.root)
        cal_window.grab_set()
        
        # Centrar ventana
        cal_window.update_idletasks()
        x = (cal_window.winfo_screenwidth() // 2) - 140
        y = (cal_window.winfo_screenheight() // 2) - 160
        cal_window.geometry(f"+{x}+{y}")
        
        # Calendario más compacto
        cal = Calendar(
            cal_window,
            selectmode='day',
            date_pattern='dd/mm/yyyy',
            font=('Segoe UI', 9)
        )
        cal.pack(padx=10, pady=10, fill="both", expand=True)
        
        def select_date():
            selected_date = cal.get_date()
            self.fecha.set(selected_date)
            
            # Actualizar todas las variables de fecha
            for field_name, var in self.field_variables.items():
                if 'fecha' in field_name.lower():
                    var.set(selected_date)
            
            cal_window.destroy()
        
        # Botones compactos
        button_frame = ctk.CTkFrame(cal_window, fg_color="transparent")
        button_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        accept_btn = ctk.CTkButton(
            button_frame,
            text="✓",
            width=40,
            height=30,
            font=("Segoe UI", 14),
            command=select_date,
            fg_color=("#27ae60", "#229954")
        )
        accept_btn.pack(side="left", padx=(0, 5), expand=True)
        
        today_btn = ctk.CTkButton(
            button_frame,
            text="Hoy",
            width=60,
            height=30,
            font=("Segoe UI", 11),
            command=lambda: cal.selection_set(datetime.now()),
            fg_color=("#3498db", "#2980b9")
        )
        today_btn.pack(side="left", padx=5, expand=True)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="✗",
            width=40,
            height=30,
            font=("Segoe UI", 14),
            command=cal_window.destroy,
            fg_color=("#e74c3c", "#c0392b")
        )
        cancel_btn.pack(side="left", padx=(5, 0), expand=True)
    
    def open_calendar_for_field(self, field_name):
        """Abrir calendario para un campo específico"""
        cal_window = ctk.CTkToplevel(self.root)
        cal_window.title(f"Seleccionar Fecha - {field_name}")
        cal_window.geometry("280x320")
        cal_window.resizable(False, False)
        cal_window.transient(self.root)
        cal_window.grab_set()
        
        # Centrar ventana
        cal_window.update_idletasks()
        x = (cal_window.winfo_screenwidth() // 2) - 140
        y = (cal_window.winfo_screenheight() // 2) - 160
        cal_window.geometry(f"+{x}+{y}")
        
        # Calendario
        cal = Calendar(
            cal_window,
            selectmode='day',
            date_pattern='dd/mm/yyyy',
            font=('Segoe UI', 9)
        )
        cal.pack(padx=10, pady=10, fill="both", expand=True)
        
        def select_date():
            selected_date = cal.get_date()
            # Actualizar solo la variable del campo específico
            if field_name in self.field_variables:
                self.field_variables[field_name].set(selected_date)
            
            cal_window.destroy()
        
        # Botones
        button_frame = ctk.CTkFrame(cal_window, fg_color="transparent")
        button_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        accept_btn = ctk.CTkButton(
            button_frame,
            text="✓",
            width=40,
            height=30,
            font=("Segoe UI", 14),
            command=select_date,
            fg_color=("#27ae60", "#229954")
        )
        accept_btn.pack(side="left", padx=(0, 5), expand=True)
        
        today_btn = ctk.CTkButton(
            button_frame,
            text="Hoy",
            width=60,
            height=30,
            font=("Segoe UI", 11),
            command=lambda: cal.selection_set(datetime.now()),
            fg_color=("#3498db", "#2980b9")
        )
        today_btn.pack(side="left", padx=5, expand=True)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="✗",
            width=40,
            height=30,
            font=("Segoe UI", 14),
            command=cal_window.destroy,
            fg_color=("#e74c3c", "#c0392b")
        )
        cancel_btn.pack(side="left", padx=(5, 0), expand=True)

    def load_printers(self):
        printer_name = self.printer_manager.load_printers()
        if printer_name:
            print(f"Impresora seleccionada: {printer_name}")
    
    def auto_verify_printer(self):
        self.root.after(200, self.update_printer_status)
    
    def update_printer_status(self, manual=False):
        success, status, color = self.printer_manager.verify_printer()
        
        if success:
            self.status_icon.configure(text="●", text_color="green")
            self.status_text.configure(text="IMPRESORA LISTA", text_color="green")
            if manual:
                messagebox.showinfo("Verificación", "Impresora conectada y lista")
        else:
            self.status_icon.configure(text="●", text_color="red")
            self.status_text.configure(text="IMPRESORA NO DISPONIBLE", text_color="red")
            if manual:
                messagebox.showwarning("Verificación", "No se pudo conectar a la impresora")
    
    def print_current_format(self):
        """Imprimir con el formato actual"""
        if not self.printer_manager.selected_printer:
            messagebox.showwarning("Advertencia", "Por favor seleccione una impresora")
            return
        
        # Obtener datos de los campos
        data = {}
        for field_name, var in self.field_variables.items():
            data[field_name] = var.get().strip()
        
        # Asegurar que la fecha esté actualizada
        if 'fecha' not in data or not data['fecha']:
            data['fecha'] = self.fecha.get()
        
        # Validar datos con el formato actual
        formato = self.formatos[self.current_format]
        is_valid, message = formato.validate_data(data)
        
        if not is_valid:
            messagebox.showwarning("Datos inválidos", message)
            return
        
        # Preguntar si desea guardar como PDF
        respuesta = messagebox.askyesno("Guardar PDF", 
                                       "¿Desea guardar una copia en PDF?\n\n"
                                       "Sí: Guardar PDF e imprimir\n"
                                       "No: Solo imprimir")
        
        # Iniciar impresión en hilo separado
        thread = threading.Thread(
            target=self._print_job,
            args=(self.current_format, data, respuesta)
        )
        thread.start()
    
    def print_test(self):
        """Imprimir prueba"""
        if not self.printer_manager.selected_printer:
            messagebox.showwarning("Advertencia", "Por favor seleccione una impresora")
            return
        
        thread = threading.Thread(
            target=self._print_job,
            args=("test", {}, False)
        )
        thread.start()
    
    def _print_job(self, formato_key, data: Dict, guardar_pdf):
        """Ejecutar trabajo de impresión"""
        progress_window = self.create_progress_window(formato_key == "test")
        
        try:
            self.update_progress(progress_window, "Preparando impresión...", 0.1)
            time.sleep(0.2)
            
            self.update_progress(progress_window, "Generando contenido...", 0.3)
            
            if formato_key == "test":
                img = self.generate_test_image()
                is_test = True
            else:
                formato = self.formatos.get(formato_key)
                if not formato:
                    raise Exception(f"Formato '{formato_key}' no encontrado")
                
                img = formato.generate_image(data=data)
                is_test = False
            
            if guardar_pdf and formato_key != "test":
                self.update_progress(progress_window, "Guardando PDF...", 0.6)
                formato.save_as_pdf(img, data)
            
            self.update_progress(progress_window, "Enviando a impresora...", 0.8)
            self.printer_manager.print_image(img, is_test)
            
            self.update_progress(progress_window, "¡Completado!", 1.0)
            time.sleep(0.3)
            
            progress_window.destroy()
            
            formato_nombre = self.formatos[formato_key].get_format_name() if formato_key != "test" else "Prueba"
            mensaje = f"{formato_nombre} impreso correctamente"
            if guardar_pdf and not is_test:
                mensaje += "\n✓ Copia guardada en PDF"
            
            self.root.after(0, lambda: messagebox.showinfo("Éxito", mensaje))
            
        except Exception as e:
            progress_window.destroy()
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error:\n{str(e)}"))
    
    def generate_test_image(self):
        formato = self.formatos["formato1"]
        img = Image.new('RGB', (formato.width_px, formato.height_px), 'white')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        textos = [
            "PRUEBA DE IMPRESORA",
            "EPSON TM-T20II",
            datetime.now().strftime('%d/%m/%Y %H:%M'),
            f"Formato: {self.current_format}"
        ]
        
        y = 60
        for texto in textos:
            text_width = draw.textlength(texto, font=font)
            x = (formato.width_px - text_width) // 2
            draw.text((x, y), texto, fill='black', font=font)
            y += 30
        
        return img
    
    def create_progress_window(self, is_test):
        """Ventana de progreso compacta"""
        progress = ctk.CTkToplevel(self.root)
        progress.title("Progreso")
        progress.geometry("300x140")  # Más compacta
        progress.resizable(False, False)
        progress.transient(self.root)
        progress.grab_set()
        
        progress.update_idletasks()
        x = (progress.winfo_screenwidth() // 2) - 150
        y = (progress.winfo_screenheight() // 2) - 70
        progress.geometry(f"+{x}+{y}")
        
        # Contenido compacto
        content = ctk.CTkFrame(progress, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=15)
        
        title = "🖨️ IMPRESIÓN DE PRUEBA" if is_test else "🖨️ IMPRIMIENDO"
        title_label = ctk.CTkLabel(
            content,
            text=title,
            font=("Segoe UI", 13, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        progress.status_label = ctk.CTkLabel(
            content,
            text="Iniciando...",
            font=("Segoe UI", 11)
        )
        progress.status_label.pack(pady=(0, 8))
        
        progress.progressbar = ctk.CTkProgressBar(
            content,
            width=200,
            height=8,
            corner_radius=4
        )
        progress.progressbar.pack()
        progress.progressbar.set(0)
        
        progress.percent_label = ctk.CTkLabel(
            content,
            text="0%",
            font=("Segoe UI", 11, "bold")
        )
        progress.percent_label.pack(pady=(5, 0))
        
        return progress
    
    def update_progress(self, window, status, value):
        window.status_label.configure(text=status)
        window.progressbar.set(value)
        window.percent_label.configure(text=f"{int(value*100)}%")
        window.update()