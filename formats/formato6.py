# formats/formato6.py
from formats.base_format import BaseTicketFormat
from PIL import Image, ImageDraw, ImageFont
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class FormatoHidratacion(BaseTicketFormat):
    """Formato 6: Ticket de Hidratación / Medicamentos"""
    
    def get_format_name(self):
        return "HOSP_Hidratacion"
    
    def get_required_fields(self):
        """Campos ordenados para generar la grilla 3x2 perfecta"""
        return [
            # --- FILA 1 ---
            {
                'name': 'nombre_paciente',
                'label': 'NOMBRES Y APELLIDOS',
                'type': 'text',
                'required': True,
                'width': 280,
                'tooltip': 'Nombre completo del paciente'
            },
            {
                'name': 'goteo',
                'label': 'GOTEO',
                'type': 'text',
                'required': True,
                'width': 280,
                'tooltip': 'Velocidad de goteo'
            },
            # --- FILA 2 ---
            {
                'name': 'responsable',
                'label': 'RESPONSABLE',
                'type': 'text',
                'required': True,
                'width': 280,
                'tooltip': 'Personal a cargo'
            },
            {
                'name': 'frasco',
                'label': 'FRASCO',
                'type': 'text',
                'required': True,
                'width': 280,
                'tooltip': 'Número o tipo de frasco'
            },
            # --- FILA 3 ---
            {
                'name': 'fecha',
                'label': 'FECHA',
                'type': 'date',
                'required': True,
                'width': 200,
                'tooltip': 'Fecha de registro'
            },
            {
                'name': 'medicamentos',
                'label': 'MEDICAMENTO / HIDRATACIÓN',
                'type': 'dynamic_list',
                'required': True,
                'width': 280,
                'tooltip': 'Lista de medicamentos'
            }
        ]
    
    def generate_image(self, data: dict, **kwargs):
        nombre = data.get('nombre_paciente', '')
        medicamentos_str = data.get('medicamentos', '')
        goteo = data.get('goteo', '')
        frasco = data.get('frasco', '')
        responsable = data.get('responsable', '')
        fecha = data.get('fecha', '')
        
        medicamentos = medicamentos_str.split('|') if medicamentos_str else []
        
        img = Image.new('RGB', (self.width_px, self.height_px), 'white')
        draw = ImageDraw.Draw(img)
        
        try:
            font_title = ImageFont.truetype("arialbd.ttf", 26)
            font_bold = ImageFont.truetype("arialbd.ttf", 22)
            font_normal = ImageFont.truetype("arial.ttf", 22)
        except:
            font_title = ImageFont.load_default()
            font_bold = ImageFont.load_default()
            font_normal = ImageFont.load_default()
            
        y_position = 20
        margen_x = 35  # Margen izquierdo y derecho ampliado
        
        # ================= LOGO Y TÍTULO =================
        try:
            logo_path = resource_path("images/logo.png")
            if os.path.exists(logo_path):
                logo_image = Image.open(logo_path)
                max_logo_height = 65
                logo_aspect_ratio = logo_image.width / logo_image.height
                new_logo_width = int(max_logo_height * logo_aspect_ratio)
                logo_image = logo_image.resize((new_logo_width, max_logo_height), Image.Resampling.LANCZOS)
                
                img.paste(logo_image, (margen_x, y_position))
                
                texto_x = margen_x + new_logo_width + 15
                draw.text((texto_x + 50, y_position), "HOSPITAL", fill='black', font=font_title)
                draw.text((texto_x, y_position + 35), "BICENTENARIO CHAO", fill='black', font=font_title)
                
                y_position += max_logo_height + 40
        except Exception as e:
            draw.text((margen_x, y_position), "HOSPITAL BICENTENARIO CHAO", fill='black', font=font_title)
            y_position += 60
            
        # ================= NOMBRES =================
        draw.text((margen_x, y_position), "NOMBRES Y APELLIDOS:", fill='black', font=font_bold)
        y_position += 35
        draw.text((margen_x, y_position), f"{nombre}", fill='black', font=font_normal)
        draw.line([(margen_x, y_position+30), (self.width_px - margen_x, y_position+30)], fill='black', width=1)
        y_position += 50
        
        # ================= MEDICAMENTOS =================
        draw.text((margen_x, y_position), "MEDICAMENTO/HIDRATACIÓN:", fill='black', font=font_bold)
        y_position += 40
        for med in medicamentos:
            draw.text((margen_x, y_position), f"- {med}", fill='black', font=font_normal)
            y_position += 30
            
        y_position += 30
        
        # ================= FUNCIÓN DE APOYO =================
        # Esta pequeña función dibuja la Etiqueta en Negrita y el Texto al lado en Normal
        def draw_bold_and_normal(x, y, label_bold, text_normal):
            # 1. Dibuja la parte en negrita
            draw.text((x, y), label_bold, fill='black', font=font_bold)
            # 2. Calcula cuánto espacio ocupó esa palabra
            ancho_label = draw.textlength(label_bold, font=font_bold)
            # 3. Dibuja el texto normal justo al lado (+8 pixeles de separación)
            draw.text((x + ancho_label + 8, y), text_normal, fill='black', font=font_normal)

        # ================= CAMPOS INFERIORES =================
        draw_bold_and_normal(margen_x, y_position, "GOTEO:", goteo)
        y_position += 45
        
        draw_bold_and_normal(margen_x, y_position, "FRASCO:", frasco)
        y_position += 45
        
        draw_bold_and_normal(margen_x, y_position, "RESPONSABLE:", responsable)
        y_position += 45
        
        draw_bold_and_normal(margen_x, y_position, "FECHA:", fecha)
        
        return img