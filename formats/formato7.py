# formats/formato7.py
from formats.base_format import BaseTicketFormat
from PIL import Image, ImageDraw, ImageFont

class FormatoReporteCamas(BaseTicketFormat):
    """Formato: Reporte de Pacientes de Hospitalización"""
    
    def get_format_name(self):
        return "HOSP_Reporte_Camas"
    
    def get_required_fields(self):
        return [
            # Fila 1
            {'name': 'fecha', 'label': 'FECHA', 'type': 'date', 'required': True, 'width': 200},
            {'name': 'ginecologia', 'label': 'GINECOLOGÍA', 'type': 'number', 'required': True, 'width': 280},
            # Fila 2
            {'name': 'cirugia', 'label': 'CIRUGÍA', 'type': 'number', 'required': True, 'width': 280},
            {'name': 'medicina', 'label': 'MEDICINA', 'type': 'number', 'required': True, 'width': 280},
            # Fila 3
            {'name': 'pediatria', 'label': 'PEDIATRÍA', 'type': 'number', 'required': True, 'width': 280}
        ]
    
    def generate_image(self, data: dict, **kwargs):
        fecha = data.get('fecha', '')
        gine = int(data.get('ginecologia') or 0)
        ciru = int(data.get('cirugia') or 0)
        medi = int(data.get('medicina') or 0)
        pedi = int(data.get('pediatria') or 0)
        
        total = gine + ciru + medi + pedi
        
        img = Image.new('RGB', (self.width_px, self.height_px), 'white')
        draw = ImageDraw.Draw(img)
        
        try:
            font_title = ImageFont.truetype("arialbd.ttf", 22)
            font_bold = ImageFont.truetype("arialbd.ttf", 20)
            font_normal = ImageFont.truetype("arial.ttf", 20)
        except:
            font_title = font_bold = font_normal = ImageFont.load_default()
        
        margen_x = 20        # ← Margen izquierdo
        margen_derecho = 100 # ← Margen derecho
        ancho_util = self.width_px - margen_derecho  # Ancho útil de contenido
        
        y_pos = 20
        # Título
        draw.text((margen_x, y_pos), "REPORTE DE PACIENTES DE", fill='black', font=font_title)
        y_pos += 30
        draw.text((margen_x, y_pos), "HOSPITALIZACION", fill='black', font=font_title)
        y_pos += 40
        
        # Fecha y Total
        draw.text((margen_x, y_pos), f"FECHA: {fecha}", fill='black', font=font_bold)
        y_pos += 40
        draw.text((margen_x, y_pos), f"TOTAL DE CAMAS OCUPADAS = {total}", fill='black', font=font_bold)
        y_pos += 60
        
        # Función para dibujar las filas con óvalos
        def dibujar_fila(y, etiqueta, valor):
            draw.text((margen_x, y + 10), etiqueta, fill='black', font=font_bold)
            
            # Óvalo posicionado relativo al ancho útil
            oval_x1 = margen_x + 210
            oval_x2 = margen_x + 420
            oval_centro = (oval_x1 + oval_x2) // 2
            oval_rect = [(oval_x1, y - 5), (oval_x2, y + 50)]
            draw.ellipse(oval_rect, outline='black', width=3)
            
            # Centrar el texto dentro del óvalo
            texto_val = str(valor)
            ancho_txt = draw.textlength(texto_val, font=font_normal)
            draw.text((oval_centro - (ancho_txt / 2), y + 10), texto_val, fill='black', font=font_normal)

        dibujar_fila(y_pos, "GINECOLOGIA", gine)
        y_pos += 70
        dibujar_fila(y_pos, "CIRUGIA", ciru)
        y_pos += 70
        dibujar_fila(y_pos, "MEDICINA", medi)
        y_pos += 70
        dibujar_fila(y_pos, "PEDIATRIA", pedi)
        
        fondo_cuadro = y_pos + 65
        
        # Rectángulo respetando margen derecho
        draw.rectangle([(5, 5), (ancho_util, fondo_cuadro)], outline='black', width=3)
        
        return img