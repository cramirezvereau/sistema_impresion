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
        # Convertir a enteros de forma segura (si está vacío, es 0)
        gine = int(data.get('ginecologia') or 0)
        ciru = int(data.get('cirugia') or 0)
        medi = int(data.get('medicina') or 0)
        pedi = int(data.get('pediatria') or 0)
        
        total = gine + ciru + medi + pedi
        
        # Mantenemos el tamaño normal de la imagen
        img = Image.new('RGB', (self.width_px, self.height_px), 'white')
        draw = ImageDraw.Draw(img)
        
        try:
            font_title = ImageFont.truetype("arialbd.ttf", 22)
            font_bold = ImageFont.truetype("arialbd.ttf", 20)
            font_normal = ImageFont.truetype("arial.ttf", 20)
        except:
            font_title = font_bold = font_normal = ImageFont.load_default()
            
        y_pos = 20
        # Título
        draw.text((20, y_pos), "REPORTE DE PACIENTES DE", fill='black', font=font_title)
        y_pos += 30
        draw.text((20, y_pos), "HOSPITALIZACION", fill='black', font=font_title)
        y_pos += 40
        
        # Fecha y Total
        draw.text((20, y_pos), f"FECHA: {fecha}", fill='black', font=font_bold)
        y_pos += 40
        draw.text((20, y_pos), f"TOTAL DE CAMAS OCUPADAS = {total}", fill='black', font=font_bold)
        y_pos += 60
        
        # Función para dibujar las filas con óvalos
        def dibujar_fila(y, etiqueta, valor):
            draw.text((20, y + 10), etiqueta, fill='black', font=font_bold)
            # Elipse con tamaño ajustado (más grande)
            oval_rect = [(220, y - 5), (430, y + 50)]
            draw.ellipse(oval_rect, outline='black', width=3)
            
            # Centrar el texto dentro del óvalo
            texto_val = str(valor)
            ancho_txt = draw.textlength(texto_val, font=font_normal)
            draw.text((325 - (ancho_txt/2), y + 10), texto_val, fill='black', font=font_normal)

        dibujar_fila(y_pos, "GINECOLOGIA", gine)
        y_pos += 70
        dibujar_fila(y_pos, "CIRUGIA", ciru)
        y_pos += 70
        dibujar_fila(y_pos, "MEDICINA", medi)
        y_pos += 70
        dibujar_fila(y_pos, "PEDIATRIA", pedi)
        
        # ==============================================================
        # DIBUJAR EL RECUADRO HASTA EL FINAL DE LOS DATOS (Sin cortar la imagen)
        # ==============================================================
        # El último óvalo (Pediatría) termina en y_pos + 50. Le damos un margen de 15px.
        fondo_cuadro = y_pos + 65 
        
        # Dibujamos el rectángulo cuidando que la derecha tenga un margen de 15px
        draw.rectangle([(5, 5), (self.width_px - 15, fondo_cuadro)], outline='black', width=3)
        
        # Retornamos la imagen tal cual, sin hacer ".crop()"
        return img