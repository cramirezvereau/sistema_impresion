# formats/formato3.py (ejemplo con todos los tipos de validación)
from formats.base_format import BaseTicketFormat
from PIL import Image, ImageDraw, ImageFont

class FormatoAtencionOdontologica(BaseTicketFormat):
    """Formato 3: Atención Odontológica con todas las validaciones"""
    
    def get_format_name(self):
        return "Atención_Odontológica"
    
    def get_required_fields(self):
        """Campos requeridos para este formato"""
        return [
            {
                'name': 'dni',
                'label': 'DNI',
                'type': 'dni',
                'required': True,
                'width': 200,
                'tooltip': '8 dígitos numéricos'
            },
            {
                'name': 'nombre',
                'label': 'NOMBRE COMPLETO',
                'type': 'text',
                'required': True,
                'width': 400,
                'tooltip': 'Nombre y apellidos'
            },
            {
                'name': 'hora_ingreso',
                'label': 'HORA INGRESO',
                'type': 'hora',  # NUEVO: Campo de hora
                'required': True,
                'width': 120,
                'tooltip': 'Formato: HH:MM:SS (24h)'
            },
            {
                'name': 'fecha',
                'label': 'FECHA',
                'type': 'date',
                'required': True,
                'width': 180,
                'tooltip': 'Fecha de consulta'
            }
        ]
    
    def generate_image(self, data: dict, **kwargs):
        dni = data.get('dni', '')
        nombre = data.get('nombre', '')
        hora_ingreso = data.get('hora_ingreso', '')
        fecha = data.get('fecha', '')
        
        img = Image.new('RGB', (self.width_px, self.height_px), 'white')
        draw = ImageDraw.Draw(img)
        
        # Configurar fuentes
        try:
            font_title = ImageFont.truetype("arialbd.ttf", 20)
            font_normal = ImageFont.truetype("arial.ttf", 16)
            font_bold = ImageFont.truetype("arialbd.ttf", 18)
        except:
            font_title = ImageFont.load_default()
            font_normal = ImageFont.load_default()
            font_bold = ImageFont.load_default()
        
        y_position = 20
        center_x = self.width_px // 2
        
        # TÍTULO
        titulo = "ATENCIÓN ODONTOLÓGICA"
        text_width = draw.textlength(titulo, font=font_title)
        draw.text(((self.width_px - text_width) // 2, y_position), 
                 titulo, fill='black', font=font_title)
        y_position += 35
        
        # Línea separadora
        draw.line([(20, y_position), (self.width_px-20, y_position)], fill='black', width=2)
        y_position += 20
        
        # DATOS DEL PACIENTE
        # Fila 1: DNI
        draw.text((30, y_position), "DNI:", fill='black', font=font_bold)
        draw.text((100, y_position), dni if dni else "__________", 
                 fill='black', font=font_normal)
        y_position += 25
        
        # Fila 2: Nombre
        draw.text((30, y_position), "NOMBRE:", fill='black', font=font_bold)
        nombre_lines = self.wrap_text(nombre, 35)
        for line in nombre_lines:
            draw.text((120, y_position), line, fill='black', font=font_normal)
            y_position += 20
        if len(nombre_lines) == 1:
            y_position += 20
        
       
        
        
        
        # Fila 6: Fecha
        draw.text((30, y_position), "FECHA:", fill='black', font=font_bold)
        draw.text((130, y_position), fecha, fill='black', font=font_normal)
        y_position += 30
        
         # Fila 6: Fecha
        draw.text((30, y_position), "HORA:", fill='black', font=font_bold)
        draw.text((130, y_position), hora_ingreso, fill='black', font=font_normal)
        y_position += 30
        # Línea separadora
        draw.line([(20, y_position), (self.width_px-20, y_position)], fill='black', width=1)
        y_position += 120
        
        
        # FIRMA
        draw.line([(center_x - 100, y_position), (center_x + 100, y_position)], 
                 fill='black', width=1)
        y_position += 15
        draw.text((center_x - 40, y_position), "Firma del Médico", 
                 fill='black', font=font_bold)
        
        return img
    
    def wrap_text(self, text, max_length):
        """Dividir texto en líneas de máximo max_length caracteres"""
        if not text:
            return []
        
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            if len(' '.join(current_line + [word])) <= max_length:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines