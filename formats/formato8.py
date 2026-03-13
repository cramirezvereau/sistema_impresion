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
            font_title = ImageFont.truetype("arialbd.ttf", 24)
            font_bold = ImageFont.truetype("arialbd.ttf", 24)
            # NUEVA FUENTE GIGANTE para los códigos numéricos
            font_valores = ImageFont.truetype("arial.ttf", 32) 
        except:
            font_title = font_bold = font_valores = ImageFont.load_default()
            
        y_pos = 20
        
        # ============================================
        # 1. ENCABEZADO - HOSPITAL 
        # ============================================
        hospital_text = "HOSPITAL BICENTENARIO DE CHAO"
        text_width_hospital = draw.textlength(hospital_text, font=font_title)
        
        x_hospital = (self.width_px - text_width_hospital) / 2
        draw.text((x_hospital, y_pos), hospital_text, fill='black', font=font_title)
        
        y_pos += 40 
        
        # ============================================
        # 2. COORDENADAS DE LA TABLA PRINCIPAL
        # ============================================
        x_inicio = 20
        x_fin = self.width_px - 40 
        
        # CABECERA: DNI PACIENTE
        draw.rectangle([(x_inicio, y_pos), (x_fin, y_pos + 100)], outline='black', width=3)
        
        tit_txt = "DNI PACIENTE"
        ancho_tit = draw.textlength(tit_txt, font=font_title)
        x_tit = x_inicio + ((x_fin - x_inicio - ancho_tit) / 2)
        draw.text((x_tit, y_pos + 15), tit_txt, fill='black', font=font_title)
        
        draw.line([(x_tit, y_pos + 45), (x_tit + ancho_tit, y_pos + 45)], fill='black', width=3)
        
        # DNI IMPRESO CON LA NUEVA FUENTE GRANDE
        ancho_dni = draw.textlength(dni, font=font_valores)
        draw.text((x_inicio + ((x_fin - x_inicio - ancho_dni) / 2), y_pos + 55), dni, fill='black', font=font_valores)
        
        y_pos += 100
        
        # FILAS INFERIORES (LAB, RX, CITA)
        col_div = x_inicio + 150 
        
        def dibujar_celda(y, titulo, valor):
            # Aumentamos el alto de la celda a 65 para que la letra gigante respire bien
            alto_celda = 65
            draw.rectangle([(x_inicio, y), (x_fin, y + alto_celda)], outline='black', width=3)
            draw.line([(col_div, y), (col_div, y + alto_celda)], fill='black', width=3)
            
            # Título (LAB, RX, CITA) se mantiene normal
            draw.text((x_inicio + 10, y + 18), titulo, fill='black', font=font_bold)
            
            # VALORES IMPRESOS CON LA LETRA GIGANTE (Centrados verticalmente)
            draw.text((col_div + 15, y + 14), valor, fill='black', font=font_valores)

        dibujar_celda(y_pos, "LAB", lab)
        y_pos += 65
        dibujar_celda(y_pos, "RX", rx)
        y_pos += 65
        dibujar_celda(y_pos, "CITA", cita)
        
        return img