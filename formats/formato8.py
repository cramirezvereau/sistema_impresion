# formats/formato8.py
from formats.base_format import BaseTicketFormat
from PIL import Image, ImageDraw, ImageFont

class FormatoEmeLaboratorio(BaseTicketFormat):
    """Formato: EME-Laboratorio (Grilla DNI)"""
    
    def get_format_name(self):
        return "EME_Laboratorio"
    
    def get_required_fields(self):
        return [
            {'name': 'dni', 'label': 'DNI PACIENTE', 'type': 'dni', 'required': True, 'width': 400},
            {'name': 'lab', 'label': 'LAB', 'type': 'text', 'required': False, 'width': 400},
            {'name': 'rx', 'label': 'RX', 'type': 'text', 'required': False, 'width': 400},
            {'name': 'cita', 'label': 'CITA', 'type': 'text', 'required': False, 'width': 400}
        ]
    
    def generate_image(self, data: dict, **kwargs):
        dni = data.get('dni', '')
        lab = data.get('lab', '')
        rx = data.get('rx', '')
        cita = data.get('cita', '')
        
        img = Image.new('RGB', (self.width_px, self.height_px), 'white')
        draw = ImageDraw.Draw(img)
        
        try:
            font_title = ImageFont.truetype("arialbd.ttf", 26)
            font_bold = ImageFont.truetype("arialbd.ttf", 24)
            font_normal = ImageFont.truetype("arial.ttf", 24)
        except:
            font_title = font_bold = font_normal = ImageFont.load_default()
            
        # Coordenadas de la tabla principal
        x_inicio, y_inicio = 20, 20
        x_fin = self.width_px - 20
        y_pos = y_inicio
        
        # CABECERA: DNI PACIENTE
        draw.rectangle([(x_inicio, y_pos), (x_fin, y_pos + 100)], outline='black', width=2)
        # Texto centrado y subrayado
        tit_txt = "DNI PACIENTE"
        ancho_tit = draw.textlength(tit_txt, font=font_title)
        x_tit = x_inicio + ((x_fin - x_inicio - ancho_tit) / 2)
        draw.text((x_tit, y_pos + 15), tit_txt, fill='black', font=font_title)
        # Línea de subrayado
        draw.line([(x_tit, y_pos + 45), (x_tit + ancho_tit, y_pos + 45)], fill='black', width=2)
        
        # Valor del DNI centrado
        ancho_dni = draw.textlength(dni, font=font_normal)
        draw.text((x_inicio + ((x_fin - x_inicio - ancho_dni) / 2), y_pos + 60), dni, fill='black', font=font_normal)
        
        y_pos += 100
        
        # FILAS INFERIORES (LAB, RX, CITA)
        col_div = x_inicio + 150 # Donde se parte la columna
        
        def dibujar_celda(y, titulo, valor):
            # Dibujar contorno de fila
            draw.rectangle([(x_inicio, y), (x_fin, y + 60)], outline='black', width=2)
            # Línea divisoria de columna
            draw.line([(col_div, y), (col_div, y + 60)], fill='black', width=2)
            # Textos
            draw.text((x_inicio + 10, y + 15), titulo, fill='black', font=font_bold)
            draw.text((col_div + 10, y + 15), valor, fill='black', font=font_normal)

        dibujar_celda(y_pos, "LAB", lab)
        y_pos += 60
        dibujar_celda(y_pos, "RX", rx)
        y_pos += 60
        dibujar_celda(y_pos, "CITA", cita)
        
        return img